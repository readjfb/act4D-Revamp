from multiprocessing import Process, Queue
from data_intake import data_sender
from data_processor import data_processor
from Saver import data_saver
from EMonitor import run as emonitor_run
from GUI import launchGUI as gui_run
from dataclasses import dataclass, field
from typing import List
from collections import deque
from plotter import animation_control


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

    match_tor_zeroed: float = 0
    matchF_zeroed: float = 0

    timestep: float = 0

    # Info about the participants
    participant_age: float = 0
    participant_gender: str = "UNSPECIFIED"
    participant_years_since_stroke: int = 0
    participant_dominant_arm: str = "RIGHT"
    participant_paretic_arm: str = "NONE"

    rNSA: int = 0
    FMA: int = 0
    subject_type: str = "UNSPECIFIED"

    subject_number: float = 0
    trial_toggle: str = "Testing"
    testing_arm: str = "Default"

    cache_tor: List[float] = field(default_factory=list)
    cacheF: List[float] = field(default_factory=list)

    mvt_tor: float = 0.0
    mvt_f: float = 0.0

    tare_tor: float = 0.0
    tare_f: float = 0.0

    prev_time: float = 0.0

    sound_trigger: List[str] = field(default_factory=str)

    stop_trigger: bool = False

    def __post_init__(self):
        if not self.sound_trigger:
            self.sound_trigger = []

        if not self.cache_tor:
            self.cache_tor = list()

        if not self.cacheF:
            self.cacheF = list()

"""
experiment.mode_state will be set to START when the start button is pressed
"""

def default_demo(experiment, transfer):
    if experiment.mode_state == "START":
        experiment.mode_state = "SHOULDER ELBOW"

    if experiment.mode_state == "SHOULDER ELBOW":
        transfer["target_tor"] = experiment.target_tor
        transfer["low_lim_tor"] = experiment.low_lim_tor
        transfer["up_lim_tor"] = experiment.up_lim_tor
        transfer["match_tor"] = experiment.match_tor_zeroed

        transfer["targetF"] = experiment.targetF
        transfer["low_limF"] = experiment.low_limF
        transfer["up_limF"] = experiment.up_limF
        transfer["matchF"] = experiment.matchF_zeroed

        transfer["sound_trigger"] = experiment.sound_trigger

    elif experiment.mode_state == "SHOULDER":
        transfer["targetF"] = experiment.targetF
        transfer["low_limF"] = experiment.low_limF
        transfer["up_limF"] = experiment.up_limF
        transfer["matchF"] = experiment.matchF

    else:
        print("Invalid state entered")


def blank_screen(experiment, transfer):
    if experiment.mode_state == "START":
        pass

    transfer = transfer


def zero_sensors(experiment, transfer):
    # To be created
    if experiment.mode_state == "START":
        # Do the audio cue; for now print
        # transfer["stop_trigger"] = True
        experiment.saver.clear()

        experiment.mode_state = "Wait"
        experiment.prev_time = experiment.timestep

    if experiment.mode_state == "Default":
        transfer["target_tor"] = experiment.target_tor
        transfer["low_lim_tor"] = experiment.low_lim_tor
        transfer["up_lim_tor"] = experiment.up_lim_tor
        transfer["match_tor"] = experiment.match_tor_zeroed

        transfer["targetF"] = experiment.targetF
        transfer["low_limF"] = experiment.low_limF
        transfer["up_limF"] = experiment.up_limF
        transfer["matchF"] = experiment.matchF_zeroed

        experiment.cache_tor = list()
        experiment.cacheF = list()

    elif experiment.mode_state == "Wait":
        wait_time = 2
        transfer["sound_trigger"].append("starting")

        if experiment.timestep - experiment.prev_time > wait_time:
            experiment.mode_state = "Zeroing"
            experiment.prev_time = experiment.timestep

    elif experiment.mode_state == "Zeroing":
        zero_time = 5
        transfer["sound_trigger"].append("relax")
        
        if experiment.timestep - experiment.prev_time > zero_time:
            experiment.mode_state = "Ending"
            experiment.prev_time = experiment.timestep

            experiment.tare_tor = sum(experiment.cache_tor) / len(experiment.cache_tor)
            experiment.tare_f = sum(experiment.cacheF) / len(experiment.cacheF)
            
            experiment.saver.save_data("Zero")

        experiment.cache_tor.append(experiment.match_tor)
        experiment.cacheF.append(experiment.matchF)

    elif experiment.mode_state == "Ending":
        end_time = 0.5
        transfer["sound_trigger"].append("ending")

        if experiment.timestep - experiment.prev_time > end_time:
            experiment.mode_state = "Default"

