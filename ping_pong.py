from multiprocessing import Pipe
from multiprocessing import Process
import time


def process(pid, connread, connwrite, numiter, duration):
    """Processes repeatedly calls each other in a circular way"""
    for iteration in xrange(numiter):
        if pid != 0 or iteration != 0:
            connread[0].recv()
        print 'I am process %d' % pid
        time.sleep(duration)
        connwrite[0].send('Done')


def create_processes(data):
    """Creates maxnum processes"""
    return [Process(target=process, args=(proc, data.pipesread[proc],
                                          data.pipeswrite[proc], data.numiter,
                                          data.duration))
            for proc in xrange(data.numprocesses)]


def create_pipes(numprocesses):
    """Creates pipes which connects process with its neighbour
    Returns dictionaries where keys are pid and values are pipes objects for
    reading/writing
    """
    pipesread = {i: [] for i in xrange(numprocesses)}
    pipeswrite = {i: [] for i in xrange(numprocesses)}
    for i in xrange(numprocesses - 1):
        pipe = Pipe()
        pipeswrite[i].append(pipe[0])
        pipesread[i + 1].append(pipe[1])
    pipe = Pipe()
    pipeswrite[numprocesses - 1].append(pipe[0])
    pipesread[0].append(pipe[1])
    return pipesread, pipeswrite


def create_all(data):
    """Main method which returns pipes and processes for pingpong"""
    pipesread, pipeswrite = create_pipes(data.numprocesses)
    data.set_pipes(pipesread, pipeswrite)
    data.set_processes(create_processes(data))
