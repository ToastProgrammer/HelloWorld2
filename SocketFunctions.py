from socket import *
from Constants import *
from time import sleep
from DataFunctions import CorruptCheck, LossCheck
import random


##-----------------Socket Functions-------------------##
#------------------------------------------------------#
#def Client_Wait(ServerName, ServerPort, seqNum, prevPacket):


def udt_send(packet, socket, port, corChance = 0, lossChance = 0):
    packet = CorruptCheck(packet, corChance)
    if LossCheck(lossChance):   # If packet "lost", send nothing
        return
    else:                       # Otherwise send as normal
        try:
            socket.sendto(packet, (ServerName, port))
        except:
            print("SOCKET ERROR", socket)

def rdt_rcv(socket):
    rcvpkt, clientAddress = socket.recvfrom(2048)
    return rcvpkt



