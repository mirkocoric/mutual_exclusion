"""Methods which are common for mutual_exclusion algorithms"""

import time
from collections import namedtuple
from multiprocessing import Pipe
from itertools import combinations
from counting_connection import CountingConnection
from counting_connection import REQUESTFLAG, RESPONSEFLAG


Message = namedtuple('Message', 'flag timestamp')


def create_message(flag, timestamp):
    """Creates Message for each process"""
    return Message(flag, timestamp)


def send_request(connwrite, pid):
    """Send request messages to all sites"""
    timestamp = time.time()
    for conn in connwrite:
        conn.send(Message(flag=REQUESTFLAG, timestamp=timestamp))
        print('Process %d sent Request' % pid)
    return timestamp


def send_response(connwrite, timestamp, pid):
    """Send response message"""
    for conn in connwrite:
        conn.send(Message(flag=RESPONSEFLAG, timestamp=timestamp))
        print ('Process %d sent Response' % pid)


def create_pipes(numprocesses):
    """Creates pipes which connects process with its neighbour
    Returns dictionaries where keys are pid and values are pipes objects for
    reading/writing
    """
    pipes = {i: [] for i in xrange(numprocesses)}
    for i, j in combinations(xrange(numprocesses), 2):
        conn1, conn2 = Pipe()
        pipes[i].append(CountingConnection(conn1))
        pipes[j].append(CountingConnection(conn2))
    return pipes
