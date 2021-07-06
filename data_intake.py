import nidaqmx as daq
from nidaqmx.constants import CONTINUOUS, READ_ALL_AVAILABLE
import time
import warnings

class NI_Interface:
    def __init__(self, daq_name, channels, stream_rate=1000) -> None:
        self.daqtask = daq.Task(daq_name)
        self.intended_stream_rate = stream_rate

        for chn in channels:
            self.daqtask.ai_channels.add_ai_voltage_chan(chn)
        self.daqtask.timing.cfg_samp_clk_timing(stream_rate, sample_mode=CONTINUOUS)

        self.prev_time = time.perf_counter()

    def read_samples(self):
        """Reads in the samples from the daqtask

        Returns:
            2d list: formatted as channel1, channel2... channelN, sample time
        """
        try:
            samples = self.daqtask.read(number_of_samples_per_channel=READ_ALL_AVAILABLE)
        except Exception:
            # DO BETTER CATCHING!!!!
            return []

        time_delta = (time.perf_counter() - self.prev_time) / len(samples)

        if time_delta - self.intended_stream_rate > 0.05 * self.intended_stream_rate:
            warnings.warn('Data intake is not running smoothly')

        tme = self.prev_time()

        for sample in samples:
            sample.append(tme)
            tme += time_delta

        self.prev_time = time.perf_counter()

        return samples
