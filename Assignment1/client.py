# based on https://pythontic.com/modules/socket/udp-client-server-example
import socket

serverAddressPortTuple = ("server", 50000)
bufferSize = 1024
fileName = "File.txt"

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
clientInput = input("Enter the worker number: ")
print("input ="+clientInput)
bytesToSend = str.encode("worker"+str(clientInput))
# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPortTuple)

while True:
    fileFromWorker = UDPClientSocket.recvfrom(bufferSize)
    fileMessage = fileFromWorker[0]
    if ("{}".format(fileMessage) == "b'SendingFinished'"):
        break
    if (clientInput == "1"):
        with open("./files/worker1File.txt", "a") as file:
            file.write(fileMessage.decode())
    if (clientInput == "2"):
        with open("./files/tempImage.jpg", "ab") as file:
            file.write(fileMessage)
    if (clientInput == "3"):
        with open("./files/worker3File.txt", "a") as file:
            file.write(fileMessage.decode())
