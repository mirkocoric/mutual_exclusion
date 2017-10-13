from multiprocessing import Pipe
from multiprocessing import Process
import time


def process(pid, conn_read, conn_write, n_iter, duration):
    """Processes repeatedly calls each other in a circular way"""
    for iteration in xrange(n_iter):
        if pid or iteration:
            conn_read[0].recv()
        print 'I am process %d' % pid
        time.sleep(duration)
        conn_write[0].send('Done')


def create_processes(data):
    """Creates maxnum processes"""
    return [Process(target=process, args=(proc, data.pipes_read[proc],
                                          data.pipes_write[proc], data.n_iter,
                                          data.duration))
            for proc in xrange(data.n_processes)]


def create_pipes(n_processes):
    """Creates pipes which connects process with its neighbour
    Returns dictionaries where keys are pid and values are pipes objects for
    reading/writing
    """
    pipes_read = {i: [] for i in xrange(n_processes)}
    pipes_write = {i: [] for i in xrange(n_processes)}
    for i in xrange(n_processes - 1):
        pipe = Pipe()
        pipes_write[i].append(pipe[0])
        pipes_read[i + 1].append(pipe[1])
    pipe = Pipe()
    pipes_write[n_processes - 1].append(pipe[0])
    pipes_read[0].append(pipe[1])
    return pipes_read, pipes_write


def create_all(data):
    """Main method which returns pipes and processes for pingpong"""
    pipes_read, pipes_write = create_pipes(data.n_processes)
    data.set_pipes(pipes_read, pipes_write)
    data.set_processes(create_processes(data))
