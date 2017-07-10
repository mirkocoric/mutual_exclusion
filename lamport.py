
import time
from multiprocessing import Process
import Queue as q
from mutual_exclusion_methods import create_pipes, send_response, send_request
from mutual_exclusion_methods import receive_message, set_analytics, Message
from mutual_exclusion_methods import check_messages_end
from counting_connection import REQUESTFLAG, RESPONSEFLAG, RELEASEFLAG


def lamport(pid, data, start_time):
    """Implements ricart_argawala algorithm for mutual exclusion"""
    conns = data.pipes_read[pid]
    analytics = set_analytics(conns)
    pq = q.PriorityQueue()
    for _ in xrange(data.n_iter):
        timestamp = send_request(conns, pid)
        pq.put((timestamp, pid))
        check_messages(conns, timestamp, pid, pq)
        print ('I am process %d my request time is %f' %
               (pid, timestamp - start_time))
        time.sleep(data.duration)
        send_release(conns, timestamp, pid)
    while analytics.n_send_resp < data.n_iter * len(conns):
        check_messages_end(conns, timestamp, pid)
    analytics.print_analytics(pid)


def check_messages(connread, timestamp, pid, pq):
    """Check messages from connections
    Returns list of connections to send response after leaving critical section
    """
    n_perm = 0
    while True:
        next_ts, next_pid = pq.get()
        if n_perm == len(connread) and pid == next_pid:
            break
        pq.put((next_ts, next_pid))
        message, conn = receive_message(connread, pid)
        if message.flag == REQUESTFLAG:
            send_response([conn], timestamp, pid)
            pq.put((message.timestamp, message.pid))
        elif message.flag == RESPONSEFLAG:
            n_perm += 1
        elif message.flag == RELEASEFLAG:
            pq.get()


def send_release(connwrite, timestamp, pid):
    """Send release message"""
    for conn in connwrite:
        conn.send(Message(flag=RELEASEFLAG, timestamp=timestamp, pid=pid))
        print ('Process %d sent Release' % pid)


def create_processes(data):
    """Creates maxnum processes"""
    start_time = time.time()
    return ([Process(target=lamport, args=(proc, data, start_time))
             for proc in xrange(data.n_processes)])


def create_all(data):
    """Returns pipes and processes for mutual exclusion"""
    data.set_pipes(create_pipes(data.n_processes), {})
    data.set_processes(create_processes(data))
