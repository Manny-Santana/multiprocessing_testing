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
        logging.info(f"Thread {name} finishing update - runtime: {t2 - t1}")


if __name__ == "__main__":

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    database = FakeDB()
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=2) as exuecutor:

        for index in range(2):
            exuecutor.submit(database.update, index)
    

    main_stop = time.perf_counter()
    logging.info(f"Testing update ending value is {database.value}, runtime: {main_stop - start}")