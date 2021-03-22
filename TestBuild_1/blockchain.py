import time
import json
import subprocess
import sys
import threading
from os import path
from os import listdir
from web3 import Web3
from web3 import geth
from web3.middleware import geth_poa_middleware

class bcNode:
    #-----------------------------------------------------------------------
    def __init__(self, ip, genesis=False):
    #-----------------------------------------------------------------------
        self.pubKey = ''
        self.enode = ''
        self.web3 = ''

        self.isGenesis = genesis
        self.ip = ip

        self.contract = None

        if(self.isGenesis):
            self.initBlockchainNode()

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
            print("[Script Output] Please save the public key.")

            command = 'geth account new --datadir ./ETH/node'
            subprocess.run(command, shell=True)
            self.pubKey = input("[Script Output] Enter the public key generated: ")

            #Set genesisPK if isGenesis
            if self.isGenesis:
                genesisPK = self.pubKey

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

        #Run node
        if(self.isGenesis):
            print("[Script Output] Starting genesis node... Please enter the node's password when terminal opens.")
            command = 'geth --datadir ./ETH/node --networkid 15 --port 30305 --nat extip:{0} --mine --unlock {1} --nodiscover'.format(self.ip, self.pubKey)
        else:
            print("[Script Output] Starting node...")
            command = 'geth --datadir ./ETH/node --networkid 15 --port 30305 --nat extip:{0} --nodiscover'.format(self.ip)
        threading.Thread(target=runNode, args=[command]).start()

        subprocess.run('cls', shell=True)

        #Initialize Enode
        if(not self.isGenesis):
            self.enode = input("[Script Output] Enode: ")

        #Initialize web3
        input('Press any key to start listening on P2P')
        self.web3 = Web3(Web3.IPCProvider())
        print("Web3 connected: ", self.web3.isConnected())
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        #Initialize contract
        if(not self.isGenesis):
            #Get contract address to interface with
            contractAddress = input("Contract Address: ")

            #Initialize contract Abi
            abi = json.loads('[{"inputs":[{"internalType":"uint256","name":"total","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"accountAddress","type":"address"},{"indexed":false,"internalType":"bool","name":"isChunk","type":"bool"},{"indexed":false,"internalType":"string","name":"senderGUID","type":"string"},{"indexed":false,"internalType":"string","name":"receiverGUID","type":"string"},{"indexed":false,"internalType":"string","name":"chunkHash","type":"string"},{"indexed":false,"internalType":"string","name":"linkToOGF","type":"string"}],"name":"logUpload","type":"event"},{"inputs":[],"name":"enroll","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"giveOmnies","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"myBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bool","name":"isChunk","type":"bool"},{"internalType":"string","name":"senderGUID","type":"string"},{"internalType":"string","name":"receiverGUID","type":"string"},{"internalType":"string","name":"chunkHash","type":"string"},{"internalType":"string","name":"linkToOGF","type":"string"}],"name":"uploadFile","outputs":[],"stateMutability":"nonpayable","type":"function"}]')

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
    def sendETH(self,puk):
    #-----------------------------------------------------------------------
        #Unlock account
        prefixed = [filename for filename in listdir('./ETH/node/keystore/') if filename.startswith("UTC")]
        with open('./ETH/node/keystore/{0}'.format(prefixed[0])) as keyfile:
            encrypted_key = keyfile.read()
            private_key = self.web3.eth.account.decrypt(encrypted_key, '123')

        #Set up transaction to receive ether
        nonce = self.web3.eth.getTransactionCount(self.pubKey)
        tx = {
            'nonce': nonce,
            'to': puk,
            'value': self.web3.toWei(100, 'ether'),
            'gas': 200000,
            'gasPrice': self.web3.toWei('50', 'gwei')
        }

        #Sign and send transaction
        signed_tx = self.web3.eth.account.signTransaction(tx, private_key)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print("Tx hash: ", self.web3.toHex(tx_hash))
        print('Sent eth')
    

    #-----------------------------------------------------------------------
    def enroll(self):
    #-----------------------------------------------------------------------
        try:
            tx_hash = self.contract.functions.enroll().transact()
            tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)

            #Print balance
            print("Omnies Balance: ", self.contract.functions.myBalance().call())

        except:
            print("Already enrolled.")

    #-----------------------------------------------------------------------
    def upload(self, isChunk, senderGUID, receiverGUID, chunkHash, linkToOGF):
    #-----------------------------------------------------------------------
        #Transact with smart contract that chunk has been uploaded
        print("[Script Output] Transacting chunk...")

        #Call Upload file
        tx_hash = self.contract.functions.uploadFile(isChunk, senderGUID, receiverGUID, chunkHash, linkToOGF).transact()
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)

        #Print balance
        print("Omnies Balance: ", self.contract.functions.myBalance().call())

    #-----------------------------------------------------------------------
    def retreive(self):
    #-----------------------------------------------------------------------
        #Read upload events
        event_filter = self.contract.events.logUpload.createFilter(fromBlock=0)
        for event in event_filter.get_all_entries():
            receipt = self.web3.eth.getTransactionReceipt(event['transactionHash']) #Get the transaction receipt
            result = self.contract.events.logUpload().processReceipt(receipt) #Process receipt data from hex

            print("isChunk: ", result[0]['args']['isChunk'])
            print("SenderGUID: ", result[0]['args']['senderGUID'])
            print("receiverGUID: ", result[0]['args']['receiverGUID'])
            print("chunkHash: ", result[0]['args']['chunkHash'])
            print("linkToOGF: ", result[0]['args']['linkToOGF'])