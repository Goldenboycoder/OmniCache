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
        self.web3 = ''
        self.ip = ip
        self.txNonceCount = 0
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
            Path("./logs").mkdir(exist_ok=True)
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
        command = 'geth --datadir ./ETH/node --syncmode=full --cache=2048 --networkid 15 --port 30305 --nat extip:{0} --mine --unlock {1} --nodiscover --password {2}'.format(self.ip, self.pubKey, "tmpPass")

        threading.Thread(target=runNode, args=[command]).start()

        subprocess.run('cls', shell=True)

        #Initialize web3
        print("Connecting to web3..")
        while True:
            self.web3 = Web3(Web3.IPCProvider())
            if self.web3.isConnected():
                self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
                if self.web3.geth.personal.list_wallets()[0]['status'] == "Unlocked":
                    print("Web3 connected. ", self.web3.isConnected())
                    break

        #Make pubKey checksum
        self.pubKey = self.web3.toChecksumAddress(self.pubKey)

        #Deploy Contract
        #Contract Abi
        abi = json.loads('[{"inputs":[{"internalType":"uint256","name":"total","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"accountAddress","type":"address"},{"indexed":true,"internalType":"int256","name":"linkToOGF","type":"int256"},{"indexed":false,"internalType":"int256","name":"senderGUID","type":"int256"},{"indexed":true,"internalType":"int256","name":"receiverGUID","type":"int256"},{"indexed":false,"internalType":"string","name":"chunkHash","type":"string"},{"indexed":false,"internalType":"int256","name":"chunkNb","type":"int256"}],"name":"logChunk","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"accountAddress","type":"address"},{"indexed":true,"internalType":"int256","name":"linkToOGF","type":"int256"}],"name":"logDeletion","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"accountAddress","type":"address"},{"indexed":false,"internalType":"int256","name":"linkToOGF","type":"int256"},{"indexed":false,"internalType":"string","name":"fileName","type":"string"},{"indexed":false,"internalType":"string","name":"fileHash","type":"string"},{"indexed":false,"internalType":"int256","name":"totalSize","type":"int256"}],"name":"logFile","type":"event"},{"inputs":[{"internalType":"int256","name":"linkToOGF","type":"int256"}],"name":"deleteFile","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"enroll","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"giveOmnies","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"myBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"int256","name":"linkToOGF","type":"int256"},{"internalType":"int256","name":"senderGUID","type":"int256"},{"internalType":"int256","name":"receiverGUID","type":"int256"},{"internalType":"string","name":"chunkHash","type":"string"},{"internalType":"int256","name":"chunkNb","type":"int256"}],"name":"uploadChunk","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"int256","name":"linkToOGF","type":"int256"},{"internalType":"string","name":"fileName","type":"string"},{"internalType":"string","name":"fileHash","type":"string"},{"internalType":"int256","name":"totalSize","type":"int256"}],"name":"uploadFile","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
        bytecode = "608060405234801561001057600080fd5b50604051610a65380380610a658339818101604052602081101561003357600080fd5b8101908080519060200190929190505050806003819055506003546000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208190555033600260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050610984806100e16000396000f3fe608060405234801561001057600080fd5b50600436106100885760003560e01c8063985059a91161005b578063985059a914610263578063c9116b6914610346578063e65f2a7e14610364578063f02404f21461038257610088565b806318160ddd1461008d5780635e1bb33d146100ab57806372556805146100c95780638da5cb5b1461022f575b600080fd5b6100956103b0565b6040518082815260200191505060405180910390f35b6100b36103ba565b6040518082815260200191505060405180910390f35b61022d600480360360808110156100df57600080fd5b81019080803590602001909291908035906020019064010000000081111561010657600080fd5b82018360208201111561011857600080fd5b8035906020019184600183028401116401000000008311171561013a57600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f8201169050808301925050505050505091929192908035906020019064010000000081111561019d57600080fd5b8201836020820111156101af57600080fd5b803590602001918460018302840111640100000000831117156101d157600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f82011690508083019250505050505050919291929080359060200190929190505050610494565b005b61023761065e565b604051808273ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b610344600480360360a081101561027957600080fd5b81019080803590602001909291908035906020019092919080359060200190929190803590602001906401000000008111156102b457600080fd5b8201836020820111156102c657600080fd5b803590602001918460018302840111640100000000831117156102e857600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f82011690508083019250505050505050919291929080359060200190929190505050610684565b005b61034e610750565b6040518082815260200191505060405180910390f35b61036c610796565b6040518082815260200191505060405180910390f35b6103ae6004803603602081101561039857600080fd5b81019080803590602001909291905050506108d4565b005b6000600354905090565b600061040e600a6000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205461091b90919063ffffffff16565b6000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055506000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054905090565b3373ffffffffffffffffffffffffffffffffffffffff167ff4b85aff480ae00982e9651a2395f791ff773c3de995223c9f2a8717eba3661e85858585604051808581526020018060200180602001848152602001838103835286818151815260200191508051906020019080838360005b83811015610520578082015181840152602081019050610505565b50505050905090810190601f16801561054d5780820380516001836020036101000a031916815260200191505b50838103825285818151815260200191508051906020019080838360005b8381101561058657808201518184015260208101905061056b565b50505050905090810190601f1680156105b35780820380516001836020036101000a031916815260200191505b50965050505050505060405180910390a261061660326000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205461093790919063ffffffff16565b6000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208190555050505050565b600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b82853373ffffffffffffffffffffffffffffffffffffffff167f916bbccc00cde19c8479e05a1e232d9ed1dcc5f41bde371f0db01a278216b0448786866040518084815260200180602001838152602001828103825284818151815260200191508051906020019080838360005b8381101561070d5780820151818401526020810190506106f2565b50505050905090810190601f16801561073a5780820380516001836020036101000a031916815260200191505b5094505050505060405180910390a45050505050565b60008060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054905090565b6000801515600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff161515146107f457600080fd5b6113886000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208190555060018060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff0219169083151502179055506000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054905090565b803373ffffffffffffffffffffffffffffffffffffffff167fb25d3cd3fc81c089eb4207f4687721d48cd1d8d812b02fc86682b2178cbeef5460405160405180910390a350565b60008082840190508381101561092d57fe5b8091505092915050565b60008282111561094357fe5b81830390509291505056fea2646970667358221220ff533ece730d3e725c5eafd8693a5b977d64cd44e54da0a2161a864cfa135f1764736f6c634300060c0033"
        self.web3.eth.defaultAccount = self.web3.eth.accounts[0]

        contractInterface = self.web3.eth.contract(abi=abi, bytecode=bytecode) #Initialize the contract object
        tx_hash =  contractInterface.constructor(99999999999999).transact() #Deploy the contract
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash) #Retreive the receipt
        #print(self.web3.eth.get_balance(self.web3.pubKey));
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
        if(self.txNonceCount == 0):                #Initialize Nonce in case of restart
            self.txNonceCount = self.web3.eth.getTransactionCount(self.pubKey)

        nonce = self.txNonceCount
        

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
        try:
            tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)

            print("Status: ", tx_receipt['status'])


            #Check status of eth transaction
            if(tx_receipt['status'] == 1):
                print("Successfully sent ETH!")
                self.txNonceCount += 1
            else:
                print("ETH Tx sent, but status failed!")
                self.sendETH(puk)

        except:
            print("Error with sendETH tx! Retrying..")
            self.sendETH(puk)