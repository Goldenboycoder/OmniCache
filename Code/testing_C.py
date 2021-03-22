import threading
import datetime
from pathlib import Path
import time
import subprocess
from p2p_C import Node
from blockchain_C import bcNode

subprocess.run('cls', shell=True)
print("Test Environment Setup Script")

#Obtain IP and Port
ip = input('[Script Output] IP: ') #Providing your ip (if in lan local otherwise public)
port = eval(input("[Script Output] Port: ")) #Port dedicated for the P2P network
subprocess.run('cls', shell=True)

#Initialize blockchain node
bc_Node = bcNode(ip)

#Initialize p2p node
myNode = Node(ip, port,bc_Node, npeer=10)

print('[Script Output] Enter Node info to connect to \n')
hip = input("[Script Output] Target IP: ")
hport = eval(input("[Script Output] Target Port: "))

#Prepare join request arguments 
tosend='-'.join([ip,str(port)])

#Start listening on provided port
thread=threading.Thread(target=myNode.connectionSpawner,args=[])
thread.start()

#Send join request
myNode.connectAndSend(hip,hport,'join',tosend,waitReply=False)