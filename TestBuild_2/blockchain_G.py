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
from pathlib import Path

class bcNode:
    #-----------------------------------------------------------------------
    def __init__(self, ip):
    #-----------------------------------------------------------------------
        self.pubKey = ''
        self.enode = ''
        self.web3 = ''
        self.ip = ip
        self.contract = None
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
            #import os
            #os.remove("tmpPass")

            #Read public keys
            keyFiles = [filename for filename in listdir('./ETH/node/keystore/') if filename.startswith("UTC")]

            #Set PubKey
            self.pubKey = "0x" + keyFiles[0].split("--")[2]

            #Create genesis.json
            genesisJson = json.dumps({"config":{"chainId":15,"homesteadBlock":0,"eip150Block":0,"eip155Block":0,"eip158Block":0,"byzantiumBlock":0,"constantinopleBlock":0,"petersburgBlock":0,"clique":{"period":5,"epoch":30000}},"difficulty":"1","gasLimit":"8000000","extradata":"0x{0}{1}{2}".format(64 * '0', self.pubKey[2:], 130 * '0'),"alloc":{"{0}".format(self.pubKey[2:]):{"balance":"3000000000000000000000"}}}, indent=4)
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
        print("[Script Output] Starting genesis node... Please enter the node's password when terminal opens.")
        command = 'geth --datadir ./ETH/node --cache=2048 --networkid 15 --port 30305 --nat extip:{0} --mine --unlock {1} --nodiscover --password {2}'.format(self.ip, self.pubKey, "tmpPass")

        threading.Thread(target=runNode, args=[command]).start()

        subprocess.run('cls', shell=True)

        #Initialize web3
        time.sleep(3)
        self.web3 = Web3(Web3.IPCProvider())
        print("Web3 connected: ", self.web3.isConnected())
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        #Make pubKey checksum
        self.pubKey = self.web3.toChecksumAddress(self.pubKey)

        #Deploy Contract
        #Contract Abi
        abi = json.loads('[{"inputs":[{"internalType":"uint256","name":"total","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"accountAddress","type":"address"},{"indexed":true,"internalType":"int128","name":"linkToOGF","type":"int128"},{"indexed":false,"internalType":"int256","name":"senderGUID","type":"int256"},{"indexed":true,"internalType":"int256","name":"receiverGUID","type":"int256"},{"indexed":false,"internalType":"string","name":"chunkHash","type":"string"},{"indexed":false,"internalType":"int256","name":"chunkNb","type":"int256"}],"name":"logChunk","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"accountAddress","type":"address"},{"indexed":true,"internalType":"int128","name":"linkToOGF","type":"int128"}],"name":"logDeletion","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"accountAddress","type":"address"},{"indexed":false,"internalType":"int128","name":"linkToOGF","type":"int128"},{"indexed":false,"internalType":"string","name":"fileName","type":"string"},{"indexed":false,"internalType":"string","name":"fileHash","type":"string"},{"indexed":false,"internalType":"int256","name":"totalSize","type":"int256"}],"name":"logFile","type":"event"},{"inputs":[{"internalType":"int128","name":"linkToOGF","type":"int128"}],"name":"deleteFile","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"enroll","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"giveOmnies","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"myBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"int128","name":"linkToOGF","type":"int128"},{"internalType":"int256","name":"senderGUID","type":"int256"},{"internalType":"int256","name":"receiverGUID","type":"int256"},{"internalType":"string","name":"chunkHash","type":"string"},{"internalType":"int256","name":"chunkNb","type":"int256"}],"name":"uploadChunk","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"int128","name":"linkToOGF","type":"int128"},{"internalType":"string","name":"fileName","type":"string"},{"internalType":"string","name":"fileHash","type":"string"},{"internalType":"int256","name":"totalSize","type":"int256"}],"name":"uploadFile","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
        bytecode = "608060405234801561001057600080fd5b50604051610a77380380610a778339818101604052602081101561003357600080fd5b8101908080519060200190929190505050806003819055506003546000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208190555033600260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050610996806100e16000396000f3fe608060405234801561001057600080fd5b50600436106100885760003560e01c8063785cb1791161005b578063785cb179146103185780638da5cb5b14610349578063c9116b691461037d578063e65f2a7e1461039b57610088565b806318160ddd1461008d5780635e1bb33d146100ab57806360956555146100c95780636a40c414146101af575b600080fd5b6100956103b9565b6040518082815260200191505060405180910390f35b6100b36103c3565b6040518082815260200191505060405180910390f35b6101ad600480360360a08110156100df57600080fd5b810190808035600f0b906020019092919080359060200190929190803590602001909291908035906020019064010000000081111561011d57600080fd5b82018360208201111561012f57600080fd5b8035906020019184600183028401116401000000008311171561015157600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f8201169050808301925050505050505091929192908035906020019092919050505061049d565b005b610316600480360360808110156101c557600080fd5b810190808035600f0b9060200190929190803590602001906401000000008111156101ef57600080fd5b82018360208201111561020157600080fd5b8035906020019184600183028401116401000000008311171561022357600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f8201169050808301925050505050505091929192908035906020019064010000000081111561028657600080fd5b82018360208201111561029857600080fd5b803590602001918460018302840111640100000000831117156102ba57600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f8201169050808301925050505050505091929192908035906020019092919050505061056c565b005b6103476004803603602081101561032e57600080fd5b810190808035600f0b9060200190929190505050610739565b005b610351610783565b604051808273ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b6103856107a9565b6040518082815260200191505060405180910390f35b6103a36107ef565b6040518082815260200191505060405180910390f35b6000600354905090565b6000610417600a6000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205461092d90919063ffffffff16565b6000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055506000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054905090565b8285600f0b3373ffffffffffffffffffffffffffffffffffffffff167f0ca4b706f504c3506adce721b4b2976cb39c3e54e2424bd734d5c52f115c5f228786866040518084815260200180602001838152602001828103825284818151815260200191508051906020019080838360005b8381101561052957808201518184015260208101905061050e565b50505050905090810190601f1680156105565780820380516001836020036101000a031916815260200191505b5094505050505060405180910390a45050505050565b3373ffffffffffffffffffffffffffffffffffffffff167fc34e9c0afb2f46e02128a2451e87f4d532f3a616d5f0fcfcebbc0895cb13dda2858585856040518085600f0b81526020018060200180602001848152602001838103835286818151815260200191508051906020019080838360005b838110156105fb5780820151818401526020810190506105e0565b50505050905090810190601f1680156106285780820380516001836020036101000a031916815260200191505b50838103825285818151815260200191508051906020019080838360005b83811015610661578082015181840152602081019050610646565b50505050905090810190601f16801561068e5780820380516001836020036101000a031916815260200191505b50965050505050505060405180910390a26106f160326000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205461094990919063ffffffff16565b6000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208190555050505050565b80600f0b3373ffffffffffffffffffffffffffffffffffffffff167fd100f861f50fed75d4470f6006981223ade513e4321b4039b3661eabd7b0b7ab60405160405180910390a350565b600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60008060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054905090565b6000801515600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff1615151461084d57600080fd5b6113886000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208190555060018060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff0219169083151502179055506000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054905090565b60008082840190508381101561093f57fe5b8091505092915050565b60008282111561095557fe5b81830390509291505056fea264697066735822122011aba844c77b8c5f90f94b86f3ab22a9230b1a14b80b949de0edf21dcc57495364736f6c634300060c0033"
        self.web3.eth.defaultAccount = self.web3.eth.accounts[0]

        contractInterface = self.web3.eth.contract(abi=abi, bytecode=bytecode) #Initialize the contract object
        tx_hash =  contractInterface.constructor(99999999999999).transact() #Deploy the contract
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash) #Retreive the receipt
        print("Contract Address:",tx_receipt.contractAddress) #Return the contract address using the receipt
        
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
            'chainId': 15,
            'nonce': nonce,
            'to': puk,
            'value': self.web3.toWei(100, 'ether'),
            'gas': 200000,
            'gasPrice': self.web3.toWei(50, 'gwei')
        }

        #Sign and send transaction
        signed_tx = self.web3.eth.account.signTransaction(tx, private_key)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print("Tx hash: ", self.web3.toHex(tx_hash))
        print('Sent eth')