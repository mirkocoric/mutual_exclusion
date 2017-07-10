from wrapt import ObjectProxy

REQUESTFLAG = 'Request'
RESPONSEFLAG = 'Response'
RELEASEFLAG = 'Release'


class CountingConnection(ObjectProxy):
    """Class which counts messages and calculates relevant information"""

    def __init__(self, conn):
        ObjectProxy.__init__(self, conn)
        self._self_conn = conn
        self._self_analytics = None

    def set_analytics(self, analytics):
        """Sets analytics object"""
        self._self_analytics = analytics

    def send(self, message):
        """Sends message and call functions to count number of messages"""
        self._self_conn.send(message)
        if message.flag == REQUESTFLAG:
            self._self_analytics.send_req()
        elif message.flag == RESPONSEFLAG:
            self._self_analytics.send_resp()

    def recv(self):
        """Receives message and call functions to count number of messages"""
        message = self._self_conn.recv()
        if message.flag == REQUESTFLAG:
            self._self_analytics.recv_req()
        elif message.flag == RESPONSEFLAG:
            self._self_analytics.recv_resp()
        return message
