"""Methods which are common for mutual_exclusion algorithms"""

import time
from collections import namedtuple
from multiprocessing import Pipe
from itertools import combinations
from select import kevent, kqueue
from counting_connection import CountingConnection
from counting_connection import REQUESTFLAG, RESPONSEFLAG
from analytics import Analytics

Message = namedtuple('Message', 'flag timestamp pid')


def create_message(flag, timestamp, pid):
    """Creates Message for each process"""
    return Message(flag, timestamp, pid)


def send_request(connwrite, pid):
    """Send request messages to all sites"""
    timestamp = time.time()
    for conn in connwrite:
        conn.send(Message(flag=REQUESTFLAG, timestamp=timestamp, pid=pid))
        print('Process %d sent Request' % pid)
    return timestamp


def send_response(connwrite, timestamp, pid):
    """Send response message"""
    for conn in connwrite:
        conn.send(Message(flag=RESPONSEFLAG, timestamp=timestamp, pid=pid))
        print ('Process %d sent Response' % pid)


def find_connection(event, connread):
    """Find connection for which event is related"""
    for conn in connread:
        if conn.fileno() == event.ident:
            return conn


def receive_message(connread, pid):
    """Receives one message"""
    k = [kevent(conn) for conn in connread]
    queue = kqueue()
    queue.control(k, 0)
    event = queue.control(None, 1)
    conncheck = find_connection(event[0], connread)
    message = conncheck.recv()
    print('Process %d received %s'
          % (pid, message.flag))
    return message, conncheck


def create_pipes(numprocesses):
    """Creates pipes which connects process with its neighbour
    Returns dictionaries where keys are pid and values are pipes objects for
    reading/writing
    """
    pipes = {i: [] for i in xrange(numprocesses)}
    analytics = [Analytics() for i in xrange(numprocesses)]
    for i, j in combinations(xrange(numprocesses), 2):
        conn1, conn2 = Pipe()
        pipes[i].append(CountingConnection(conn1, analytics[i]))
        pipes[j].append(CountingConnection(conn2, analytics[j]))
    return pipes


def check_messages_end(connread, timestamp, pid):
    """Check messages when finished if some process is still not sent
    requests
    """
    message, conn = receive_message(connread, pid)
    if message.flag == REQUESTFLAG:
        send_response([conn], timestamp, pid)
