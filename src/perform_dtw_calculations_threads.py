import queue
import threading
import time
import os
import itertools
from app.analyzer import Analyzer

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print(f'starting {self.name}') 
        process_data(self.name, self.q)
        print(f'exiting {self.name}')

def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print( "%s processing %s-%s" % (threadName, data[0], data[1]))
            analyzer = Analyzer()
            analyzer.current_recording = data[0]
            analyzer.current_pattern = data[1]
            analyzer.analyze_dtw()
        else:
            queueLock.release()
            time.sleep(1)

threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4"]
nameList = ["One", "Two", "Three", "Four", "Five"]
queueLock = threading.Lock()
workQueue = queue.Queue(60)
threads = []
threadID = 1

recordings = os.listdir('./Recordings')
patterns = os.listdir('./Patterns')
list_tuple = list(itertools.product(recordings, patterns))
list_tuple = [tuple for tuple in list_tuple if tuple[0] not in ('R1.wav', 'C61.wav', 'R150-1.wav')]

# Create new threads
for tName in threadList:
   thread = myThread(threadID, tName, workQueue)
   thread.start()
   threads.append(thread)
   threadID += 1

# Fill the queue
queueLock.acquire()
for tuple in list_tuple:
    workQueue.put(tuple)
queueLock.release()

# Wait for queue to empty
while not workQueue.empty():
   pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
   t.join()
print("Exiting Main Thread")