import logging
from threading import Thread
import time


def threading_function(name):
    logging.info(f"Thread {name}: starting")
    time.sleep(2)
    logging.info(f"Thread {name}: finishing")



if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    logging.info(f"Main     : before creating thread")

    x = Thread(target=threading_function, args=(1,) , daemon=True)

    logging.info(f"Main     : before running thread")

    x.start()

    logging.info(f"Main     : waiting for thread to finish")

    x.join()

    logging.info("Main      : all done")