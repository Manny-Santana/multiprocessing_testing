from concurrent.futures import ThreadPoolExecutor
import logging
import time

class FakeDB:
    def __init__(self) -> None:
        self.value = 0

    def update(self, name):
        logging.info(f"Thread {name} starting update")
        t1 = time.perf_counter()
        local_copy = self.value
        local_copy += 1
        time.sleep(0.1)
        self.value = local_copy
        t2 = time.perf_counter()
        logging.info(f"Thread {name} finishing update - runtime: {t1 - t2}")


def threading_function(name, sleep):
    logging.info(f"Thread {name}: starting")
    time.sleep(sleep)
    logging.info(f"Thread {name}: finishing")



if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("starting")
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=3) as executor:
        
        sleep_values = [2,2,2]
        # must provide a seperate list for each args that is going to be executed on the specified worker threads
        executor.map(threading_function, range(3), sleep_values)

    main_stop = time.perf_counter()
    logging.info(f"main program ended with runtime: {start - main_stop}")