from concurrent.futures import ThreadPoolExecutor
import logging

import time



def threading_function(name, sleep):
    logging.info(f"Thread {name}: starting")
    time.sleep(sleep)
    logging.info(f"Thread {name}: finishing")



if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("starting")

    with ThreadPoolExecutor(max_workers=3) as executor:
        
        sleep_values = [2,2,2]
        # must provide a seperate list for each args that is going to be executed on the specified worker threads
        executor.map(threading_function, range(3), sleep_values)

