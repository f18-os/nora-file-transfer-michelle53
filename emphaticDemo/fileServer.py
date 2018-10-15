#! /usr/bin/env python3

import sys,os#, socket, params
sys.path.append("../lib")       # for params
import re, socket, params
from threading import Thread
from framedSock import FramedStreamSock

class ServerThread(Thread):
    requestCount = 0
    def __init__(self, sock, debug):
        Thread.__init__(self, daemon= True)
        self.fsock, self.debug = FramedStreamSock(s0ck, debug), debug
        self.start()
    def run(self):
        while True:
            msg = self.fsock.receivemsg()
            if not msg:
                if self.debug: print(self.fscok, "server thread done")
                return
            requestNum = ServerThread.requestCount
            time.sleep(0.001)
            ServerThread.requestCount = requestNum + 1
            msg = ("%s! (%d)" (msg, requestNum)).encode()
            self.fsock.sendmsg(msg)



switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)


import framedSock




#fork and create thread
def client_fork():

    while True:
        from framedSock import FramedStreamSock
        sock, addr = lsock.accept()
        print("connection rec'd from", addr)
        ServerThread(sock, debug)
        fsock = FramedStreamSock(sock, debug)
        data = sock.recv( 100 )


        if not data: # check if data is being recieved
            break # check if connection still exists
        while(data): # while data is being sent
            file_out.write(data)
            data = fsock.recv(100)

        file_out.close()
        fsock.sendmsg( b'Finished transfer' )
        fsock.close()

i = 0 # keep track of file written
while True:
    rc = os.fork() # fork
    if rc < 0:
        print('error')
        sys.exit(1)
    elif rc == 0: # child
        file_out = open( 'out_' + str( i ) , 'wb' )
        i = i + 1
        
        #ServerThread( sock, debug)
        client_fork() # write to file
    else:
        child = os.wait()

