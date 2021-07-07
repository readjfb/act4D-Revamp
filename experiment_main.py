from multiprocessing import Process, Pipe
from data_intake import NI_Interface
from data_processor import data_processor
from Saver import data_saver
from EMonitor import run as emonitor_run


def main():
    # This is the em (emonitor) section, delegating the subprocess
    em_parent_conn, em_child_conn = Pipe()
    em_p = Process(
        target=emonitor_run,
        args=(
            1 / 60,
            em_child_conn,
        ),
    )

    em_p.start()

    ni = NI_Interface()

    saver = data_saver("test_test", "Testing")

    while em_p.is_alive():
        n = ni.read_samples()

        if n:
            last = n

            timesteps = []

            for i in range(len(last[0])):
                # Transpose the matrix from 3xn to nx3
                timesteps.append([C[i] for C in last])
                saver.add_data(timesteps[-1])

            transfer = dict()

            # These should all be doubles
            transfer['target_tor'] = 0.6
            transfer['low_lim_tor'] = 0.5
            transfer['up_lim_tor'] = 0.7
            transfer['match_tor'] = timesteps[0][0]

            transfer['targetF'] = 0.7
            transfer['low_limF'] = 0.6
            transfer['up_limF'] = 0.8
            transfer['matchF'] = timesteps[0][1]

            # This should be an array of boolean values
            transfer['sound_trigger'] = [0] * 13

            # This should be a single boolean value
            transfer['stop_trigger'] = False

            em_parent_conn.send(transfer)

    ni.safe_exit()
    saver.save_data("Testing")


if __name__ == "__main__":
    main()
