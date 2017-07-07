"""Testing different mutual exclusion algorithms"""
import argparse
import ping_pong
import ricart_agrawala
import lamport
from data import Data


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
    args = parser.parse_args()
    return (args.n_iter,
            args.n_processes,
            args.method,
            args.process_duration)


def start_app():
    """Creates pipes and processes and starts application"""
    numiter, numprocesses, method, duration = parse_args()
    data = Data(numprocesses, numiter, duration)
    if method == 'pingpong':
        ping_pong.create_all(data)
    elif method == 'ricart_agrawala':
        ricart_agrawala.create_all(data)
    elif method == 'lamport':
        lamport.create_all(data)
    else:
        raise ValueError(
            'Unsupported method. Please choose pingpong or ricart_agrawala')

    print 'Starting processes'
    try:
        for proc in data.processes:
            proc.start()
        for proc in data.processes:
            proc.join()
    finally:
        data.close_conn()
        print 'Pipe closed'


if __name__ == '__main__':
    start_app()
