from wrapt import ObjectProxy

REQUESTFLAG = 'Request'
RESPONSEFLAG = 'Response'
RELEASEFLAG = 'Release'


class CountingQueue(ObjectProxy):
    """Class which counts messages and calculates relevant information"""

    def __init__(self, conn, analytics):
        ObjectProxy.__init__(self, conn)
        self._self_conn = conn
        self._self_analytics = analytics

    def put(self, message):
        """Sends message and call functions to count number of messages"""
        self._self_conn.put(message)
        if message.flag == REQUESTFLAG:
            self._self_analytics.send_req()
        elif message.flag == RESPONSEFLAG:
            self._self_analytics.send_resp()

    def get(self):
        """Receives message and call functions to count number of messages"""
        message = self._self_conn.get()
        if message.flag == REQUESTFLAG:
            self._self_analytics.recv_req()
        elif message.flag == RESPONSEFLAG:
            self._self_analytics.recv_resp()
        return message
