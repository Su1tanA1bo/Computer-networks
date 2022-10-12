# based on https://pythontic.com/modules/socket/udp-client-server-example
import zlib
import socket
import hashlib
from typing import ByteString
import struct

srcPort = 1111 #inheader
serverAddressPortTuple = ("server", 50000)
serverPort = 50000 #inheader
bufferSize = 10241
fileName = "File.txt"

def checksum_generator(data):
 checksum = zlib.crc32(data)
 return checksum

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

clientInput = input("Enter the worker number: ")
bytesToSend = str.encode("worker"+str(clientInput))
messageLength = len(bytesToSend) #inheader
#generating checksum
checksum = checksum_generator(bytesToSend)
#gathering header info
udp_header = struct.pack("!IIII", srcPort, serverPort, messageLength, checksum)
# Send to server using created UDP socket
#UDPClientSocket.sendto(bytesToSend, serverAddressPortTuple)
print(str(udp_header))

#msgFromServer = UDPClientSocket.recvfrom(bufferSize)
#msg = "{}".format(msgFromServer[0].decode('utf8'))

file = open("./files/"+fileName, 'w')
#file.write(msg)
file.close()
