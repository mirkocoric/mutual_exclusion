from _multiprocessing import Connection
from common import RequestFlag, ResponseFlag
from analytics import Analytics


class AnalyticsConnection(object):
    """Class which collects messages and calculates relevant information"""

    def __init__(self):
        self.analytics = Analytics()

    def send(self, conn, message):
        """Sends message and call functions to count number of messages"""
        conn.send(message)
        if message.flag == RequestFlag:
            self.analytics.sent_request_message()
        if message.flag == ResponseFlag:
            self.analytics.sent_response_message()

    def recv(self, conn):
        """Receives message and call functions to count number of messages"""
        message = conn.recv()
        if message.flag == RequestFlag:
            self.analytics.received_request_message()
        if message.flag == ResponseFlag:
            self.analytics.received_response_message()
        return message

    def num_sent_responses(self):
        """Returns number of sent responses"""
        return self.analytics.numsentresponses

    def print_analytics(self, pid):
        """Prints relevant analytics"""
        return self.analytics.print_analytics(pid)
