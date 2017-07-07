from select import select
import time
from collections import namedtuple
import common
from multiprocessing import Process
from common import RequestFlag, ResponseFlag
from data import Data
from analytics_connection import AnalyticsConnection
from analytics import Analytics
StartTime = time.time()


def ricart_agrawala(pid, data):
    """Implements ricart_argawala algorithm for mutual exclusion"""
    later_connections = []
    analytics = AnalyticsConnection()
    conn = data.pipesread[pid]
    for _ in xrange(data.numiter):
        timestamp = common.send_request(conn, pid, analytics)
        later_connections = check_messages(conn, timestamp, pid, analytics)
        print ('I am process %d my request time is %f' %
               (pid, timestamp - StartTime))
        time.sleep(data.duration)
        common.send_response(later_connections, timestamp, pid, analytics)
    while analytics.num_sent_responses() < data.numiter * len(conn):
        check_messages_end(conn, timestamp, pid, analytics)
    analytics.print_analytics(pid)


def check_messages(connread, timestamp, pid, analytics):
    """Check messages from connections
    Returns list of connections to send response after leaving critical section
    """
    permissions_number = 0
    send_response_later = []
    while permissions_number < len(connread):
        conncheck, _, _ = select(connread, [], [])
        for conn in conncheck:
            message = analytics.recv(conn)
            print('Process %d received %s'
                  % (pid, message.flag))
            if (message.flag == RequestFlag and
                    message.timestamp < timestamp):
                common.send_response([conn], timestamp, pid, analytics)
            elif (message.flag == RequestFlag):
                send_response_later.append(conn)
            elif (message.flag == ResponseFlag):
                permissions_number += 1
    return send_response_later


def check_messages_end(connread, timestamp, pid, analytics):
    """Check messages when finished if some process is still not sent
    requests
    """
    conncheck, _, _ = select(connread, [], [])
    for conn in conncheck:
        message = conn.recv()
        print('Process %d received %s'
              % (pid, message.flag))
        if message.flag == RequestFlag:
            common.send_response([conn], timestamp, pid, analytics)


def create_processes(data):
    """Creates maxnum processes"""
    return ([Process(target=ricart_agrawala, args=(proc, data))
             for proc in xrange(data.numprocesses)])


def create_all(data):
    """Returns pipes and processes for pingpong"""
    data.set_pipes(common.create_pipes(data.numprocesses), {})
    data.set_processes(create_processes(data))
