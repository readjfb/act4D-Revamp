from multiprocessing import Process, Pipe, Queue
from sys import exec_prefix
from time import time
from data_intake import NI_Interface
from data_processor import data_processor
from Saver import data_saver
from EMonitor import run as emonitor_run
from dataclasses import dataclass, field
from typing import List


@dataclass
class MainExperiment:
    mode: str = "DEFAULT"
    submode: str = "SHOULDER ELBOW"
    substate: str = "AUTO"

    target_tor: float = 0.6
    low_lim_tor: float = 0.5
    up_lim_tor: float = 0.7
    match_tor: float = 0.6

    targetF: float = 0.7
    low_limF: float = 0.6
    up_limF: float = 0.8
    matchF: float = 0.75

    timestep: float = 0

    sound_trigger: List[bool] = field(default_factory=list)

    stop_trigger: bool = False

    def __post_init__(self):
        if not self.sound_trigger:
            self.sound_trigger = [False] * 13


def default_demo(experiment, transfer):
    if experiment.submode == "SHOULDER ELBOW":
        transfer['target_tor'] = experiment.target_tor
        transfer['low_lim_tor'] = experiment.low_lim_tor
        transfer['up_lim_tor'] = experiment.up_lim_tor
        transfer['match_tor'] = experiment.match_tor

        transfer['targetF'] = experiment.targetF
        transfer['low_limF'] = experiment.low_limF
        transfer['up_limF'] = experiment.up_limF
        transfer['matchF'] = experiment.matchF

        transfer['sound_trigger'] = experiment.sound_trigger

    elif experiment.submode == "SHOULDER":
        transfer['targetF'] = experiment.targetF
        transfer['low_limF'] = experiment.low_limF
        transfer['up_limF'] = experiment.up_limF
        transfer['matchF'] = experiment.matchF

    else:
        print("Invalid state entered")


def main():
    # emonitor section, delegating the subprocess and connection
    emonitor_queue = Queue()
    em_p = Process(
        target=emonitor_run,
        args=(
            1 / 60,
            emonitor_queue,
        ),
    )
    em_p.start()

    # Initialize NI-DAQ
    ni = NI_Interface()

    # Initialize the saver object; We'll change the stuff that gets passed in,
    # and might change it later on
    saver = data_saver("test_test", "Testing")

    # Initialize the experiment dataclass
    experiment = MainExperiment()

    experiment.submode = "SHOULDER"

    TRANSMIT_KEYS = ['target_tor', 'low_lim_tor', 'up_lim_tor', 'match_tor',
                     'targetF', 'low_limF', 'up_limF', 'matchF', 'sound_trigger', 'stop_trigger']

    MODE_SWITCHER = {"DEFAULT": default_demo}

    # If any of the windows are closed, quit for now; this is something to change later
    while em_p.is_alive():
        data = ni.read_samples()

        if not data:
            # If there's no samples available, just loop again
            # If something must be done at the full framerate, put it before this
            continue

        # Intializes the dict of outputs with zeros
        transfer = dict.fromkeys(TRANSMIT_KEYS, 0)

        transfer['sound_trigger'] = [False] * 13
        transfer['stop_trigger'] = False

        for i in range(len(data[0])):
            # Transpose the matrix from 3xn to nx3
            datapoint = [C[i] for C in data]
            # For all of the other stuff that we want saved, add to this call
            saver.add_data(datapoint)

            experiment.match_tor, experiment.matchF, experiment.timestep = datapoint

            # Call the function that corresponds to the current mode
            # They all should take in the experiment dataclass and the transfer dict
            MODE_SWITCHER[experiment.mode](experiment, transfer)

            # Things that must be run with every datapoint (such as motors)
            # would be called here

        # This runs slowly, so we can run the emonitor whenever it's convenient
        if not emonitor_queue.full():
            emonitor_queue.put(transfer)

    # Exit all processes

    # Clear the queue
    while not emonitor_queue.empty():
        emonitor_queue.get_nowait()

    # Save the data
    saver.save_data("Testing")

    # Exit the DAQ
    ni.safe_exit()


if __name__ == "__main__":
    main()
