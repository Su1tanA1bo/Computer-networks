# based on https://pythontic.com/modules/socket/udp-client-server-example
import zlib
import socket

serverAddressPortTuple = ("server", 50000)
bufferSize = 1024
fileName = "File.txt"

def checksum_generator(data):
 checksum = zlib.crc32(data)
 return checksum

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
clientInput = input("Enter the worker number: ")
bytesToSend = str.encode("worker"+str(clientInput))
# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPortTuple)

#msgFromServer = UDPClientSocket.recvfrom(bufferSize)
#msg = "{}".format(msgFromServer[0].decode('utf8'))

file = open("./files/"+fileName, 'w')
#file.write(msg)
file.close()
