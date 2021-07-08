from multiprocessing import Process, Pipe, Queue
from sys import exec_prefix
from time import time
from data_intake2 import data_sender
from data_processor import data_processor
from Saver import data_saver
from EMonitor import run as emonitor_run
from dataclasses import dataclass, field
from typing import List


@dataclass
class MainExperiment:
    experiment_mode: str = "DEFAULT"
    mode_state: str = "SHOULDER ELBOW"
    state_section: str = "AUTO"
    paused: bool = False

    target_tor: float = 0.6
    low_lim_tor: float = 0.5
    up_lim_tor: float = 0.7
    match_tor: float = 0.6

    targetF: float = 0.7
    low_limF: float = 0.6
    up_limF: float = 0.8
    matchF: float = 0.75

    timestep: float = 0

    participant_age: float = 0
    partipant_gender: str = "DEFAULT"
    particiapnt_years_since_stroke: int = 0
    participant_dominant_arm: str = "RIGHT"
    participant_paretic_arm: str = "NONE"

    sound_trigger: List[bool] = field(default_factory=list)

    stop_trigger: bool = False

    def __post_init__(self):
        if not self.sound_trigger:
            self.sound_trigger = [False] * 13


def default_demo(experiment, transfer):
    if experiment.submode == "SHOULDER ELBOW":
        transfer["target_tor"] = experiment.target_tor
        transfer["low_lim_tor"] = experiment.low_lim_tor
        transfer["up_lim_tor"] = experiment.up_lim_tor
        transfer["match_tor"] = experiment.match_tor

        transfer["targetF"] = experiment.targetF
        transfer["low_limF"] = experiment.low_limF
        transfer["up_limF"] = experiment.up_limF
        transfer["matchF"] = experiment.matchF

        transfer["sound_trigger"] = experiment.sound_trigger

    elif experiment.submode == "SHOULDER":
        transfer["targetF"] = experiment.targetF
        transfer["low_limF"] = experiment.low_limF
        transfer["up_limF"] = experiment.up_limF
        transfer["matchF"] = experiment.matchF

    else:
        print("Invalid state entered")


def main():
    # emonitor section, delegating the subprocess and connection
    QUEUES = []

    emonitor_queue = Queue()
    QUEUES.append(emonitor_queue)

    em_p = Process(
        target=emonitor_run,
        args=(1 / 60, emonitor_queue),
    )
    em_p.start()

    # Initialize NI-Interface
    HZ = 1000

    data_transfer_queue = Queue()
    data_intake_comm_queue = Queue()
    QUEUES.append(data_transfer_queue)
    QUEUES.append(data_intake_comm_queue)
    data_intake_p = Process(
        target=data_sender, args=(1 / HZ, data_transfer_queue, data_intake_comm_queue)
    )
    data_intake_p.start()

    # Initialize the saver object; We'll change the stuff that gets passed in,
    # and might change it later on
    saver = data_saver("test_test", "Testing")

    # Initialize the experiment dataclass
    experiment = MainExperiment()

    experiment.mode_state = "SHOULDER"

    TRANSMIT_KEYS = [
        "target_tor",
        "low_lim_tor",
        "up_lim_tor",
        "match_tor",
        "targetF",
        "low_limF",
        "up_limF",
        "matchF",
        "sound_trigger",
        "stop_trigger",
    ]

    MODE_SWITCHER = {"DEFAULT": default_demo}

    # If any of the windows are closed, quit for now; this is something to change later

    data_buffer = None

    while em_p.is_alive():
        data = None


        while data_transfer_queue.not_empty:
            data_seq = data_transfer_queue.get_nowait()
            for point in data_seq:
                data_buffer.append(point)

        if data_buffer:
            data = data_buffer.pop(0)


        if not data:
            continue

        # Intializes the dict of outputs with zeros
        # Care should be taken S.T. dict is initialized with valid, legal
        # arguements
        transfer = dict.fromkeys(TRANSMIT_KEYS, 0)

        transfer["sound_trigger"] = [False] * 13
        transfer["stop_trigger"] = False

        # For all of the other stuff that we want saved, add to this call
        saver.add_data(datapoint)

        experiment.match_tor, experiment.matchF, experiment.timestep = data

        # Call the function that corresponds to the current mode
        # They all should take in the experiment dataclass and the transfer dict
        MODE_SWITCHER[experiment.experiment_mode](experiment, transfer)

        # This runs slowly, so we can run the emonitor whenever it's convenient
        if not emonitor_queue.full():
            emonitor_queue.put(transfer)

    # Exit all processes

    # Exit the DAQ
    data_intake_comm_queue.put("EXIT")
    data_intake_p.join()

    # Clear the queues
    for queue in QUEUES:
        while not queue.empty():
            queue.get_nowait()

    # Save the data
    saver.save_data("Testing")


if __name__ == "__main__":
    main()
