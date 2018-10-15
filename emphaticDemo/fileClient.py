#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os
sys.path.append("../lib")       # for params
import params
import framedSock import FramedStreamSock
from threading import Thread
import time

from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

file_name = input('File to send: ') # get the filename we want to send
#if os.path.exists('./' + file_name):
   # print('file already exists in server')
if not os.path.exists(file_name): # file does not exists
    print('file does not exists')
elif os.path.getsize( file_name) < 0: # file is empty
    print( 'file is empty' )
    s.close()

else:
    f = open( file_name, 'rb' ) # open file to read in bytes

    fs = FramedStreamSock(s, debug=debug)

    data = f.read(100) # read only 100 bytes
    while data: # continue while we are reading
        if not data: break # check if there is a connection still going
        fs.sendmsg( data )
        data = f.read(100)
        for i in range( 100 ):
            ClientThread(serverHost, serverPort, debug)

    f.close() # close file
s.close() # close socket





    
