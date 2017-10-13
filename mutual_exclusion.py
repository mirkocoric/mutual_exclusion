"""Testing different mutual exclusion algorithms"""
import argparse
import ping_pong
import ricart_agrawala
import lamport
from mutual_exclusion_data import MutualExclusionData


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
    parser.add_argument('duration',
                        help='Duration of each process',
                        type=float)
    return parser.parse_args()


def start_app():
    """Creates pipes and processes and starts application"""
    args = parse_args()
    data = MutualExclusionData(args)
    if args.method == 'pingpong':
        ping_pong.create_all(data)
    elif args.method == 'ricart_agrawala':
        ricart_agrawala.create_all(data)
    elif args.method == 'lamport':
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
        data.close()
        print 'Pipe closed'


if __name__ == '__main__':
    start_app()
