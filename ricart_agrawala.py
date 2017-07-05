from select import select
import time
from itertools import combinations
from multiprocessing import Pipe
from multiprocessing import Process
from collections import namedtuple
from statistics import Statistics

Message = namedtuple('Message', 'flag timestamp')
StartTime = time.time()


def process(pid, conn, numiter, duration):
    """Implements ricart_argawala algorithm for mutual exclusion"""
    send_response_later = []
    statistics = Statistics()
    for _ in xrange(numiter):
        timestamp = send_request(conn, pid, statistics)
        send_response_later = check_messages(conn, timestamp, pid, statistics)
        print ('I am process %d my request time is %f' %
               (pid, timestamp - StartTime))
        time.sleep(duration)
        send_response(send_response_later, pid, statistics)
    while statistics.numsentresponses < numiter*len(conn):
        check_messages_end(conn, pid, statistics)
    statistics.print_statistics(pid)


def create_pipes(numprocesses):
    """Creates pipes which connects process with its neighbour
    Returns dictionaries where keys are pid and values are pipes objects for
    reading/writing
    """
    pipes = {i: [] for i in xrange(1, numprocesses+1)}
    for i, j in combinations(xrange(1, numprocesses+1), 2):
        pipe = Pipe()
        pipes[i].append(pipe[0])
        pipes[j].append(pipe[1])
    return pipes


def create_processes(numiter, numprocesses, pipes, duration):
    """Creates maxnum processes"""
    return [Process(target=process, args=(proc, pipes[proc],
                                          numiter, duration))
            for proc in xrange(1, numprocesses + 1)]


def create_message(flag, timestamp):
    """Creates Message for each process"""
    return Message(flag, timestamp)


def send_request(connwrite, pid, statistics):
    """Send request messages to all sites"""
    timestamp = time.time()
    for conn in connwrite:
        conn.send(Message(flag='Request', timestamp=timestamp))
        statistics.sent_request_message()
        print('Process %d sent Request' % pid)
    return timestamp


def send_response(connwrite, pid, statistics):
    """Send response message"""
    for conn in connwrite:
        conn.send(Message(flag='Response', timestamp=None))
        statistics.sent_response_message()
        print ('Process %d sent Response' % pid)


def check_messages_end(connread, pid, statistics):
    """Check messages when finished if some process is still not sent
    requests
    """
    conncheck, _, _ = select(connread, [], [])
    for conn in conncheck:
        message = conn.recv()
        print('Process %d received %s'
              % (pid, message.flag))
        if message.flag == 'Request':
            send_response([conn], pid, statistics)
            statistics.received_request_message()


def check_messages(connread, timestamp, pid, statistics):
    """Check messages from connections
    Returns list of connections to send response after leaving critical section
    """
    permissions_number = 0
    send_response_later = []
    while permissions_number < len(connread):
        conncheck, _, _ = select(connread, [], [])
        for conn in conncheck:
            message = conn.recv()
            print('Process %d received %s'
                  % (pid, message.flag))
            if (message.flag == 'Request' and
               message.timestamp < timestamp):
                send_response([conn], pid, statistics)
                statistics.received_request_message()
            elif (message.flag == 'Request'):
                send_response_later.append(conn)
                statistics.received_request_message()
            elif (message.flag == 'Response'):
                permissions_number += 1
                statistics.received_response_message()
    return send_response_later


def create_all(numprocesses, numiter, duration):
    """Main method which returns pipes and processes for pingpong"""
    pipes = create_pipes(numprocesses)
    return (pipes, {},
            create_processes(numiter, numprocesses, pipes, duration))
