import time
import json
import subprocess
import sys
import threading
from pathlib import Path
from os import path
from os import listdir
from web3 import Web3
from web3 import geth
from web3.middleware import geth_poa_middleware

class bcNode:
    #-----------------------------------------------------------------------
    def __init__(self, ip):
    #-----------------------------------------------------------------------
        self.pubKey = ''
        self.enode = ''
        self.web3 = ''
        self.ip = ip
        self.contract = None

    #-====================================Joining the Blockchain======================================

    #-----------------------------------------------------------------------
    def initBlockchainNode(self, genesisPK=None):
    #-----------------------------------------------------------------------

        #Internal function to run node in a new subprocess
        def runNode(command):
            subprocess.run(command, creationflags=subprocess.CREATE_NEW_CONSOLE)

        #Run initialization script
        subprocess.run('cls', shell=True)
        print("Blockchain Node Setup")
        print("1- Initialize node")
        print("2- Run node")
        menuDo = input("Choose option: ")

        #If initialize node
        if(menuDo == '1'):

            #Delete existing data directory
            if(path.exists("./ETH/")):
                print("[Script Output] Deleting existing data directory..")
                command = 'rmdir /q /s "./ETH/"'
                res = subprocess.run(command, shell=True).returncode
                if(res != 0):
                    sys.exit("[Script Output] Could not delete files.")
                else:
                    print("[Script Output] Data directory deleted")

            #Create new account
            print("[Script Output] Creating account...")

            #Create tmp pass file for geth
            tmpFile = open("tmpPass", "w")
            tmpFile.write('123')
            tmpFile.close()

            #Command for creating new account
            command = 'geth account new --datadir ./ETH/node --password tmpPass'

            #Redirect initialization out to logfile
            Path("./logs/blockchain").mkdir(exist_ok=True)
            with open('logs/blockchain/initLog.txt', "w") as outfile:
                subprocess.run(command, shell=True, stdout=outfile, stderr=outfile)
            
            #Delete the tmp file
            import os
            os.remove("tmpPass")

            #Read public keys
            keyFiles = [filename for filename in listdir('./ETH/node/keystore/') if filename.startswith("UTC")]

            #Set PubKey
            self.pubKey = "0x" + keyFiles[0].split("--")[2]

            #Create genesis.json
            genesisJson = json.dumps({"config":{"chainId":15,"homesteadBlock":0,"eip150Block":0,"eip155Block":0,"eip158Block":0,"byzantiumBlock":0,"constantinopleBlock":0,"petersburgBlock":0,"clique":{"period":5,"epoch":30000}},"difficulty":"1","gasLimit":"8000000","extradata":"0x{0}{1}{2}".format(64 * '0', genesisPK[2:], 130 * '0'),"alloc":{"{0}".format(genesisPK[2:]):{"balance":"3000000000000000000000"}}}, indent=4)
            with open("./ETH/genesis.json","w") as genesisFile :
                genesisFile.write(genesisJson)

            #Initialize data directory
            print("[Script Output] Initializing Node...")
            command = 'geth init --datadir ./ETH/node ./ETH/genesis.json'
            init = subprocess.run(command, shell=True).returncode

            #If initialization failed then abort
            if(init != 0):
                sys.exit("[Script Output] Initialization failed. Aborting..")

        #Run Node
        print("[Script Output] Starting node...")
        command = 'geth --datadir ./ETH/node --networkid 15 --cache=2048 --port 30305 --nat extip:{0} --nodiscover'.format(self.ip)

        threading.Thread(target=runNode, args=[command]).start()

        subprocess.run('cls', shell=True)

        #Initialize web3
        time.sleep(3)
        self.web3 = Web3(Web3.IPCProvider())
        print("Web3 connected: ", self.web3.isConnected())
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        #Initialize Enode
        self.enode = self.web3.geth.admin.node_info()["enode"]

        #Make pubKey checksum
        self.pubKey = self.web3.toChecksumAddress(self.pubKey)

        #Initialize contract
        #Get contract address to interface with
        contractAddress = input("Contract Address: ")

        #Initialize contract Abi
        abi = json.loads('[{"inputs":[{"internalType":"uint256","name":"total","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"accountAddress","type":"address"},{"indexed":true,"internalType":"int256","name":"linkToOGF","type":"int256"},{"indexed":false,"internalType":"int256","name":"senderGUID","type":"int256"},{"indexed":true,"internalType":"int256","name":"receiverGUID","type":"int256"},{"indexed":false,"internalType":"string","name":"chunkHash","type":"string"},{"indexed":false,"internalType":"int256","name":"chunkNb","type":"int256"}],"name":"logChunk","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"accountAddress","type":"address"},{"indexed":true,"internalType":"int256","name":"linkToOGF","type":"int256"}],"name":"logDeletion","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"accountAddress","type":"address"},{"indexed":false,"internalType":"int256","name":"linkToOGF","type":"int256"},{"indexed":false,"internalType":"string","name":"fileName","type":"string"},{"indexed":false,"internalType":"string","name":"fileHash","type":"string"},{"indexed":false,"internalType":"int256","name":"totalSize","type":"int256"}],"name":"logFile","type":"event"},{"inputs":[{"internalType":"int256","name":"linkToOGF","type":"int256"}],"name":"deleteFile","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"enroll","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"giveOmnies","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"myBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"int256","name":"linkToOGF","type":"int256"},{"internalType":"int256","name":"senderGUID","type":"int256"},{"internalType":"int256","name":"receiverGUID","type":"int256"},{"internalType":"string","name":"chunkHash","type":"string"},{"internalType":"int256","name":"chunkNb","type":"int256"}],"name":"uploadChunk","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"int256","name":"linkToOGF","type":"int256"},{"internalType":"string","name":"fileName","type":"string"},{"internalType":"string","name":"fileHash","type":"string"},{"internalType":"int256","name":"totalSize","type":"int256"}],"name":"uploadFile","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
        
        #Initialize contract object
        self.contract = self.web3.eth.contract(address=contractAddress, abi=abi)

        #Initialize Account
        self.web3.eth.defaultAccount = self.web3.eth.accounts[0]

        #Unlock Account
        self.web3.geth.personal.unlock_account(self.web3.eth.accounts[0], "123", 0)

        
    #-----------------------------------------------------------------------
    def addToNet(self,enode):
    #-----------------------------------------------------------------------
        #Add node as peer
        self.web3.geth.admin.add_peer(enode)
        print("[Script Output] Adding node as blockchain peer...")
    
    #-----------------------------------------------------------------------
    def enroll(self):
    #-----------------------------------------------------------------------
        try:
            tx_hash = self.contract.functions.enroll().transact()
            tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)

            #Print balance
            print("Omnies Balance: ", self.contract.functions.myBalance().call())

        except:
            print("Error Occured.")

    #-----------------------------------------------------------------------
    def logFileUpload(self, linkToOGF, fileName, fileHash, totalSize):
    #-----------------------------------------------------------------------
        #Transact with smart contract that File needs to be uploaded
        print("[Script Output] Logging File")

        #Call upload file
        tx_hash = self.contract.functions.uploadFile(linkToOGF, fileName, fileHash, totalSize).transact()
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)

        #Print balance
        print("Omnies Balance: ", self.contract.functions.myBalance().call())

    #-----------------------------------------------------------------------
    def logChunkUpload(self, linkToOGF, senderGUID, receiverGUID, chunkHash, chunkNb):
    #-----------------------------------------------------------------------
        #Transact with smart contract that chunk has been uploaded
        print("[Script Output] Logging chunk number", chunkNb)

        #Call upload chunk
        tx_hash = self.contract.functions.uploadChunk(linkToOGF, senderGUID, receiverGUID, chunkHash, chunkNb).transact()
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)

    #-----------------------------------------------------------------------
    def logDeletion(self, linkToOGF):
    #-----------------------------------------------------------------------
        #Transact with smart contract that file has been deleted
        print("[Script Output] Logging file deletion")

        #Call upload chunk
        tx_hash = self.contract.functions.deleteFile(linkToOGF).transact()
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)

    #-----------------------------------------------------------------------
    def filterByAddress(self):
    #-----------------------------------------------------------------------
        #Read logFile events
        validFiles=[]
        event_filter = self.contract.events.logFile.createFilter(fromBlock=0, argument_filters={'accountAddress':self.web3.eth.defaultAccount})
        for event in event_filter.get_all_entries():
            receipt = self.web3.eth.getTransactionReceipt(event['transactionHash']) #Get the transaction receipt
            result = self.contract.events.logFile().processReceipt(receipt) #Process receipt data from hex

            #Check if file is valid
            if self.isFileValid(result[0]['args']['linkToOGF']) :   
                print("Valid File: ")
                print("\tlinkToOGF:", result[0]['args']['linkToOGF'])
                print("\tfileName:", result[0]['args']['fileName'])
                print("\tfileHash:", result[0]['args']['fileHash'])
                print("\ttotalSize:", result[0]['args']['totalSize'])

                validFiles.append(result[0]['args'])
        return validFiles

    #-----------------------------------------------------------------------
    def filterByFile(self, link):
    #-----------------------------------------------------------------------
        #Read logChunk events
        chunks=[]
        event_filter = self.contract.events.logChunk.createFilter(fromBlock=0, argument_filters={'accountAddress':self.web3.eth.defaultAccount, 'linkToOGF':link})
        for event in event_filter.get_all_entries():
            receipt = self.web3.eth.getTransactionReceipt(event['transactionHash']) #Get the transaction receipt
            result = self.contract.events.logChunk().processReceipt(receipt) #Process receipt data from hex

            print("Chunk Nb:", result[0]['args']['chunkNb'])
            print("linkToOGF:", result[0]['args']['linkToOGF'])
            print("senderGUID:", result[0]['args']['senderGUID'])
            print("receiverGUID:", result[0]['args']['receiverGUID'])
            print("chunkHash:", result[0]['args']['chunkHash'])
            
            chunks.append(result[0]['args'])
        return chunks


    #-----------------------------------------------------------------------
    def filterByRGUID(self, recvGUID, chunkHashes):
    #-----------------------------------------------------------------------
        invalidChunksHosted = []
    	#Read logChunk events for the specific recvGUID
        event_filter = self.contract.events.logChunk.createFilter(fromBlock=0, argument_filters={'recvGUID':recvGUID})
        for event in event_filter.get_all_entries():
            receipt = self.web3.eth.getTransactionReceipt(event['transactionHash']) #Get the transaction receipt
            result = self.contract.events.logChunk().processReceipt(receipt) #Process receipt data from hex

            #For each chunk returned, check if its currently on host's machine
            if result[0]['args']['chunkHash'] in chunkHashes:
            	#If yes, check if its invalid
            	if not self.isFileValid(result[0]['args']['linkToOGF']):
            		#If invalid append to list of invalidChunksHosted
                    
            		invalidChunksHosted.append(result[0]['args']['chunkHash'])

        return invalidChunksHosted

    #-----------------------------------------------------------------------
    def isFileValid(self, link):
    #-----------------------------------------------------------------------
        #Read logDeletion events
        event_filter = self.contract.events.logDeletion.createFilter(fromBlock=0, argument_filters={'accountAddress':self.web3.eth.defaultAccount, 'linkToOGF':link})
        if(not event_filter.get_all_entries()):
            return True
        return False