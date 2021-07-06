from multiprocessing import Process, Pipe
from time import sleep, time
from data_intake import NI_Interface
from data_processor import data_processor
from Saver import data_saver
from EMonitor import run as emonitor_run


def main():
    em_parent_conn, em_child_conn = Pipe()
    em_p = Process(target=emonitor_run, args=(1/60, em_child_conn,))

    em_p.start()

    ni = NI_Interface()

    saver = data_saver("test_test", "Testing")

    while em_p.is_alive():
        n = ni.read_samples()

        if n:
            last = n
            
            timesteps = []

            for i in range(len(last[0])):
                timesteps.append([C[i] for C in last])
                saver.add_data(timesteps[-1])

            arr = [0] * 10

            arr[0] = 0.6
            arr[1] = 0.5
            arr[2] = 0.7
            arr[3] = timesteps[0][0]

            arr[4] = 0.7
            arr[5] = 0.6
            arr[6] = 0.8
            arr[7] = timesteps[0][1]

            arr[8] = [0] * 13

            arr[9] = False

            em_parent_conn.send(arr)

            '''
            # These should all be doubles
            self.target_tor = io_array[0]
            self.low_lim_tor = io_array[1]
            self.up_lim_tor = io_array[2]
            self.match_tor = io_array[3]

            self.targetF = io_array[4]
            self.low_limF = io_array[5]
            self.up_limF = io_array[6]
            self.matchF = io_array[7]

            # This should be an array of booleans
            self.sound_trigger = self.io_array[8]

            # This should be a single boolean value
            self.stop_trigger = self.io_array[9]'''

    saver.save_data("Testing")
    ni.safe_exit()

if __name__ == '__main__':
    main()