from multiprocessing import Process, Pipe
from time import sleep
from data_intake import NI_Interface
from Saver import data_saver


def main():

    ni = NI_Interface(stream_rate=2000)

    saver = data_saver("test_test", "Testing")

    last = [[0], [0], [0]]

    while last[-1][-1] < 5:
        try:
            n = ni.read_samples()

            if n:
                last = n

                for i in range(len(last[0])):
                    saver.add_data([C[i] for C in last])

        except KeyboardInterrupt:
            print(last)
            break

    saver.save_data("Testing")

    ni.safe_exit()


if __name__ == "__main__":
    main()
