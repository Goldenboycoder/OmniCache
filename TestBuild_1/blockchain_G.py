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
    def __init__(self, ip):
    #-----------------------------------------------------------------------
        self.pubKey = ''
        self.enode = ''
        self.web3 = ''
        self.ip = ip
        self.contract = None
        self.initBlockchainNode()

    #-====================================Initializing the Blockchain======================================

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
        print("[Script Output] Starting genesis node... Please enter the node's password when terminal opens.")
        command = 'geth --datadir ./ETH/node --networkid 15 --port 30305 --nat extip:{0} --mine --unlock {1} --nodiscover'.format(self.ip, self.pubKey)

        threading.Thread(target=runNode, args=[command]).start()

        subprocess.run('cls', shell=True)

        #Initialize web3
        input('Press any key to start listening on P2P')
        self.web3 = Web3(Web3.IPCProvider())
        print("Web3 connected: ", self.web3.isConnected())
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        #Deploy Contract

        #Contract Abi
        abi = json.loads('[{"inputs":[{"internalType":"uint256","name":"total","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"accountAddress","type":"address"},{"indexed":false,"internalType":"bool","name":"isChunk","type":"bool"},{"indexed":false,"internalType":"string","name":"senderGUID","type":"string"},{"indexed":false,"internalType":"string","name":"receiverGUID","type":"string"},{"indexed":false,"internalType":"string","name":"chunkHash","type":"string"},{"indexed":false,"internalType":"string","name":"linkToOGF","type":"string"}],"name":"logUpload","type":"event"},{"inputs":[],"name":"enroll","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"giveOmnies","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"myBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bool","name":"isChunk","type":"bool"},{"internalType":"string","name":"senderGUID","type":"string"},{"internalType":"string","name":"receiverGUID","type":"string"},{"internalType":"string","name":"chunkHash","type":"string"},{"internalType":"string","name":"linkToOGF","type":"string"}],"name":"uploadFile","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
        #Contract BytecodecontractInterface new web3.py
        bytecode = "608060405234801561001057600080fd5b50604051610a16380380610a168339818101604052602081101561003357600080fd5b8101908080519060200190929190505050806003819055506003546000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208190555033600260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050610935806100e16000396000f3fe608060405234801561001057600080fd5b50600436106100625760003560e01c806318160ddd146100675780635e1bb33d1461008557806370114c25146100a35780638da5cb5b1461032f578063c9116b6914610363578063e65f2a7e14610381575b600080fd5b61006f61039f565b6040518082815260200191505060405180910390f35b61008d6103a9565b6040518082815260200191505060405180910390f35b61032d600480360360a08110156100b957600080fd5b81019080803515159060200190929190803590602001906401000000008111156100e257600080fd5b8201836020820111156100f457600080fd5b8035906020019184600183028401116401000000008311171561011657600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f8201169050808301925050505050505091929192908035906020019064010000000081111561017957600080fd5b82018360208201111561018b57600080fd5b803590602001918460018302840111640100000000831117156101ad57600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f8201169050808301925050505050505091929192908035906020019064010000000081111561021057600080fd5b82018360208201111561022257600080fd5b8035906020019184600183028401116401000000008311171561024457600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f820116905080830192505050505050509192919290803590602001906401000000008111156102a757600080fd5b8201836020820111156102b957600080fd5b803590602001918460018302840111640100000000831117156102db57600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f820116905080830192505050505050509192919290505050610483565b005b610337610722565b604051808273ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b61036b610748565b6040518082815260200191505060405180910390f35b61038961078e565b6040518082815260200191505060405180910390f35b6000600354905090565b60006103fd600a6000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020546108cc90919063ffffffff16565b6000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055506000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054905090565b3373ffffffffffffffffffffffffffffffffffffffff167f52f4703559b7ca5c8b998a7433378acb097298909785f201ffb2f0c563dec6d8868686868660405180861515815260200180602001806020018060200180602001858103855289818151815260200191508051906020019080838360005b838110156105145780820151818401526020810190506104f9565b50505050905090810190601f1680156105415780820380516001836020036101000a031916815260200191505b50858103845288818151815260200191508051906020019080838360005b8381101561057a57808201518184015260208101905061055f565b50505050905090810190601f1680156105a75780820380516001836020036101000a031916815260200191505b50858103835287818151815260200191508051906020019080838360005b838110156105e05780820151818401526020810190506105c5565b50505050905090810190601f16801561060d5780820380516001836020036101000a031916815260200191505b50858103825286818151815260200191508051906020019080838360005b8381101561064657808201518184015260208101905061062b565b50505050905090810190601f1680156106735780820380516001836020036101000a031916815260200191505b50995050505050505050505060405180910390a26106d960016000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020546108e890919063ffffffff16565b6000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055505050505050565b600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60008060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054905090565b6000801515600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff161515146107ec57600080fd5b6113886000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208190555060018060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff0219169083151502179055506000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054905090565b6000808284019050838110156108de57fe5b8091505092915050565b6000828211156108f457fe5b81830390509291505056fea2646970667358221220a66dd36ae8987b488b50128fe7521e1b846dfe7f4b41b194aca49f3274eafc1764736f6c634300060c0033"
        web3.eth.defaultAccount = web3.eth.accounts[0];

        contractInterface = web3.eth.contract(abi=abi, bytecode=bytecode) #Initialize the contract object
        tx_hash =  contractInterface.constructor(99999999999999).transact() #Deploy the contract
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash) #Retreive the receipt
        print(tx_receipt.contractAddress) #Return the contract address using the receipt
        
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