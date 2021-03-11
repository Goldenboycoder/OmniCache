import socket
import uuid
import threading
import datetime
import time
import json
from pathlib import Path
from blockchain import bcNode

class Node:
    #-----------------------------------------------------------------------
    def __init__(self,myip,port,bNode,npeer=2,guid=None):
    #-----------------------------------------------------------------------
        self.bNode=bNode
        self.myip=myip
        self.port=port

        if guid:
            self.guid=guid
        else:
            print("guid was not provided, should be later on")
            self.guid=guid

        self.npeer=npeer #max number of peers

        self.peers={} #our routing table

        self.protocol={
            'JOIN':self.join,#JOIN code
            'UPFL':self.upfl,#UPFL code :  upload file 
            'AKFL':self.akfl,#Acknowledge file code
            'FUND':self.fund,#FUND code request to genesis to send eth when account is empty
            'ADPR':self.adpr,#ADPR code add peer when new peer joins
            'DEFS':self.defs,#DEFS code define self after getting id and table from genesis
            'ADBN':self.adbn}#ADBN code add blockchain node after gettting it's PK and Enode
        
        if self.bNode.isGenesis:
            self.lastid=0
            self.guid=self.lastid
        else:
            print("normal peer")

        self.startTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.turnoff=False

    #================================Protocols===============================================
    
    
    def join(self,peercon,data): #JOIN code
        ip, port = data.split('-')
        if self.bNode.isGenesis :
            #if this node is the genesis node send him eather and add him to table
            if not self.peerLimitReached() :
                self.addPeer(self.lastid+1,ip,int(port))
                self.lastid+=1
                #broadcast peer added
                tosend="-".join([str(self.lastid),ip,str(port)])
                self.broadcast("adpr",tosend,self.lastid)
                #send the joining node an id and routing table
                table=self.peers.copy()
                table[self.guid]=[self.myip,self.port]
                print(self.peers)
                table=json.dumps(table)
                tosend="-".join([str(self.lastid),self.bNode.pubKey,table]) #this wont work if table is big because recv 4096 bytes only
                # ! on the receiver side the keys will be of type Char
                self.connectAndSend(ip,int(port),'defs',tosend,pId=self.lastid,waitReply=False)
                

                #self.bNode.addToNet(enode)
                #self.bNode.sendETH(puk)
                self.logging("New peer {} joined the Network".format(self.lastid))
        else:
            try:
                peer=min(self.peers.keys())
                toforward=self.peers[peer]
                self.connectAndSend(toforward[0],toforward[1],"join",data,pId=peer,waitReply=False)
                self.logging("Forwarding a {} request to peer id = {}".format("JOIN",peer))
            except Exception as e:
                print(e)

        
    def adbn(self,peercon,data):
        pk , enode= data.split('-')
        if self.bNode.isGenesis :
            self.bNode.addToNet(enode)
            self.logging("added new peer to the blockchain network *") 
            self.bNode.sendETH(pk)
        else:
            self.bNode.addToNet(enode)
            self.logging("added new peer to the blockchain network")
            peer = min(self.peers.keys())
            toforward = self.peers[peer]
            self.connectAndSend(toforward[0],toforward[1],"adbn",data,pId=peer,waitReply=False)
            self.logging("Forwarding a {} request to peer id = {}".format("ADBN",peer))


    def upfl(self,peercon,data): # UPFL code :  upload file 
        pid , fileN = data.split('-')
        #after receiving the file
        ip , port = self.peers[int(pid)]
        self.connectAndSend(ip,port,'akfl','-'.join([str(self.guid),fileN]),int(pid),waitReply=False)
        self.logging("peer {} uploaded a file named : {}".format(pid,fileN))


    def akfl(self,peercon,data): # Acknowledge file code
        pid , fileN = data.split('-')
        print("got ACK for file named: ",fileN)
        self.logging("peer {} uploaded a file named : {}".format(pid,fileN))

    #not used in this scenario
    def fund(self,peercon,data): #FUND code request to genesis to send eth when account is empty
        pass


    def adpr(self,peercon,data): # ADPR code add peer when new peer joins
        pid , ip , port = data.split('-')
        self.addPeer(int(pid),ip,int(port))

    
    def defs(self,peercon,data): # DEFS code define self after getting id and table from genesis
        guid , genesisPK ,table = data.split('-')
        guid=int(guid)
        table=json.loads(table)
        self.setmyid(guid)
        for peer in table :
            if int(peer) != guid:
                self.peers[int(peer)]=table[peer]
        self.logging("Sucessfully defined as peerID = {} \n with table {}\n Genesis PK : {}".format(guid,table,genesisPK))
        self.bNode.initBlockchainNode(genesisPK=genesisPK)
        #at the end send an add blockchain node to network (ADBN) request
        peer=max(self.peers.keys())
        toforward=self.peers[peer]
        tosend='-'.join([self.bNode.pubKey,self.bNode.enode])
        self.connectAndSend(toforward[0],toforward[1],"adbn",tosend,pId=peer,waitReply=False)


    #========================================================================================
    
    #--------------------------------------------------------------------------
    def setmyid( self, guid ):
    #--------------------------------------------------------------------------
	    self.guid = guid
    
    #--------------------------------------------------------------------------------------
    def broadcast(self,msgType,msgData,pid):
    #--------------------------------------------------------------------------------------
        for peer in self.peers :
            if peer != pid and peer!=self.guid :
                time.sleep(0.5) #just to test
                ip , port = self.peers[peer]
                self.connectAndSend(ip,port,msgType,msgData,pId=peer,waitReply=False)

    #--------------------------------------------------------------------------------------
    def logging(self,error):
    #--------------------------------------------------------------------------------------
        '''
        function that is used to write to log files
        '''
        try:
            Path("./logs").mkdir(exist_ok=True)
            filename=Path("./logs/"+self.startTime.replace(':','-')+".txt")
            file = open(filename,'a') 
            file.write("[{}] : ".format(datetime.datetime.now().strftime("%H:%M:%S"))+error+'\n') 
            file.close()
        except:
            print("{} could not be created".format(str(filename)))


    #--------------------------------------------------------------------------------------
    def peerLimitReached(self):
    #--------------------------------------------------------------------------------------
        if self.npeer == len(self.peers) or len(self.peers) > self.npeer :
            return True
        else:
            return False


    def addPeer(self,peerid,ip,port):
        if peerid not in self.peers :
            self.peers[peerid]=[ip,port]
            self.logging("{} peer was added with address {} and port {}".format(peerid,ip,port))
        else:
            old=self.peers[peerid]
            self.peers[peerid]=[ip,port]
            self.logging("Updated peer {} from {} ==> {}".format(peerid,old,[ip,port]))


    #--------------------------------------------------------------------------------------
    def createServerSocket(self):
    #--------------------------------------------------------------------------------------
        '''
        create a server socket from myip and port then listen
        '''
        try:
            inbound = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            inbound.bind((self.myip,self.port))
            inbound.listen()
            return inbound
        except :
            self.logging("* error in createServerSocket : on ip={} port={}".format(self.myip,self.port))
    

    #--------------------------------------------------------------------------------------
    def connectAndSend(self,host,port,msgType,msgData,pId=None,waitReply=True):
    #--------------------------------------------------------------------------------------
        '''
        connect and send message to specified peer
        '''
        msgreply=[]
        try:
            peerconn=PeerConnection(host,port,self.startTime,peerguid=pId)
            peerconn.sendData(msgType,msgData)
            self.logging("Sent {}-{} to peerid : {}".format(msgType,msgData,pId))

            if waitReply:
                onereply=peerconn.recvdata()
                while (onereply != (None,None)):
                    msgreply.append(onereply)
                    self.logging("Got a reply from peerid : {}".format(pId))
                    onereply=peerconn.recvdata()# may need to delete
                return msgreply
            #time.sleep(2) #for testing
            peerconn.close()
        except:
            self.logging("* Could not connect and send to {} : {} on {}".format(pId,host,port))
        


    #--------------------------------------------------------------------------------------
    def handlePeer(self,clientSocket):
    #--------------------------------------------------------------------------------------
        host , port = clientSocket.getpeername()
        self.logging("* Connection to {} has been esstablished".format(str((host,port))))
        '''
        handle peer depending request/ProtocolCode
        '''
        peerconn = PeerConnection(host,port,self.startTime,clientSocket,None)

        try:
            protocolCode , data = peerconn.recvdata()
            if protocolCode : 
                protocolCode = protocolCode.upper()
                
            if protocolCode in self.protocol :
                self.protocol[protocolCode](peerconn , data)
            else :
                self.logging("{} code not recognized ".format(protocolCode))
        except Exception as e:
            print(e)
            self.logging("* error while handeling peer {}:{} with code {}".format(host,port,protocolCode))
            
        #may need to keep open
        self.logging("Closing connection with {} : {}".format(host , port))
        peerconn.close()


    #--------------------------------------------------------------------------------------
    def connectionSpawner(self):
    #--------------------------------------------------------------------------------------
        inbound=self.createServerSocket()
        #inbound.settimeout(70)# this line could be deleted to avoid possible problems 
        print("started listening on port : ",self.port)
        self.logging("started listening on port : {}".format(self.port))
        '''
        this function spwanes inbound connections and sends them off to be handled in threads
        '''
        while not self.turnoff:
            try:
                clientSocket , address = inbound.accept()
                thred=threading.Thread(target=self.handlePeer,args=[clientSocket],daemon=True)
                #uses daemon thread to be able to test, in real application proccess will keep running in background after program closes
                thred.start()
            except :
                self.logging("* error in connectionsSpawner : was not able to spawn a connection to {}".format(address))
                continue
        
        inbound.close()


