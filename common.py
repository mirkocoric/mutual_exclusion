"""Methods which are common for mutual_exclusion algorithms"""

import time
from collections import namedtuple
from multiprocessing import Pipe
from itertools import combinations


Message = namedtuple('Message', 'flag timestamp')
RequestFlag = 'Request'
ResponseFlag = 'Response'


def create_message(flag, timestamp):
    """Creates Message for each process"""
    return Message(flag, timestamp)


def send_request(connwrite, pid, analytics):
    """Send request messages to all sites"""
    timestamp = time.time()
    for conn in connwrite:
        analytics.send(conn, Message(flag=RequestFlag,
                                     timestamp=timestamp))
        print('Process %d sent Request' % pid)
    return timestamp


def send_response(connwrite, timestamp, pid, analytics):
    """Send response message"""
    for conn in connwrite:
        analytics.send(conn, Message(flag=ResponseFlag, timestamp=timestamp))
        print ('Process %d sent Response' % pid)


def create_pipes(numprocesses):
    """Creates pipes which connects process with its neighbour
    Returns dictionaries where keys are pid and values are pipes objects for
    reading/writing
    """
    pipes = {i: [] for i in xrange(numprocesses)}
    for i, j in combinations(xrange(numprocesses), 2):
        pipe = Pipe()
        pipes[i].append(pipe[0])
        pipes[j].append(pipe[1])
    return pipes
