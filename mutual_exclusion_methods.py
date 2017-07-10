"""Methods which are common for mutual_exclusion algorithms"""

import time
from collections import namedtuple
from multiprocessing import Pipe
from itertools import combinations
from select import select
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


def receive_message(connread, pid):
    """Receives one message"""
    conncheck, _, _ = select(connread, [], [])
    if conncheck:
        message = conncheck[0].recv()
        print('Process %d received %s'
              % (pid, message.flag))
        return message, conncheck[0]


def set_analytics(conns):
    """Creates analytics object and sets it to each connection"""
    analytics = Analytics()
    for conn in conns:
        conn.set_analytics(analytics)
    return analytics


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


def check_messages_end(connread, timestamp, pid):
    """Check messages when finished if some process is still not sent
    requests
    """
    message, conn = receive_message(connread, pid)
    if message.flag == REQUESTFLAG:
        send_response([conn], timestamp, pid)