#==========================================================================================
class PeerConnection:

    #--------------------------------------------------------------------------------------
    def __init__(self,peerip,port,start,sock=None,peerguid=None):
    #--------------------------------------------------------------------------------------

        self.peerguid=peerguid 
        self.peerip=peerip
        self.port=int(port)
        self.start=start
        '''
        if socket not available create it and connect
        '''
        if not sock:
            try:
                self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.sock.connect((self.peerip,self.port))
            except:
                self.logging("* peercon could not connect to {} on {}".format(self.peerip,self.port))
        else:
            self.sock=sock
    

    #--------------------------------------------------------------------------------------
    def logging(self,error):
    #--------------------------------------------------------------------------------------
        '''
        function that is use to write to log files
        '''
        try:
            Path("./logs").mkdir(exist_ok=True)
            filename=Path("./logs/"+self.start.replace(':','-')+".txt")
            file = open(filename,'a') 
            file.write("[{}] : ".format(datetime.datetime.now().strftime("%H:%M:%S"))+error+'\n') 
            file.close()
        except:
            self.logging("* {} could not be created".format(str(filename)))


    #--------------------------------------------------------------------------------------   
    def setPeerGuid(self,guid):
    #--------------------------------------------------------------------------------------
        self.peerguid=guid
    

    #--------------------------------------------------------------------------------------
    def forgeMessage(self,msgType,msgData):
    #--------------------------------------------------------------------------------------
        #The network byte order is defined to always be big-endian (>)
        msg="-".join([msgType,msgData])
        return msg.encode("utf-8")


    #--------------------------------------------------------------------------------------
    def sendData(self,msgType,msgData):
    #--------------------------------------------------------------------------------------
        '''
        send msg and return true on success 
        '''
        try:
            msg=self.forgeMessage(msgType,msgData)
            self.sock.sendall(msg)
        except:
            self.logging("* failed to send data to {} on {}".format(self.peerip,self.port))
            return False
        return True



    #--------------------------------------------------------------------------------------
    def recvdata(self):
    #--------------------------------------------------------------------------------------
        '''
        receive msg and return (protocolCode,data) on success 
        '''
        try:
            received=self.sock.recv(4096)
            msg=received.decode('utf-8')
            msgType , msgData=msg.split('-',1)
        except:
            self.logging("* failed to receive data from {} on {}".format(self.peerip,self.port))
        return (msgType,msgData)



    #--------------------------------------------------------------------------------------
    def close(self):
    #--------------------------------------------------------------------------------------
        '''
        close the connection , sendData and recvdate wont work after this
        '''
        self.sock.close()
        self.sock=None



    def __str__(self):
        return "|%s|" % self.peerguid
