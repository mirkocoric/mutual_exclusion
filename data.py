class Data(object):
    """Stores list of pipes, processes and algorithm arguments"""

    def __init__(self, numprocesses, numiter, duration):
        self.numiter = numiter
        self.numprocesses = numprocesses
        self.duration = duration
        self.pipesread = None
        self.pipeswrite = None
        self.processes = None

    def set_pipes(self, pipesread, pipeswrite):
        """Sets pipes variable"""
        self.pipesread = pipesread
        self.pipeswrite = pipeswrite

    def set_processes(self, processes):
        """Sets processes variable"""
        self.processes = processes

    @staticmethod
    def close(pipes):
        """Closes every pipe in given dictionary"""
        for listconn in pipes.keys():
            for conn in pipes[listconn]:
                conn.close()

    def close_conn(self):
        """Closes created pipes"""
        self.close(self.pipesread)
        self.close(self.pipeswrite)
