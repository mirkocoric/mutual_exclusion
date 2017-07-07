from _multiprocessing import Connection
from common import RequestFlag, ResponseFlag


class Analytics(object):
    """Class which calculates relevant analytics"""

    def __init__(self):
        self.numsentrequests = 0
        self.numsentresponses = 0
        self.numrecvrequests = 0
        self.numrecvresponses = 0

    def received_response_message(self):
        """Updates number of received response messages"""
        self.numrecvresponses += 1

    def received_request_message(self):
        """Updates number of received request messages"""
        self.numrecvrequests += 1

    def sent_response_message(self):
        """Updates number of sent response messages"""
        self.numsentresponses += 1

    def sent_request_message(self):
        """Updates number of sent request messages"""
        self.numsentrequests += 1

    def print_analytics(self, pid):
        """Prints relevant analytics"""
        print '********\nAnalytics for process %d' % pid
        print 'Received responses %d' % self.numrecvresponses
        print 'Received requests %d' % self.numrecvrequests
        print 'Sent responses %d' % self.numsentresponses
        print 'Sent requests %d' % self.numsentrequests
