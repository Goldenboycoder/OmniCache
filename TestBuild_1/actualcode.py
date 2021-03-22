#-------------------Useful Code---------------#

geth attach ipc:\\.\pipe\geth.ipc

contractInterface.at(publishedContractAddr).totalSupply()

print(contract.functions.enroll().call())
print(contract.functions.myBalance().call())

web3.fromWei(eth.getBalance(eth.accounts[0]), "ether")

personal.unlockAccount(eth.accounts[0])

publishedContractAddr = "0x17f25af90872401f45e92291011941f16acd422b"

contract = contractInterface.at(publishedContractAddr)


#-------------------Deploying smart contract---------------#


#Contract Abi
abi = [{"inputs":[{"internalType":"uint256","name":"total","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"accountAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"LogStashiesSent","type":"event"},{"inputs":[],"name":"enroll","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"giveStashies","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"myBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"spendStashies","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]

#Contract Bytecode
bytecode = "0x608060405234801561001057600080fd5b506040516106563803806106568339818101604052602081101561003357600080fd5b8101908080519060200190929190505050806003819055506003546000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208190555033600260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050610575806100e16000396000f3fe608060405234801561001057600080fd5b50600436106100625760003560e01c806313ef6b751461006757806318160ddd146100855780638da5cb5b146100a3578063b0860bbe146100d7578063c9116b6914610119578063e65f2a7e14610137575b600080fd5b61006f610155565b6040518082815260200191505060405180910390f35b61008d61027e565b6040518082815260200191505060405180910390f35b6100ab610288565b604051808273ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b610103600480360360208110156100ed57600080fd5b81019080803590602001909291905050506102ae565b6040518082815260200191505060405180910390f35b610121610389565b6040518082815260200191505060405180910390f35b61013f6103cf565b6040518082815260200191505060405180910390f35b60006101a9600a6000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205461050c90919063ffffffff16565b6000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055503373ffffffffffffffffffffffffffffffffffffffff167f24cf573c534d748a3dd5523a44f0e84170de5094077bf284871a13271a371dd4600a6040518082815260200191505060405180910390a26000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054905090565b6000600354905090565b600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6000610301826000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205461052890919063ffffffff16565b6000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055506000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020549050919050565b60008060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054905090565b6000801515600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff1615151461042d57600080fd5b60146000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208190555060018060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff0219169083151502179055506000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054905090565b60008082840190508381101561051e57fe5b8091505092915050565b60008282111561053457fe5b81830390509291505056fea2646970667358221220679a04014c09db27b056443f7263dba5695c87ae944f50384e9ec7f8ed8602d964736f6c634300060c0033"

web3.eth.defaultAccount = web3.eth.accounts[0];

contractInterface = eth.contract(abi)

contractTx = contractInterface.new(9999999999999999,{from: eth.accounts[0],data: bytecode,gas: 300000})


contractHash = contractTx.transactionHash

publishedContractAddr = eth.getTransactionReceipt(contractHash).contractAddress

contract = contractInterface.at(publishedContractAddr)


#-------------------Calling smart contract functions---------------#

print(contract.functions.enroll().call())
print(contract.functions.myBalance().call())



#------------------------------Events------------------------------#
event Transfer(address indexed from, address indexed to, uint256 value);
emit ValueChanged(count - 1, count);


#------------------------------Filtering---------------------------#
event_signature_transfer = web3.Web3.sha3(text='Transfer(address,address,uint256)')
event_filter = w3.eth.filter({'topics': [event_signature_transfer]})
transfer_events = w3.eth.getFilterChanges(event_filter.filter_id)

# ... do something ...

new_transfer_events = w3.eth.getFilterChanges(event_filter.filter_id)