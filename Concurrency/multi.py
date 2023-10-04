import multiprocessing 
import random 
from datetime import datetime
import time

def printCurrentTime():
    time.sleep(random.random())
    print(datetime.now())

if __name__== "__main__":
    processes = [multiprocessing.Process(target=printCurrentTime)for _ in range(3)]

    for p in processes: 
        p.start()

    for p in processes:
        p.join()
