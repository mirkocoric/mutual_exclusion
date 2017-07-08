REQUESTFLAG = 'Request'
RESPONSEFLAG = 'Response'


class CountingConnection(object):
    """Class which counts messages and calculates relevant information"""

    def __init__(self, conn):
        self.conn = conn
        self.analytics = None
        not_copy = ['__class__', 'send', 'recv']
        for attr in dir(conn):
            if attr not in not_copy:
                setattr(self, attr, getattr(conn, attr))

    def set_analytics(self, analytics):
        """Sets analytics object"""
        self.analytics = analytics

    def send(self, message):
        """Sends message and call functions to count number of messages"""
        self.conn.send(message)
        if message.flag == REQUESTFLAG:
            self.analytics.send_req()
        elif message.flag == RESPONSEFLAG:
            self.analytics.send_resp()

    def recv(self):
        """Receives message and call functions to count number of messages"""
        message = self.conn.recv()
        if message.flag == REQUESTFLAG:
            self.analytics.recv_req()
        elif message.flag == RESPONSEFLAG:
            self.analytics.recv_resp()
        return message
