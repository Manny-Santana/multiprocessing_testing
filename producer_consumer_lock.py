from concurrent.futures import ThreadPoolExecutor
import logging
import threading
import time
import random

# producer thread that reads from the fake network and puts the message into a Pipeline

SENTINEL = object()

def producer(pipeline):
    """pretend we're getting a message from the network."""

    for index in range(10):
        message = random.randint(1,101)
        logging.info(f"Producer got message: {message}")
        pipeline.set_message(message, "Producer")

    pipeline.set_message(SENTINEL, "Producer")