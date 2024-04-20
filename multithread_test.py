import logging
from threading import Thread
import time


def threading_function(name,sleep):
    logging.info(f"Thread {name}: starting")
    time.sleep(sleep)
    logging.info(f"Thread {name}: finishing")



if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    worker_threads = list()


    for index in range(3):
        logging.info(f"Main      : create and start thread {index}")

        x = Thread(target=threading_function, args=(index, 2))

        worker_threads.append(x)

        x.start()

    for index, thread in enumerate(worker_threads):
        logging.info(f"Main      : before joining thread {index}")
        thread.join()
        logging.info(f"Main      : thread {index} done ")
