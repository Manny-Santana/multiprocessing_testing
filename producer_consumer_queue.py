import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor as ThreadPool
import random
import queue

class Pipeline(queue.Queue):

    """
    pipeline is an object created to store the state of the message at any given time, this pipeline object is passed between the producer and the consumer and the
    data within the state of this pipeline is consumed or modified via mutator functions
    
    """
    def __init__(self) -> None:
        # SIGNAL = object() no more need for a signal we are using an event
        super().__init__(maxsize=10)
        
        
    def get_message(self, name):
        logging.info(f"{name} about to get message from queue")
        value = self.get()
        logging.info(f"{name} got {value} from the queue")
        return value
    
    def set_message(self, value, name):
        logging.info(f"{name} about to add {value} to the queue")
        self.put(value)
        logging.info(f"{name} added {value} to the queue")

def producer(pipeline, event):
    """mocks generating fake number and sending the data via the pipeline and an event"""

    while not event.is_set():
        message = random.randint(1, 101)
        logging.info(f"Producer got message {message}")
        pipeline.set_message(message, "Producer")
    
    logging.info(f"Producer received EXIT event. Exiting")

def consumer(pipeline, event):
    """ 
    mocks saving a number in a db and reading from the pipeline in the network

    """
    while not event.is_set() or not pipeline.empty():
        message = pipeline.get_message("Consumer")
        logging.info(f"Consumer storing message {message} (queue size={pipeline.qsize()})")
        time.sleep(0.3)
        logging.info(f"data: {message} has been stored in the db")
        
    
    logging.info(f"Consumer received EXIT event. Exiting")

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    
    # logging.getLogger().setLevel(logging.DEBUG)


    pipeline = Pipeline()
    event = threading.Event()
    with ThreadPool(max_workers=2) as exec:
        exec.submit(producer, pipeline, event)
        exec.submit(consumer, pipeline, event)
        time.sleep(3)
        logging.info("Main: about to set event")
        event.set()

       