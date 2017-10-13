class MutualExclusionData(object):
    """Stores list of pipes, processes and algorithm arguments"""

    def __init__(self, args):
        self.n_iter = args.n_iter
        self.n_processes = args.n_processes
        self.duration = args.duration
        self.pipes_read = None
        self.pipes_write = None
        self.processes = None

    def set_pipes(self, pipes_read, pipes_write):
        """Sets pipes variable"""
        self.pipes_read = pipes_read
        self.pipes_write = pipes_write

    def set_processes(self, processes):
        """Sets processes variable"""
        self.processes = processes

    @staticmethod
    def close_conn(pipes):
        """Closes every pipe in given dictionary"""
        for connlist in pipes.itervalues():
            for conn in connlist:
                conn.close()

    def close(self):
        """Closes created pipes"""
        self.close_conn(self.pipes_read)
        self.close_conn(self.pipes_write)
