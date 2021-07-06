import nidaqmx as daq
from nidaqmx.constants import CONTINUOUS, READ_ALL_AVAILABLE

daqtask = None

def initialize_ni_stream(daq_name, channels, stream_hz=1000):
    daqtask = daq.Task(daq_name)

    for chn in channels:
        daqtask.ai_channels.add_ai_voltage_chan(chn)
    daqtask.timing.cfg_samp_clk_timing(stream_hz, sample_mode=CONTINUOUS)

def read_samples(daqtask):
    try:
        daqtask.read(number_of_samples_per_channel=READ_ALL_AVAILABLE)