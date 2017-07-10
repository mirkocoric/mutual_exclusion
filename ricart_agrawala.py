import time
from multiprocessing import Process
from mutual_exclusion_methods import create_pipes, send_response, send_request
from mutual_exclusion_methods import receive_message, set_analytics
from mutual_exclusion_methods import check_messages_end
from counting_connection import REQUESTFLAG, RESPONSEFLAG


def ricart_agrawala(pid, data, start_time):
    """Implements ricart_argawala algorithm for mutual exclusion"""
    conns = data.pipes_read[pid]
    analytics = set_analytics(conns)
    for _ in xrange(data.n_iter):
        timestamp = send_request(conns, pid)
        conns_respond_later = check_messages(conns, timestamp, pid)
        print ('I am process %d my request time is %f' %
               (pid, timestamp - start_time))
        time.sleep(data.duration)
        send_response(conns_respond_later, timestamp, pid)
    while analytics.n_send_resp < data.n_iter * len(conns):
        check_messages_end(conns, timestamp, pid)
    analytics.print_analytics(pid)


def check_messages(connread, timestamp, pid):
    """Check messages from connections
    Returns list of connections to send response after leaving critical section
    """
    n_perm = 0
    conns_respond_later = []
    while n_perm < len(connread):
        message, conn = receive_message(connread, pid)
        if (message.flag == REQUESTFLAG and
                message.timestamp < timestamp):
            send_response([conn], timestamp, pid)
        elif (message.flag == REQUESTFLAG):
            conns_respond_later.append(conn)
        elif (message.flag == RESPONSEFLAG):
            n_perm += 1
    return conns_respond_later


def create_processes(data):
    """Creates maxnum processes"""
    start_time = time.time()
    return ([Process(target=ricart_agrawala, args=(proc, data,  start_time))
             for proc in xrange(data.n_processes)])


def create_all(data):
    """Returns pipes and processes"""
    data.set_pipes(create_pipes(data.n_processes), {})
    data.set_processes(create_processes(data))
