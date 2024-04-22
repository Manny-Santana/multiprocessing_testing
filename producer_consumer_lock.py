from concurrent.futures import ThreadPoolExecutor
import logging
import threading
import time
import random


class Pipeline:
    """ class to allow a single element pipeline between producer and consumer"""

    def __init__(self) -> None:
        self.message = 0
        self.producer_lock = threading.Lock()
        self.consumer_lock = threading.Lock()
        self.consumer_lock.acquire() 

    def get_message(self, name):
        logging.debug(f"{name} about to acquire getlock")
        self.consumer_lock.acquire()
        logging.debug(f"{name} has getlock")
        
        message = self.message

        logging.debug(f"{name} about to release setlock")
        self.producer_lock.release()
        logging.debug(f"{name} released setlock")
        

        return message
    
    def set_message(self, message, name):
        logging.debug(f"{name} about to acquire setlock")
        self.producer_lock.acquire()
        logging.debug(f"{name} has setlock")

        self.message = message
        logging.debug(f"{name} about to release getlock")
        self.consumer_lock.release()
        logging.debug(f"{name} getlock released")



# producer thread that reads from the fake network and puts the message into a Pipeline

SENTINEL = object()

def producer(pipeline):
    """pretend we're getting a message from the network."""

    for index in range(10):
        message = random.randint(1,101)
        logging.info(f"Producer got message: {message}")
        pipeline.set_message(message, "Producer")

    # Send a sentinel message to tell consumer we're done
    pipeline.set_message(SENTINEL, "Producer")


def consumer(pipeline):
    """ pretend were saving a number in the db"""

    message = 0
    while message is not SENTINEL:
        message = pipeline.get_message("Consumer")
        if message is not SENTINEL:
            logging.info(f"Consumer storing message {message}")


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    logging.getLogger().setLevel(logging.DEBUG)

    pipeline = Pipeline()
     
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline)
        executor.submit(consumer, pipeline)
