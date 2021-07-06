import multiprocessing as mp
from queue import Empty
import time

def foo(q):
    i = 0
    while i < 10:
        q.put(i)

        time.sleep(0.5)
        i += 1
    q.put("Returning!")

if __name__ == '__main__':
    ctx = mp.get_context('spawn')
    q = ctx.Queue()
    p = ctx.Process(target=foo, args=(q,))
    p.start()

    i = 0

    while p.is_alive():
        try:
            msg = q.get(block = False)
            print(f"Message {msg}")
        except Empty:
            pass

        if abs(int(i) - i) < 0.001:
            print(f"Hey there{i}")
        i += 0.001
    # p.join()