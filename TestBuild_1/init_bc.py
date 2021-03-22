import subprocess
import json
import sys
import threading
from os import path

subprocess.run('cls', shell=True)
print("Node Setup v1.0")
print("\t1- Initialize node")
print("\t2- Start node")

menuDo = input("Choose option: ")

#Change dataPath
dataPath =  "C:/Stash-it/"
print("[Script Output] Default dataPath for the data directories is: {0}".format(dataPath))
changePath = input("[Script Output] Change default dataPath? (y/n): ")
if(changePath == 'y'):
	dataPath = input("[Script Output] Enter a new dataPath: ")
	print("[Script Output] New dataPath: {0}".format(dataPath))
elif(changePath != 'n'):
	sys.exit("[Script Output] Invalid Input..")

if(menuDo == '1'):
	#Detect data directories
	if(path.exists("{0}".format(dataPath))):
		print("[Script Output] Detected data directory")
		delete = input("[Script Output] Delete existing data directory? (y/n): ")
		if(delete == 'y'):
			command = 'rmdir /q /s "{0}"'.format(dataPath)
			res = subprocess.run(command, shell=True).returncode
			if(res != 0):
				sys.exit("[Script Output] Could not delete files.")
			else:
				print("[Script Output] Data directory deleted...")
		else:
			sys.exit("[Script Output] Aborting...")
	#Create Accounts
	print("[Script Output] Creating account...")
	print("[Script Output] Please save the public key.")
	command = 'geth account new --datadir {0}node'.format(dataPath)
	subprocess.run(command, shell=True)

	nodeGAddr = input("[Script Output] Enter the PK belonging to the gensis node: ")


	#Creating genesis.json
	genesisJson = json.dumps({"config":{"chainId":15,"homesteadBlock":0,"eip150Block":0,"eip155Block":0,"eip158Block":0,"byzantiumBlock":0,"constantinopleBlock":0,"petersburgBlock":0,"clique":{"period":5,"epoch":30000}},"difficulty":"1","gasLimit":"8000000","extradata":"0x{0}{1}{2}".format(64 * '0', nodeGAddr[2:], 130 * '0'),"alloc":{"{0}".format(nodeGAddr[2:]):{"balance":"3000000000000000000000"}}}, indent=4)
	with open("{0}genesis.json".format(dataPath),"w") as genesisFile :
		genesisFile.write(genesisJson)


	#Initializing nodes
	print("[Script Output] Initializing Node...")
	command = 'geth init --datadir {0}node {0}genesis.json'.format(dataPath)
	init = subprocess.run(command, shell=True).returncode

	#If initialization failed for one of the nodes then abort
	if(init != 0):
		sys.exit("[Script Output] Initialization failed. Aborting..")

else:
	nodeGAddr = input("[Script Output] Enter nodeG's public key: ")

def func(command):
	subprocess.run(command, creationflags=subprocess.CREATE_NEW_CONSOLE)

#Run node
print("[Script Output] Starting node..\n")
command = 'geth --datadir {0}node --networkid 15 --port 30305 --nodiscover console --ipcdisable'.format(dataPath)
threading.Thread(target=func, args=[command]).start()
