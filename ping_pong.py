from multiprocessing import Pipe
from multiprocessing import Process
import time


def process(pid, connread, connwrite, numiter, duration):
    """Processes repeatedly calls each other in a circular way"""
    for iteration in xrange(numiter):
        if pid != 1 or iteration != 0:
            connread[0].recv()
        print 'I am process %d' % pid
        time.sleep(duration)
        connwrite[0].send('Done')


def create_processes(numiter, numprocesses, pipesread, pipeswrite, duration):
    """Creates maxnum processes"""
    return [Process(target=process, args=(proc, pipesread[proc],
                                          pipeswrite[proc], numiter,
                                          duration))
            for proc in xrange(1, numprocesses + 1)]


def create_pipes(numprocesses):
    """Creates pipes which connects process with its neighbour
    Returns dictionaries where keys are pid and values are pipes objects for
    reading/writing
    """
    pipesread = {i: [] for i in xrange(1, numprocesses+1)}
    pipeswrite = {i: [] for i in xrange(1, numprocesses+1)}
    for i in xrange(1, numprocesses):
        pipe = Pipe()
        pipeswrite[i].append(pipe[0])
        pipesread[i+1].append(pipe[1])
    pipe = Pipe()
    pipeswrite[numprocesses].append(pipe[0])
    pipesread[1].append(pipe[1])
    return pipesread, pipeswrite


def create_all(numprocesses, numiter, duration):
    """Main method which returns pipes and processes for pingpong"""
    pipesread, pipeswrite = create_pipes(numprocesses)
    return (pipesread, pipeswrite,
            create_processes(numiter, numprocesses, pipesread,
                             pipeswrite, duration))

