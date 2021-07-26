from multiprocessing import Process, Queue
from data_intake import data_sender
from data_processor import data_processor
from Saver import data_saver
from EMonitor import run as emonitor_run
from GUI import launchGUI as gui_run
from dataclasses import dataclass, field
from typing import List
from collections import deque


@dataclass
class MainExperiment:
    # Experimental state and control
    experiment_mode: str = "DEFAULT"
    mode_state: str = "SHOULDER ELBOW"
    state_section: str = "AUTO"
    paused: bool = False

    # Experimental variables for controling the output
    target_tor: float = 0.6
    low_lim_tor: float = 0.5
    up_lim_tor: float = 0.7
    match_tor: float = 0.6

    targetF: float = 0.7
    low_limF: float = 0.6
    up_limF: float = 0.8
    matchF: float = 0.75

    timestep: float = 0

    # Info about the participants
    participant_age: float = 0
    partipant_gender: str = "UNSPECIFIED"
    particiapnt_years_since_stroke: int = 0
    participant_dominant_arm: str = "RIGHT"
    participant_paretic_arm: str = "NONE"

    rNSA: int = 0
    FMA: int = 0
    subject_type: str = "UNSPECIFIED"

    sound_trigger: List[bool] = field(default_factory=list)

    stop_trigger: bool = False

    def __post_init__(self):
        if not self.sound_trigger:
            self.sound_trigger = [False] * 13


def default_demo(experiment, transfer):
    if experiment.mode_state == "SHOULDER ELBOW":
        transfer["target_tor"] = experiment.target_tor
        transfer["low_lim_tor"] = experiment.low_lim_tor
        transfer["up_lim_tor"] = experiment.up_lim_tor
        transfer["match_tor"] = experiment.match_tor

        transfer["targetF"] = experiment.targetF
        transfer["low_limF"] = experiment.low_limF
        transfer["up_limF"] = experiment.up_limF
        transfer["matchF"] = experiment.matchF

        transfer["sound_trigger"] = experiment.sound_trigger

    elif experiment.mode_state == "SHOULDER":
        transfer["targetF"] = experiment.targetF
        transfer["low_limF"] = experiment.low_limF
        transfer["up_limF"] = experiment.up_limF
        transfer["matchF"] = experiment.matchF

    else:
        print("Invalid state entered")


def main():
    # Emonitor section, delegating the subprocess and connection
    QUEUES = []

    # Process for monitor and monitor queue

    emonitor_queue = Queue()

    QUEUES.append(emonitor_queue)
    em_p = Process(
        target=emonitor_run,
        args=(1 / 60, emonitor_queue)
    )
    em_p.start()

    # Process and queues for the GUI

    gui_queue = Queue()
    gui_out_queue = Queue()
    QUEUES.append(gui_queue)
    QUEUES.append(gui_out_queue)

    gui_p = Process(
        target=gui_run,
        args=(gui_queue,gui_out_queue)
    )
    gui_p.start()

    # Initialize data collection
    HZ = 1000

    data_intake_queue = Queue()
    data_intake_comm_queue = Queue()
    QUEUES.append(data_intake_queue)
    QUEUES.append(data_intake_comm_queue)
    data_intake_p = Process(
        target=data_sender, args=(1 / HZ, data_intake_queue, data_intake_comm_queue)
    )
    data_intake_p.start()

    # Initialize the saver object; We'll change the stuff that gets passed in,
    # and might change it later on
    saver = data_saver("subject0")

    # Initialize the experiment dataclass
    experiment = MainExperiment()

    experiment.experiment_mode = "DEMO"
    experiment.mode_state = "SHOULDER ELBOW"

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

    MODE_SWITCHER = {"DEMO": default_demo}

    # If any of the windows are closed, quit for now; this is something that could be changed

    data_buffer = deque()

    while em_p.is_alive():
        data = None

        while not data_intake_queue.empty():
            data_seq = data_intake_queue.get()
            for point in data_seq:
                data_buffer.append(point)

        if data_buffer:
            data = data_buffer.popleft()

        if not data:
            continue

        # Get the data from the remote controls
        while not gui_queue.empty():
            header, data = gui_queue.get()

            if header == "Subject info":
                experiment.participant_age = data["Age"]
                experiment.particiapnt_years_since_stroke = data["Years since stroke"]
                experiment.participant_dominant_arm = data["Dominant Arm"]
                experiment.participant_paretic_arm = data["Recovery Paretic Arm"]
                experiment.partipant_gender = data["Gender"]

                experiment.rNSA = data["rNSA"]
                experiment.FMA = data["FMA"]
                experiment.subject_type = data["Subject Type"]


            print(header, "|||", data)

        # do the parsing of the queue here

        # Intializes the dict of outputs with zeros
        # Care should be taken S.T. dict is initialized with valid, legal
        # arguements
        transfer = dict.fromkeys(TRANSMIT_KEYS, 0)


        transfer["sound_trigger"] = [False] * 13
        transfer["stop_trigger"] = False

        experiment.match_tor, experiment.matchF, experiment.timestep = data

        # For all of the other stuff that we want saved, add to this call
        data_save_seq = [
            experiment.match_tor,
            experiment.matchF,
            experiment.timestep,
            experiment.experiment_mode,
            experiment.mode_state,
            experiment.state_section,
            experiment.paused,
            experiment.particiapnt_years_since_stroke,
            experiment.participant_age,
            experiment.participant_dominant_arm,
            experiment.participant_paretic_arm,
            experiment.partipant_gender,
        ]

        saver.add_data(data_save_seq)

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
    saver.add_header(
        [
            "Current Tor",
            "Current F",
            "Time",
            "Experiment Mode",
            "Mode State",
            "State Section",
            "Paused",
            "Years Since Stroke",
            "Age",
            "Dom. Arm",
            "Paretic Arm",
            "Gender",
        ]
    )
    saver.save_data(experiment.experiment_mode)


if __name__ == "__main__":
    main()
