import threading, queue
import time

if __name__ == '__main__':
    text = queue.Queue()

    for i in range(0,10):
        text.put(i)

    while True:
        try:
            tt = text.get_nowait()
        except queue.Empty:
            tt = 0
        print(tt)
        time.sleep(0.5)

