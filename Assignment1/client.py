# based on https://pythontic.com/modules/socket/udp-client-server-example
from xmlrpc import client
import zlib
import socket

serverAddressPortTuple = ("server", 50000)
bufferSize = 1024
fileName = "File.txt"

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
clientInput = input("Enter the worker number: ")
bytesToSend = str.encode("worker"+str(clientInput))
# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPortTuple)

while True:
    fileFromWorker = UDPClientSocket.recvfrom(bufferSize)
    fileMessage = fileFromWorker[0]
    WorkerPort = fileFromWorker[1]
    if (clientInput == 1):
        if ("{}".format(fileMessage) == "b'SendingFinished'"):
            break
        with open("worker1File.txt", "a") as file:
            file.write(fileMessage.decode())
    if (clientInput == 2):
        global worker2On
        worker2On = True
        if ("{}".format(fileMessage) == "b'SendingFinished'"):
            break
        with open("tempImage.jpg", "ab") as tempImage:
            tempImage.write(fileMessage)
    if (clientInput == 3):
        global worker3On
        worker3On = True
        if ("{}".format(fileMessage) == "b'SendingFinished'"):
            break
        with open("worker3File.txt", "a") as file:
            file.write(fileMessage.decode())
