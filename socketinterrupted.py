
from __future__ import print_function

# interrupting blocking sockets...

from socket import *
import threading, sys, time

def udptest():
    print(">>>>>>>>>>>>>>> UDP")

    def fn(sock, running):
        print("<<<<<<<< recvfrom", sock.fileno())
        running.set()
        print(">>>>>>>>", sock.recvfrom(1024))


    sock = socket(AF_INET, SOCK_DGRAM, 0)
    running = threading.Event()

    T = threading.Thread(target=fn, args=(sock, running))
    T.daemon = True
    print("Starting thread")
    T.start()

    running.wait()
    time.sleep(2) # wait a bit longer to increase chances of actual syscall entry
    print("Thread running")

    try:
        print("Try shutdown()")
        sock.shutdown(SHUT_RDWR)
        print("shutdown() succeeds")
    except:
        print("shutdown() errors")

    T.join(2.0)

    if T.isAlive():
        print("Still alive")
        print("close()")
        sock.close()

    T.join(2.0)

    if T.isAlive():
        print("Still alive!")

    sock.close()
    print("<<<<<<<<<<<<<<<< UDP")
udptest()

def tcpaccepttest():
    print(">>>>>>>>>>>>>>> TCP ACCEPT")

    sock = socket(AF_INET, SOCK_STREAM, 0)
    sock.bind(('127.0.0.1', 0))
    sock.listen(2)

    def fn(sock, running):
        print("<<<<<<<< accept", sock.fileno())
        running.set()
        print(">>>>>>>>", sock.accept())


    running = threading.Event()

    T = threading.Thread(target=fn, args=(sock, running))
    T.daemon = True
    print("Starting thread")
    T.start()

    running.wait()
    time.sleep(2)
    print("Thread running")

    try:
        print("Try shutdown()")
        sock.shutdown(SHUT_RDWR)
        print("shutdown() succeeds")
    except:
        print("shutdown() errors")

    T.join(2.0)

    if T.isAlive():
        print("Still alive")
        print("close()")
        sock.close()

    T.join(2.0)

    if T.isAlive():
        print("Still alive!")

    sock.close()
    print("<<<<<<<<<<<<<<<< TCP ACCEPT")
tcpaccepttest()

def tcprecvtest():
    print(">>>>>>>>>>>>>>> TCP RECV")

    accept = socket(AF_INET, SOCK_STREAM, 0)
    accept.bind(('127.0.0.1', 0))
    accept.listen(1)
    print("bound as", accept.getsockname())
    server = [None]

    def fn(accept, server, running):
        print("<<<<<<<<< accept")
        server[0], addr = accept.accept()
        print("<<<<<<<<< recv")
        running.set()
        print(">>>>>>>>", server[0].recv(1024))


    running = threading.Event()

    T = threading.Thread(target=fn, args=(accept, server, running))
    T.daemon = True
    print("Starting thread")
    T.start()

    print("Thread running")

    client = socket(AF_INET, SOCK_STREAM, 0)
    client.connect(accept.getsockname())
    print("client connects")

    running.wait()
    time.sleep(2)
    print("Thread running")

    try:
        print("Try shutdown()")
        server[0].shutdown(SHUT_RDWR)
        print("shutdown() succeeds")
    except:
        print("shutdown() errors")

    T.join(2.0)

    if T.isAlive():
        print("Still alive")
        print("close()")
        server[0].close()

    T.join(2.0)

    if T.isAlive():
        print("Still alive!")

    server[0].close()
    print("<<<<<<<<<<<<<<<< TCP RECV")
tcprecvtest()

print("Done")
