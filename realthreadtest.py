from concurrent.futures import ThreadPoolExecutor
import timeit
import logging

finalresult = []


def chunks(iterable, n):
    """yield successive n-sized chunks from an iterable"""

    for i in range(0, len(iterable), n):
        yield iterable[i: i + n]

def addThree(num_list):
    return [num + 3 for num in num_list]



if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("creating dataset ... ")

    CHUNKSIZE = 100
    DATASIZE = 1000
    data = [ i for i in range(1,DATASIZE)]

    batch = chunks(data, CHUNKSIZE)
    total_chunks = DATASIZE / CHUNKSIZE
    
    

    with ThreadPoolExecutor(max_workers=total_chunks) as executor:
        # add 3 to each item in the array
        for chunk in batch:
            executor.map(addThree, chunk)
            finalresult.extend(chunk)    
            logging.info("Main      : processed chunk")
            logging.info("Thread output: \n")
            print(finalresult)
            
    
    