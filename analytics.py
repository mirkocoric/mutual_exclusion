class Analytics(object):
    """Class which calculates relevant analytics"""

    def __init__(self):
        self.n_send_req = 0
        self.n_send_resp = 0
        self.n_recv_req = 0
        self.n_recv_resp = 0

    def recv_resp(self):
        """Updates number of received response messages"""
        self.n_recv_resp += 1

    def recv_req(self):
        """Updates number of received request messages"""
        self.n_recv_req += 1

    def send_resp(self):
        """Updates number of sent response messages"""
        self.n_send_resp += 1

    def send_req(self):
        """Updates number of sent request messages"""
        self.n_send_req += 1

    def print_analytics(self, pid):
        """Prints relevant analytics"""
        print '********\nAnalytics for process %d' % pid
        print 'Received responses %d' % self.n_recv_resp
        print 'Received requests %d' % self.n_recv_req
        print 'Sent responses %d' % self.n_send_resp
        print 'Sent requests %d' % self.n_send_req
