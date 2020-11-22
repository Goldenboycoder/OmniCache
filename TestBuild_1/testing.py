from testingnode import Node
import threading
import datetime
from pathlib import Path
import time

myNode=''
ip= input('ip : ') #providing your ip (if in lan local otherwise public)
port = eval(input("port : ")) # Port dedicated for the P2P network
genesis= input("genesis node ? (y/n): ")


if genesis == 'y':
    pubk=input('public key : ')
    enode=input('ENode : ')
    #initialize the node 
    myNode = Node(ip,port,npeer=10,publicKey=pubk,enode=enode,genesis=True)
    #start listesing for any connection/request 
    myNode.connectionSpawner()
else:
    # initialize Normal node
    myNode = Node(ip,port,npeer=10,genesis=False) 
    print('Enter Node info to connect to \n')
    hip = input("ip : ")
    hport = eval(input("port : "))
    # prepare join request arguments 
    tosend='-'.join([ip,str(port)])
    # start listening on provided port
    thread=threading.Thread(target=myNode.connectionSpawner,args=[])
    thread.start()
    #send join request
    myNode.connectAndSend(hip,hport,'join',tosend,waitReply=False)





