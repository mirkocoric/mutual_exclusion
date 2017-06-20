'''Testing different mutual exclusion algorithms'''
import argparse
from multiprocessing import Process
from multiprocessing import Pipe

def process(number, conn, maxnum):
    '''Executes process'''
    for iteration in xrange(1, maxnum):
        if number != 1 or iteration != 1:
            conn.recv()
        print 'I am process %d' % number
        conn.send('Done')
    

def pingpong(maxnum):
    '''Creates two processes and repeatedly calls each other'''
    parent_conn, child_conn = Pipe()
    #create processes
    process1 = Process(target=process, args=(1, child_conn, maxnum))
    process2 = Process(target=process, args=(2, parent_conn, maxnum))
    print 'Starting processes'
    process1.start()
    process2.start()
    process1.join()
    process2.join()
    parent_conn.close()
    child_conn.close()
    print 'Pipe closed'

def parse_args():
    """Parses arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('n',
                        help='numbers to print')
    return int(parser.parse_args().n)

def main():
    """Main function"""
    maxnum = parse_args()
    pingpong(maxnum)

if __name__ == '__main__':
    main()
