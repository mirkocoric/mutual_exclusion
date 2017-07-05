"""Testing different mutual exclusion algorithms"""
import argparse
import ping_pong
import ricart_agrawala


def parse_args():
    """Parses arguments from command line"""
    parser = argparse.ArgumentParser()
    parser.add_argument('n_iter',
                        help='number of iteration',
                        type=int)
    parser.add_argument('n_processes',
                        help='number of processes',
                        type=int)
    parser.add_argument('method',
                        help='mutual exclusion method')
    parser.add_argument('process_duration',
                        help='Duration of each process',
                        type=float)
    return (parser.parse_args().n_iter,
            parser.parse_args().n_processes,
            parser.parse_args().method,
            parser.parse_args().process_duration)


def close_conn(pipes):
    """Closes all pipes from pipes dictionary"""
    filter(lambda x: x.close(), (conn for listconn in pipes.keys()
                                 for conn in pipes[listconn]))


def start_app():
    """Creates pipes and processes and starts application"""
    numiter, numprocesses, method, duration = parse_args()
    if method == 'pingpong':
        pipesread, pipeswrite, processes = \
            ping_pong.create_all(numprocesses, numiter, duration)
    elif method == 'ricart_agrawala':
        pipesread, pipeswrite, processes = \
            ricart_agrawala.create_all(numprocesses, numiter, duration)
    else:
        raise ValueError(
            'Unsupported method. Please choose pingpong or ricart_agrawala')

    print 'Starting processes'
    try:
        for proc in processes:
            proc.start()
        for proc in processes:
            proc.join()
    finally:
        close_conn(pipesread)
        close_conn(pipeswrite)
        print 'Pipe closed'

if __name__ == '__main__':
    start_app()
