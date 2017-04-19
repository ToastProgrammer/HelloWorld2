#Eric Craaybeek, Ben Tozier
#Python Net Design Project Phase 1

#code adapted from :
#"Computer Networking: A Top-Down Approach" by Keith Ross and James Kurose
from binascii import *
from SocketFunctions import *
from DataFunctions import *
from socket import *
from Constants import *
from os import remove

global writeIndex

######## Function:
######## deliver data
#### Purpose:
#### delivers the data from packet and appends to file
## Paramters:
## Data in
def deliver_data(data, writeIndex):
    moreData = True
    fileWrite = open(dstFile, 'ab')
    fileWrite.seek(PacketSize * writeIndex, 0)
    fileWrite.write(data)
    #if EOF close file
    writeIndex += PacketSize
    if data == b'':
        fileWrite.close()
        moreData = False
    return moreData, writeIndex

######## Function:
######## ServerMain
#### Purpose:
#### contains the FSM for GBN file receive
## Paramters:
## None
def ServerMain():

    serverSocket = socket(AF_INET, SOCK_DGRAM)

    serverSocket.bind(('',ServerPort))

    print ('The server is ready to receive')

    while 1:
        # Wait here until recieve message from socket
        print("Outer Loop")

        moreData = True
        writeIndex = 0
        expectedSeqNum = 1
        sndpkt = PackageHeader(ACK,expectedSeqNum)
        while(moreData):
            print(rcvpkt)
            if CheckChecksum(rcvpkt) and CheckSequenceNum(rcvpkt, expectedSeqNum):  # If Checksum & seq num correct
                expectedSeqNum += 1

                data = UnpackageHeader(rcvpkt)
                moreData, writeIndex = deliver_data(data, writeIndex)  # Write correct data to file
                sndpkt = PackageHeader(ACK, expectedSeqNum)  # Package CORRECT ack
                print(sndpkt[2])
                udt_send(sndpkt, serverSocket, ClientPort)
                #onceThrough = True
            else:
                udt_send(sndpkt, serverSocket, ClientPort)




ServerMain()