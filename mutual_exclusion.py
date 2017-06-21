'''Testing different mutual exclusion algorithms'''
import argparse
from multiprocessing import Process
from multiprocessing import Pipe
from itertools import combinations

def process(pid, connread, connwrite, numiter, method):
    '''Executes process'''
    if method == 'pingpong':
        pingpong(pid, connread, connwrite, numiter)
    #print(connections_send)
    #print(connections_recv)
    

def create_processes(numiter, numprocesses, method, pipesread, pipeswrite):
    '''Creates maxnum processes'''
    #'Definirati poslije je li treba koristiti jedan ili dva pipea'
    return [Process(target=process, args=(proc, pipesread[proc], pipeswrite[proc], numiter,
                                          method))
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

def pingpong(pid, connread, connwrite, numiter):
    '''Creates two processes and repeatedly calls esach other'''
    for iteration in xrange(numiter):
        if pid != 1 or iteration != 0:
            connread[0].recv()
        print 'I am process %d' % pid
        connwrite[0].send('Done')

def parse_args():
    """Parses arguments"""
    #vidjeti kako ubaciti type int u add_argument
    #zadati vrijeme trajanja procesa, sleep unutar procesa
    parser = argparse.ArgumentParser()
    parser.add_argument('n_iter',
                        help='number of iteration')
    parser.add_argument('n_processes',
                        help='number of processes')
    parser.add_argument('method',
                        help='mutual exclusion method')
    method = parser.parse_args().method
    if method == 'pingpong' or method == 'ricart_argawala':
        pass
    else:
        raise ValueError('Unsupported method. Please choose pingpong or ricart_argawala')
    return (int(parser.parse_args().n_iter),
            int(parser.parse_args().n_processes),
            parser.parse_args().method
           )

def main():
    """Main function"""
    numiter, numprocesses, method = parse_args()
    pipesread, pipeswrite = create_pipes(numprocesses, method)
    processes = create_processes(numiter, numprocesses, method, pipesread, pipeswrite)
    print 'Starting processes'
    for proc in processes:
        proc.start()
    for proc in processes:
        proc.join()
      #zatvoriti sve pipes
    #parent_conn.close()
    #child_conn.close()
    print 'Pipe closed'

if __name__ == '__main__':
    main()
