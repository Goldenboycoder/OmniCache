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

        #Deploy Contract
        #Contract Abi
        abi = json.loads('[{"inputs":[{"internalType":"uint256","name":"total","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"accountAddress","type":"address"},{"indexed":true,"internalType":"string","name":"linkToOGF","type":"string"},{"indexed":false,"internalType":"string","name":"senderGUID","type":"string"},{"indexed":false,"internalType":"string","name":"receiverGUID","type":"string"},{"indexed":false,"internalType":"string","name":"chunkHash","type":"string"},{"indexed":false,"internalType":"int256","name":"chunkNb","type":"int256"}],"name":"logChunk","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"accountAddress","type":"address"},{"indexed":true,"internalType":"string","name":"linkToOGF","type":"string"}],"name":"logDeletion","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"accountAddress","type":"address"},{"indexed":false,"internalType":"string","name":"fileName","type":"string"},{"indexed":false,"internalType":"string","name":"fileHash","type":"string"},{"indexed":false,"internalType":"string","name":"linkToOGF","type":"string"},{"indexed":false,"internalType":"int256","name":"totalSize","type":"int256"}],"name":"logFile","type":"event"},{"inputs":[{"internalType":"string","name":"linkToOGF","type":"string"}],"name":"deleteFile","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"enroll","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"giveOmnies","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"myBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"linkToOGF","type":"string"},{"internalType":"string","name":"senderGUID","type":"string"},{"internalType":"string","name":"receiverGUID","type":"string"},{"internalType":"string","name":"chunkHash","type":"string"},{"internalType":"int256","name":"chunkNb","type":"int256"}],"name":"uploadChunk","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"fileName","type":"string"},{"internalType":"string","name":"fileHash","type":"string"},{"internalType":"string","name":"linkToOGF","type":"string"},{"internalType":"int256","name":"totalSize","type":"int256"}],"name":"uploadFile","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
        bytecode = "608060405234801561001057600080fd5b50604051610f1c380380610f1c8339818101604052602081101561003357600080fd5b8101908080519060200190929190505050806003819055506003546000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208190555033600260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050610e3b806100e16000396000f3fe608060405234801561001057600080fd5b50600436106100885760003560e01c80638da5cb5b1161005b5780638da5cb5b14610546578063a99100541461057a578063c9116b6914610635578063e65f2a7e1461065357610088565b806318160ddd1461008d578063271cc533146100ab5780634a6e9bb1146103355780635e1bb33d14610528575b600080fd5b610095610671565b6040518082815260200191505060405180910390f35b610333600480360360a08110156100c157600080fd5b81019080803590602001906401000000008111156100de57600080fd5b8201836020820111156100f057600080fd5b8035906020019184600183028401116401000000008311171561011257600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f8201169050808301925050505050505091929192908035906020019064010000000081111561017557600080fd5b82018360208201111561018757600080fd5b803590602001918460018302840111640100000000831117156101a957600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f8201169050808301925050505050505091929192908035906020019064010000000081111561020c57600080fd5b82018360208201111561021e57600080fd5b8035906020019184600183028401116401000000008311171561024057600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f820116905080830192505050505050509192919290803590602001906401000000008111156102a357600080fd5b8201836020820111156102b557600080fd5b803590602001918460018302840111640100000000831117156102d757600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f8201169050808301925050505050505091929192908035906020019092919050505061067b565b005b6105266004803603608081101561034b57600080fd5b810190808035906020019064010000000081111561036857600080fd5b82018360208201111561037a57600080fd5b8035906020019184600183028401116401000000008311171561039c57600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f820116905080830192505050505050509192919290803590602001906401000000008111156103ff57600080fd5b82018360208201111561041157600080fd5b8035906020019184600183028401116401000000008311171561043357600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f8201169050808301925050505050505091929192908035906020019064010000000081111561049657600080fd5b8201836020820111156104a857600080fd5b803590602001918460018302840111640100000000831117156104ca57600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f82011690508083019250505050505050919291929080359060200190929190505050610878565b005b610530610aa7565b6040518082815260200191505060405180910390f35b61054e610b81565b604051808273ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b6106336004803603602081101561059057600080fd5b81019080803590602001906401000000008111156105ad57600080fd5b8201836020820111156105bf57600080fd5b803590602001918460018302840111640100000000831117156105e157600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f820116905080830192505050505050509192919290505050610ba7565b005b61063d610c4e565b6040518082815260200191505060405180910390f35b61065b610c94565b6040518082815260200191505060405180910390f35b6000600354905090565b846040518082805190602001908083835b602083106106af578051825260208201915060208101905060208303925061068c565b6001836020036101000a03801982511681845116808217855250505050505090500191505060405180910390203373ffffffffffffffffffffffffffffffffffffffff167f60c47c7f80bea4ee9ea7310b399f134aa1c7d421ae69c7b6d29cda9e4f750e568686868660405180806020018060200180602001858152602001848103845288818151815260200191508051906020019080838360005b8381101561076657808201518184015260208101905061074b565b50505050905090810190601f1680156107935780820380516001836020036101000a031916815260200191505b50848103835287818151815260200191508051906020019080838360005b838110156107cc5780820151818401526020810190506107b1565b50505050905090810190601f1680156107f95780820380516001836020036101000a031916815260200191505b50848103825286818151815260200191508051906020019080838360005b83811015610832578082015181840152602081019050610817565b50505050905090810190601f16801561085f5780820380516001836020036101000a031916815260200191505b5097505050505050505060405180910390a35050505050565b3373ffffffffffffffffffffffffffffffffffffffff167f9ae14a749161159202b70e30bd44852520b17ca112f0649cc8cb2b10901dd7418585858560405180806020018060200180602001858152602001848103845288818151815260200191508051906020019080838360005b838110156109025780820151818401526020810190506108e7565b50505050905090810190601f16801561092f5780820380516001836020036101000a031916815260200191505b50848103835287818151815260200191508051906020019080838360005b8381101561096857808201518184015260208101905061094d565b50505050905090810190601f1680156109955780820380516001836020036101000a031916815260200191505b50848103825286818151815260200191508051906020019080838360005b838110156109ce5780820151818401526020810190506109b3565b50505050905090810190601f1680156109fb5780820380516001836020036101000a031916815260200191505b5097505050505050505060405180910390a2610a5f60326000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054610dd290919063ffffffff16565b6000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208190555050505050565b6000610afb600a6000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054610de990919063ffffffff16565b6000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055506000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054905090565b600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b806040518082805190602001908083835b60208310610bdb5780518252602082019150602081019050602083039250610bb8565b6001836020036101000a03801982511681845116808217855250505050505090500191505060405180910390203373ffffffffffffffffffffffffffffffffffffffff167f4c1374fa2d7d5df60a17a74110d0fa34208cb6119ed98dd3f1481db20ac5cb9d60405160405180910390a350565b60008060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054905090565b6000801515600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff16151514610cf257600080fd5b6113886000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208190555060018060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff0219169083151502179055506000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054905090565b600082821115610dde57fe5b818303905092915050565b600080828401905083811015610dfb57fe5b809150509291505056fea26469706673582212209f0f9d65e45eb53acea52c0efc573682c8adad4a41e94eac0d7f33b26d923f1764736f6c634300060c0033"
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
            'gasPrice': self.web3.toWei('50', 'gwei')
        }

        #Sign and send transaction
        signed_tx = self.web3.eth.account.signTransaction(tx, private_key)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print("Tx hash: ", self.web3.toHex(tx_hash))
        print('Sent eth')