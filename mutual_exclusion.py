'''Testing different mutual exclusion algorithms'''
import argparse
from multiprocessing import Process
from multiprocessing import Pipe
from itertools import combinations
import time

def process(pid, connread, connwrite, numiter, method, duration):
    '''Executes process'''
    if method == 'pingpong':
        pingpong(pid, connread, connwrite, numiter, duration)
    #print(connections_send)
    #print(connections_recv)
    

def create_processes(numiter, numprocesses, method, pipesread, pipeswrite, duration):
    '''Creates maxnum processes'''
    #'Definirati poslije je li treba koristiti jedan ili dva pipea'
    return [Process(target=process, args=(proc, pipesread[proc], pipeswrite[proc], numiter,
                                          method, duration))
            for proc in xrange(1, numprocesses + 1)]

def create_pipes_all(numprocesses):
    '''Creates pipes which connects every process pair'''
    pipes = {i:[] for i in xrange(1, numprocesses+1)}
    for i, j in combinations(xrange(1, numprocesses+1), 2):
        pipe = Pipe()
        pipes[i].append(pipe[0])
        pipes[j].append(pipe[1])
    return pipes, pipes

def create_pipes_ping_pong(numprocesses):
    '''Creates pipes which connects process with its neighbour'''
    pipesread = {i:[] for i in xrange(1, numprocesses+1)}
    pipeswrite = {i:[] for i in xrange(1, numprocesses+1)}
    for i in xrange(1, numprocesses):
        pipe = Pipe()
        pipeswrite[i].append(pipe[0])
        pipesread[i+1].append(pipe[1])
    pipe = Pipe()
    pipeswrite[numprocesses].append(pipe[0])
    pipesread[1].append(pipe[1])
    return pipesread, pipeswrite

def create_pipes(numprocesses, method):
    '''Creates pipes'''
    if method == 'ricart_argawala':
        pipes = create_pipes_all(numprocesses)
    if method == 'pingpong':
        pipes = create_pipes_ping_pong(numprocesses)
    return pipes
#def ricart_argawala(number, pipes, numiter):
#svaki svoj priority queue

def pingpong(pid, connread, connwrite, numiter, duration):
    '''Creates two processes and repeatedly calls esach other'''
    for iteration in xrange(numiter):
        if pid != 1 or iteration != 0:
            connread[0].recv()
        print 'I am process %d' % pid
        time.sleep(duration)
        connwrite[0].send('Done')

def parse_args():
    """Parses arguments"""
    #zadati vrijeme trajanja procesa, sleep unutar procesa
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
    method = parser.parse_args().method
    if method == 'pingpong' or method == 'ricart_argawala':
        pass
    else:
        raise ValueError('Unsupported method. Please choose pingpong or ricart_argawala')
    return (parser.parse_args().n_iter,
            parser.parse_args().n_processes,
            parser.parse_args().method,
            parser.parse_args().process_duration
           )

def main():
    """Main function"""
    numiter, numprocesses, method, duration = parse_args()
    pipesread, pipeswrite = create_pipes(numprocesses, method)
    processes = create_processes(numiter, numprocesses, method, pipesread, pipeswrite, duration)
    print 'Starting processes'
    for proc in processes:
        proc.start()
    for proc in processes:
        proc.join()
    #map(lambda val: val.close(), [val for key in pipesread for val in key])
    #map(lambda val: val.close(), [val for key in pipeswrite for val in key])
    #for conn in pipeswrite:
     #   conn.close()
      #zatvoriti sve pipes TODO
    #parent_conn.close()
    #child_conn.close()
    print 'Pipe closed'

if __name__ == '__main__':
    main()
