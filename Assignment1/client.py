# based on https://pythontic.com/modules/socket/udp-client-server-example
import socket

serverAddressPort   = ("server", 50000)
bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

clientInput = input("Enter the worker number: ")
bytesToSend = str.encode("worker"+str(clientInput))
# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg = "Message from Server {}".format(msgFromServer[0])
print(msg)
