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

        self.daqtask.timing.cfg_samp_clk_timing(
            stream_rate, sample_mode=AcquisitionType.CONTINUOUS
        )

        self.daqtask.start()
        self.prev_time = time.perf_counter()

    def read_samples(self):
        """Reads in the samples from the daqtask

        NOTE: This is using interpolation to figure out the timesteps, so I 
        can't promise that the times are *exactly* accurate

        Returns:
            List of samples
        """
        samples = self.daqtask.read(
            number_of_samples_per_channel=READ_ALL_AVAILABLE)

        if len(samples[0]) == 0:
            return None

        next_time = time.perf_counter()

        time_delta = (time.perf_counter() - self.prev_time) / len(samples[0])

        if (abs(1 - (time_delta / self.intended_stream_rate)) > 0.1 and self.prev_time > 5):
            warnings.warn(f"Data intake is not running smoothly")

        samples.append(
            [self.prev_time + (time_delta * i) for i in range(len(samples[0]))]
        )

        transposed = [[C[i] for C in samples] for i in range(len(samples[0]))]

        self.prev_time = next_time

        return transposed

    def safe_exit(self):
        self.daqtask.stop()
        self.daqtask.close()
        print("Closed DAQ")


def data_sender(
    sample_delay, send_queue: Queue = None, communication_queue: Queue = None
):
    """
        Runs in a separate process and constantly fills the send_queue with
        datapoints
    """
    ni_interface = NI_Interface()

    running = True

    sample_cache = []

    prev_time = time.perf_counter()

    while running:
        samples = ni_interface.read_samples()

        if samples:
            sample_cache.extend(samples)

            prev_time += sample_delay

        if not send_queue.full() and sample_cache:
            send_queue.put_nowait(sample_cache)
            sample_cache = []

        while not communication_queue.empty():
            val = communication_queue.get_nowait()

            if val == "EXIT":
                ni_interface.safe_exit()
                running = False
