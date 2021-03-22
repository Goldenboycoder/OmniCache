import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
import time
import threading

#Initialize web3
web3 = Web3(Web3.IPCProvider())
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

#Get contract address to interface with
contractAddress = input("Contract Address: ")

#Contract Abi
abi = json.loads('[{"inputs":[{"internalType":"uint256","name":"total","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"accountAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"LogStashiesSent","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"accountAddress","type":"address"},{"indexed":false,"internalType":"bytes32","name":"hash","type":"bytes32"}],"name":"UploadFile","type":"event"},{"inputs":[],"name":"enroll","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"giveStashies","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"myBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"spendStashies","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]')

#Initialize contract object
contract = web3.eth.contract(address=contractAddress, abi=abi)

#Initialize Account
web3.eth.defaultAccount = web3.eth.accounts[0]

#Call contract functions
try:
	tx_hash = contract.functions.enroll().transact()
	tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
except:
	print("Already enrolled. Giving stashies..")
	tx_hash = contract.functions.giveStashies().transact()
	tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

print(contract.functions.myBalance().call())

#Read enrollment events
event_filter = contract.events.UploadFile.createFilter(fromBlock=0)
for event in event_filter.get_all_entries():
	receipt = web3.eth.getTransactionReceipt(event['transactionHash']) #Get the transaction receipt
	result = contract.events.UploadFile().processReceipt(receipt) #Process receipt data from hex
	print(result[0]['args']['hash'].decode('utf-8'))


#Read givestashies events
event_filter = contract.events.LogStashiesSent.createFilter(fromBlock=0)
for event in event_filter.get_all_entries():
	receipt = web3.eth.getTransactionReceipt(event['transactionHash']) #Get the transaction receipt
	result = contract.events.LogStashiesSent().processReceipt(receipt) #Process receipt data from hex
	print(result[0]['args']['amount'])