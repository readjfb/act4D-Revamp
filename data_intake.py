import nidaqmx as daq
from nidaqmx.constants import READ_ALL_AVAILABLE, AcquisitionType
import time
import warnings


class NI_Interface:
    def __init__(self, channels=["Dev1/ai0", "Dev1/ai1"], stream_rate=1000) -> None:
        self.daqtask = daq.Task()
        self.intended_stream_rate = stream_rate

        for chn in channels:
            self.daqtask.ai_channels.add_ai_voltage_chan(chn)
        self.daqtask.timing.cfg_samp_clk_timing(
            stream_rate, sample_mode=AcquisitionType.CONTINUOUS
        )

        self.daqtask.start()
        self.prev_time = time.perf_counter()

    def read_samples(self):
        """Reads in the samples from the daqtask

        Returns:
            List of Lists: One list for each channel, final list is T
        """
        samples = self.daqtask.read(number_of_samples_per_channel=READ_ALL_AVAILABLE)

        if len(samples[0]) == 0:
            return None

        next_time = time.perf_counter()

        time_delta = (time.perf_counter() - self.prev_time) / len(samples[0])

        if (
            abs(time_delta - self.intended_stream_rate)
            > 0.05 * self.intended_stream_rate
        ):
            warnings.warn("Data intake is not running smoothly")

        samples.append(
            [self.prev_time + (time_delta * i) for i in range(len(samples[0]))]
        )

        self.prev_time = next_time

        return samples

    def safe_exit(self):
        self.daqtask.close()
