#!/usr/bin/env python

import threading

def specialFunction(item):
    for n in xrange(100):
        item += n
    return item

class MT_handler(threading.Thread):
    def __init__(self,inputList):
        threading.Thread.__init__(self)
        self._inputList = inputList


    def run(self):
        global resultDic, tLock
        threadName = threading.currentThread().getName()
        print threadName, 'start!'
        for item in self._inputList:
            result = specialFunction(item)
            tLock.acquire()
            resultDic[result] = threadName
            tLock.release()
        print threadName, 'finished!'

def main():
    global resultDic, tLock
    threadNumber = 24
    threadPool = []
    resultDic = {}
    tLock = threading.Lock()

    # insert thread to thread pool
    for x in xrange(0,threadNumber):
        threadPool.append(MT_handler(range(x,x+10000)))

    # init threads
    for t in threadPool:
        t.start()

    # running till all finished

    # join and close threads
    for t in threadPool:
        t.join()
    for n in sorted(resultDic.keys()):
        print n, resultDic[n]

if __name__ == '__main__':
    main()
