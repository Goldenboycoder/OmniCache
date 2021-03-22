import json
from web3 import Web3
from web3 import geth
from web3.middleware import geth_poa_middleware

#Connect to node
web3 = Web3(Web3.IPCProvider())

print(web3.isConnected())

web3.middleware_onion.inject(geth_poa_middleware, layer=0)

web3.eth.defaultAccount = web3.eth.accounts[0];
web3.geth.personal.unlock_account(web3.eth.accounts[0], "123",5)

#Contract Abi
abi = json.loads('[{"inputs":[{"internalType":"uint256","name":"total","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"accountAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"LogStashiesSent","type":"event"},{"inputs":[],"name":"enroll","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"giveStashies","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"myBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"spendStashies","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]')


#deploy contract

bytecode = "608060405234801561001057600080fd5b506040516106563803806106568339818101604052602081101561003357600080fd5b8101908080519060200190929190505050806003819055506003546000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208190555033600260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050610575806100e16000396000f3fe608060405234801561001057600080fd5b50600436106100625760003560e01c806313ef6b751461006757806318160ddd146100855780638da5cb5b146100a3578063b0860bbe146100d7578063c9116b6914610119578063e65f2a7e14610137575b600080fd5b61006f610155565b6040518082815260200191505060405180910390f35b61008d61027e565b6040518082815260200191505060405180910390f35b6100ab610288565b604051808273ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b610103600480360360208110156100ed57600080fd5b81019080803590602001909291905050506102ae565b6040518082815260200191505060405180910390f35b610121610389565b6040518082815260200191505060405180910390f35b61013f6103cf565b6040518082815260200191505060405180910390f35b60006101a9600a6000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205461050c90919063ffffffff16565b6000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055503373ffffffffffffffffffffffffffffffffffffffff167f24cf573c534d748a3dd5523a44f0e84170de5094077bf284871a13271a371dd4600a6040518082815260200191505060405180910390a26000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054905090565b6000600354905090565b600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6000610301826000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205461052890919063ffffffff16565b6000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055506000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020549050919050565b60008060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054905090565b6000801515600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff1615151461042d57600080fd5b60146000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208190555060018060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff0219169083151502179055506000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054905090565b60008082840190508381101561051e57fe5b8091505092915050565b60008282111561053457fe5b81830390509291505056fea2646970667358221220679a04014c09db27b056443f7263dba5695c87ae944f50384e9ec7f8ed8602d964736f6c634300060c0033"

contract = web3.eth.contract(abi=abi, bytecode=bytecode)

tx_hash = contract.constructor(9999999).transact()

tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

contract = web3.eth.contract(
	address=tx_receipt.contractAddress,
	abi=abi
)

# print(contract.address)

# tx_hash = contract.functions.enroll().transact()
# tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

# print(contract.functions.myBalance().call())


#use deployed contract

# address = "0x13701f0EAF10AB344Ce96243B8d0B37D3604b3B9"

# contract = web3.eth.contract(address=address, abi=abi)

# print(contract.address)


# tx_hash = contract.functions.giveStashies().transact()

# tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)


# print(contract.functions.myBalance().call())