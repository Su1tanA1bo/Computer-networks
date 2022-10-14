# based on https://pythontic.com/modules/socket/udp-client-server-example

# make new folder in client container to prove image existence
# test all threee workers inshallah
import socket
import os

localIP = "server"
localPort = 50000
bufferSize = 1024

worker1Port = ("worker1", 50001)
worker2Port = ("worker2", 50002)
worker3Port = ("worker3", 50003)
targetPort = ("", 0)
global workerThreeOn
workerThreeOn = False
global workerOneOn
workerOneOn = False
global workerTwoOn
workerTwoOn = False

responseToClient = "Message Received"
responseToClientBytes = str.encode(responseToClient)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
try:
    os.remove("tempImage.jpg")
except:
    print("tempImage doesnt exist")

print("UDP server up and listening")
# Listen for incoming datagrams


def server():
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    global clientAddress
    clientAddress = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)

    print("message is {}".format(message))
    if ("{}".format(message) == "b'worker1'"):
        targetPort = worker1Port
        print("worker 1 has been selected")
    if ("{}".format(message) == "b'worker2'"):
        targetPort = worker2Port
        print("worker 2 has been selected")
    if ("{}".format(message) == "b'worker3'"):
        targetPort = worker3Port
        print("worker 3 has been selected")

    print(clientMsg)

    # requesting file
    UDPServerSocket.sendto((str.encode("We need file")), targetPort)
    # file received
    while True:
        fileFromWorker = UDPServerSocket.recvfrom(bufferSize)
        fileMessage = fileFromWorker[0]
        WorkerPort = fileFromWorker[1]
        if ("{}".format(WorkerPort[1]) == "50001"):
            global workerOneOn
            workerOneOn = True
            if ("{}".format(fileMessage) == "b'SendingFinished'"):
                break
            with open("worker1File.txt", "a") as file:
                file.write(fileMessage.decode())
        if ("{}".format(WorkerPort[1]) == "50002"):
            global workerTwoOn
            workerTwoOn = True
            if ("{}".format(fileMessage) == "b'SendingFinished'"):
                break
            with open("tempImage.jpg", "ab") as tempImage:
                tempImage.write(fileMessage)

        if ("{}".format(WorkerPort[1]) == "50003"):
            global workerThreeOn
            workerThreeOn = True
            if ("{}".format(fileMessage) == "b'SendingFinished'"):
                break
            with open("worker3File.txt", "a") as file:
                file.write(fileMessage.decode())


server()
if workerOneOn == True:
    with open("worker1File.txt", "rb") as file:
        while True:
            bytesToSend = file.read(bufferSize)
            if not bytesToSend:
                break  # no more bytes left to send
            UDPServerSocket.sendto(bytesToSend, clientAddress)
            print("sent a packet!")
    UDPServerSocket.sendto("SendingFinished".encode(), clientAddress)
    print("worker1 file sent to client")

if workerTwoOn == True:
    with open("tempImage.jpg", "rb") as file:
        while True:
            bytesToSend = file.read(bufferSize)
            if not bytesToSend:
                break  # no more bytes left to send
            UDPServerSocket.sendto(bytesToSend, clientAddress)
            print("sent a packet!")
    UDPServerSocket.sendto("SendingFinished".encode(), clientAddress)
    print("worker2 image sent to client")

if workerThreeOn == True:
    with open("worker3File.txt", "rb") as file:
        while True:
            bytesToSend = file.read(bufferSize)
            if not bytesToSend:
                break  # no more bytes left to send
            UDPServerSocket.sendto(bytesToSend, clientAddress)
            print("sent a packet!")
    UDPServerSocket.sendto("SendingFinished".encode(), clientAddress)
    print("worker3 file sent to client")

#UDPServerSocket.sendto(fileMessage, clientAddress)
