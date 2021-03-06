from socket import *
from Constants import *
from random import *

corruptDictionary = {0 : b'\x01', 1 : b'\x02', 2 : b'\x04', 3 : b'\x08',
                     4 : b'\x10', 5 : b'\x20', 6 : b'\x40', 7 : b'\x80'}

##---------------Bitwise Manipulation-----------------##
#------------------------------------------------------#

##---------------Checksum-----------------##
def ChecksumAddition(curSum, nextItem):
    tempInt = int.from_bytes(curSum, 'big') + int.from_bytes(nextItem, 'big')
    if tempInt >= 65536: #overflow
        tempInt = (tempInt % 65536) + 1
    return(bytearray(tempInt.to_bytes(2, 'big')))

def MakeChecksum(bString):
    checksum = bytearray(b'\x00\x00')  ## Returns 16 bit bytes object (b'\x00\x00')
    localIndex = 0
    for x in bString:
        if localIndex is 0:
            tempBytes = bytearray(x)
            localIndex = 1
        else:
            tempBytes.append(x)
            checksum = ChecksumAddition(checksum,tempBytes)
            localIndex = 0
    #print(checksum)
    return checksum

def CheckChecksum(bString):
    checkString = MakeChecksum(bString[2:])
    checkArray = bytearray(checkString)
    recievedArray = bytearray(bString)
    if (checkArray[1] == recievedArray[1]) and (checkArray[0] == recievedArray[0]):
        return True
    else:
        return False

def InsertChecksum(data, checksum):
    return bytes(checksum + data)

def RemoveChecksum(bString):
    return bString[2:]


##---------------Sequence Number-----------------##
def AddSequenceNum(seq, seqNum):
    return bytes([seqNum]) + seq

def RemoveSequenceNum(seq):
    return seq[1:]

def CheckSequenceNum(seq, seqNum):
    InSequence = False
    if seq[2] is seqNum:
        InSequence = True
        return InSequence, RemoveSequenceNum(seq)
    else:
        return InSequence


##---------------Packet Functions-----------------##
def PackageHeader(data, seq, failPercent = 0):
    Segment = AddSequenceNum(data, seq)
    return InsertChecksum(Segment, MakeChecksum(Segment))

def UnpackageHeader(segment):
    return (segment[3:])

def IsAck(segment, seqNum):
    if (UnpackageHeader(segment) is ACK):
        if CheckSequenceNum(segment,seqNum):
            return True
    return False

def CorruptPacket(bString):
    bString += (corruptDictionary[randint(0,7)])
    return bString