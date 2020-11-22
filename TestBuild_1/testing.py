from testingnode import Node
import threading
import datetime
from pathlib import Path
import time

import subprocess
import json
import sys
from os import path

myNode=''

subprocess.run('cls', shell=True)
print("Test Environment Setup Script")

genesis = input("[Script Output] Genesis node? (y/n): ")

#Initialize P2P vars
ip = input('[Script Output] IP: ') #providing your ip (if in lan local otherwise public)
port = eval(input("[Script Output] Port: ")) # Port dedicated for the P2P network

subprocess.run('cls', shell=True)

if genesis == 'y':
    #Change dataPath
    dataPath =  "C:/Stash-it/"
    print("[Script Output] Default dataPath for the data directories is: {0}".format(dataPath))
    changePath = input("[Script Output] Change default dataPath? (y/n): ")
    if(changePath == 'y'):
        dataPath = input("[Script Output] Enter a new dataPath: ")
        print("[Script Output] New dataPath: {0}".format(dataPath))
    elif(changePath != 'n'):
        sys.exit("[Script Output] Invalid Input..")

    subprocess.run('cls', shell=True)

    #Init or Run?
    print("1- Initialize node")
    print("2- Run node")

    menuDo = input("Choose option: ")

    #Function to run node in new terminal
    def runNode(command):
        subprocess.run(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
    #If initialize nodes
    if(menuDo == '1'):
        #Detect data directories
        if(path.exists("{0}".format(dataPath))):
            print("[Script Output] Detected data directories")
            delete = input("[Script Output] Delete existing data directories? (y/n): ")
            if(delete == 'y'):
                command = 'rmdir /q /s "{0}"'.format(dataPath)
                res = subprocess.run(command, shell=True).returncode
                if(res != 0):
                    sys.exit("[Script Output] Could not delete files.")
                else:
                    print("[Script Output] Data directories deleted...")

        #Create Account
        print("[Script Output] Creating account...")
        print("[Script Output] Please save the public key.")
        command = 'geth account new --datadir {0}nodeG'.format(dataPath)
        subprocess.run(command, shell=True)

        nodeGPK = input("[Script Output] Enter the public key generated: ")

        #Create genesis.json
        genesisJson = json.dumps({"config":{"chainId":15,"homesteadBlock":0,"eip150Block":0,"eip155Block":0,"eip158Block":0,"byzantiumBlock":0,"constantinopleBlock":0,"petersburgBlock":0,"clique":{"period":5,"epoch":30000}},"difficulty":"1","gasLimit":"8000000","extradata":"0x{0}{1}{2}".format(64 * '0', nodeGPK[2:], 130 * '0'),"alloc":{"{0}".format(nodeGPK[2:]):{"balance":"3000000000000000000000"}}}, indent=4)
        with open("{0}genesis.json".format(dataPath),"w") as genesisFile :
            genesisFile.write(genesisJson)

        #Initializing genesis node
        print("[Script Output] Initializing Node...")
        command = 'geth init --datadir {0}nodeG {0}genesis.json'.format(dataPath)
        init = subprocess.run(command, shell=True).returncode

        #If initialization failed then abort
        if(init != 0):
            sys.exit("[Script Output] Initialization failed. Aborting..")
    else:
        nodeGPK = input("[Script Output] Enter nodeG's public key: ")

    #Run genesis node
    print("[Script Output] Starting genesis node... Please enter nodeG's password when terminal opens.")
    command = 'geth --datadir {0}nodeG --networkid 15 --port 30305 --nat extip:{1} --nodiscover --mine --unlock {2}'.format(dataPath, ip ,nodeGPK)
    threading.Thread(target=runNode, args=[command]).start()

    #Initialize the P2P node 
    myNode = Node(ip, port, npeer=10, publicKey=nodeGPK, genesis=True)
    #Start listening for any connection/request 
    myNode.connectionSpawner()

else:
    #Initialize normal P2P node
    myNode = Node(ip, port, npeer=10, genesis=False) 
    print('[Script Output] Enter Node info to connect to \n')
    hip = input("[Script Output] Target IP: ")
    hport = eval(input("[Script Output] Target Port: "))
    # prepare join request arguments 
    tosend='-'.join([ip,str(port)])
    # start listening on provided port
    thread=threading.Thread(target=myNode.connectionSpawner,args=[])
    thread.start()
    #send join request
    myNode.connectAndSend(hip,hport,'join',tosend,waitReply=False)

