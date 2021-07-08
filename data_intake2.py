import nidaqmx as daq
from nidaqmx.constants import READ_ALL_AVAILABLE, AcquisitionType
import time
import warnings
from multiprocessing import Queue

# This will run in it's own thread


class NI_Interface:
    def __init__(self, channels=["Dev1/ai0", "Dev1/ai1"], stream_rate=1000) -> None:
        self.daqtask = daq.Task()
        self.intended_stream_rate = 1 / stream_rate

        for chn in channels:
            self.daqtask.ai_channels.add_ai_voltage_chan(chn)

        self.daqtask.timing.cfg_samp_clk_timing(stream_rate)

        self.daqtask.start()
        self.prev_time = time.perf_counter()

    def read_sample(self):
        """Reads in the samples from the daqtask

        Returns:
            List, where the first n values correlate to n channels, with final value equalling the time of sample
        """
        sample = self.daqtask.read()

        sample.append(time.perf_counter())

        return sample

    def safe_exit(self):
        self.daqtask.stop()
        self.daqtask.close()
        print("Closed DAQ")


def data_sender(
    sample_delay, send_queue: Queue = None, communication_queue: Queue = None
):
    ni_interface = NI_Interface()

    running = True

    sample_cache = []

    prev_time = time.perf_counter()

    while running:
        next_sample = ni_interface.read_sample()

        next_sample.append(time.perf_counter())

        sample_cache.append(next_sample)

        prev_time += sample_delay

        try:
            time.sleep(prev_time - time.perf_counter())
        except ValueError:
            if prev_time > 2:
                warnings.warn("System may not be able to handle this DAQ rate")

            prev_time = time.perf_counter()

        if not send_queue.full():
            send_queue.put_nowait(sample_cache)
            sample_cache.clear()

        while not communication_queue.empty():
            val = communication_queue.get_nowait()

            if val == "EXIT":
                ni_interface.safe_exit()
                running = False