def main():
    # Emonitor section, delegating the subprocess and connection
    QUEUES = []

    # Process for monitor and monitor queue

    emonitor_queue = Queue()

    QUEUES.append(emonitor_queue)
    em_p = Process(target=emonitor_run, args=(1 / 60, emonitor_queue))
    em_p.start()

    # Process and queues for the GUI

    gui_queue = Queue()
    gui_out_queue = Queue()
    QUEUES.append(gui_queue)
    QUEUES.append(gui_out_queue)

    gui_p = Process(target=gui_run, args=(gui_queue, gui_out_queue))
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

    # Initialize plotting???

    plotting_comm_queue = Queue()
    QUEUES.append(plotting_comm_queue)
    plotting_p = Process(target=animation_control, args=(plotting_comm_queue,))
    plotting_p.start()

    # Initialize the saver object; We'll change the stuff that gets passed in,
    # and might change it later on
    saver = data_saver("subject0")

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

    # Initialize the experiment dataclass
    experiment = MainExperiment()

    experiment.experiment_mode = "DEMO"
    experiment.mode_state = "SHOULDER ELBOW"

    experiment.saver = saver

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

    MODE_SWITCHER = {"DEMO": default_demo, "BLANK": blank_screen, "ZERO": zero_sensors}

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

        # Get the data from the remote controls
        while not gui_queue.empty():
            header, gui_data = gui_queue.get()

            if header == "Close":
                gui_p.terminate()
                em_p.terminate()

            elif header == "Subject info":
                experiment.participant_age = gui_data["Age"]
                experiment.particiapnt_years_since_stroke = gui_data[
                    "Years since stroke"
                ]
                experiment.participant_dominant_arm = gui_data["Dominant Arm"]
                experiment.participant_paretic_arm = gui_data["Recovery Paretic Arm"]
                experiment.partipant_gender = gui_data["Gender"]

                experiment.rNSA = gui_data["rNSA"]
                experiment.FMA = gui_data["FMA"]
                experiment.subject_type = gui_data["Subject Type"]

            elif header == "Jacobean Constants":
                pass

            elif header == "Maxes":
                pass

            elif header == "Save":
                saver.save_data(experiment.experiment_mode)
                saver.clear()

            elif header == "Erase":
                saver.clear()

            elif header == "Start":
                experiment.subject_number = gui_data["Subject Number"]
                experiment.trial_toggle = gui_data["Trial Toggle"]
                experiment.testing_arm = gui_data["Testing Arm"]
                experiment.experiment_mode = gui_data["Trial Type"]

                experiment.mode_state = "START"

                saver.update_save_dir("Subject"+str(experiment.subject_number))

            # print(header, "|||", gui_data)

        if not data:
            continue

        experiment.match_tor, experiment.matchF, experiment.timestep = data

        experiment.match_tor_zeroed = experiment.match_tor - experiment.tare_tor
        experiment.matchF_zeroed = experiment.matchF - experiment.tare_f

        # This aligns with the header; if we change the order of the header, this has to be changed as well
        saver.add_data(
            [
                experiment.match_tor_zeroed,
                experiment.matchF_zeroed,
                experiment.timestep,
                experiment.experiment_mode,
                experiment.mode_state,
                experiment.state_section,
                experiment.paused,
                experiment.participant_years_since_stroke,
                experiment.participant_age,
                experiment.participant_dominant_arm,
                experiment.participant_paretic_arm,
                experiment.participant_gender,
            ]
        )

        # Initializes the dict of outputs with zeros
        # Care should be taken S.T. dict is initialized with valid, legal
        # arguments
        transfer = dict.fromkeys(TRANSMIT_KEYS, 0)

        transfer["sound_trigger"] = []
        transfer["stop_trigger"] = False

        # Call the function that corresponds to the current mode
        # They all should take in the experiment dataclass and the transfer dict
        MODE_SWITCHER[experiment.experiment_mode](experiment, transfer)

        # This runs slowly, so we can run the emonitor whenever it's convenient
        if not emonitor_queue.full():
            emonitor_queue.put(transfer)

        if not plotting_comm_queue.full():
            # These are the values to be plotted. The first value MUST be the
            # timestep, but the rest may be changed
            graphed_data = [
                experiment.timestep,
                experiment.match_tor,
                experiment.match_tor_zeroed,
                experiment.tare_tor,
                0,
                experiment.matchF,
                experiment.matchF_zeroed,
                experiment.tare_f,
                0,
            ]
            plotting_comm_queue.put(graphed_data)

    # Exit all processes

    # Exit the DAQ
    data_intake_comm_queue.put("EXIT")
    plotting_comm_queue.put("EXIT")
    data_intake_p.join()
    plotting_p.join()

    # Clear the queues
    for queue in QUEUES:
        while not queue.empty():
            queue.get_nowait()


if __name__ == "__main__":
    main()
