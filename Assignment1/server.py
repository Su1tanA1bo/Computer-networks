# based on https://pythontic.com/modules/socket/udp-client-server-example
import socket

localIP     = "server"
localPort   = 50000
bufferSize  = 1024

worker1Port = ("worker1", 50001)
worker2Port = ("worker2", 50002)
worker3Port = ("worker3", 50003)
targetPort = ("", 0)

fileName = "File.txt"

responseToClient = "Message Received"
responseToClientBytes = str.encode(responseToClient)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    clientAddress = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(clientAddress)
    
    print("message is {}".format(message))
    if("{}".format(message) == "b'worker1'"):
        targetPort = worker1Port
        print("worker 1 has been selected")
    if("{}".format(message) == "b'worker2'"):
        targetPort = worker2Port
        print("worker 2 has been selected")
    if("{}".format(message) == "b'worker3'"):
        targetPort = worker3Port
        print("worker 3 has been selected")
    
    print(clientMsg)
    print(clientIP)
    
    #requesting file
    UDPServerSocket.sendto((str.encode("We need file")), targetPort)
    worker1Message = ""
    #file received
    while True:
        fileFromWorker = UDPServerSocket.recvfrom(bufferSize)
        fileMessage = fileFromWorker[0]
        WorkerPort = fileFromWorker[1]
        if("{}".format(WorkerPort[1]) == "50001"):
            if("{}".format(fileMessage) == "b'SendingFinished'"):
                break;
            print("\nfile from worker1: {}".format(fileMessage))
            worker1Message = worker1Message+"{}".format(fileMessage)
        if("{}".format(WorkerPort) == "50002"):
            if("{}".format(fileMessage) == "b'SendingFinished'"):
                break;
            print("\nfile from worker2: {}".format(fileMessage))
            worker2Message = worker2Message+"{}".format(fileMessage)
        if("{}".format(WorkerPort) == "50003"):
            if("{}".format(fileMessage) == "b'SendingFinished'"):
                break;
            print("\nfile from worker3: {}".format(fileMessage))
            worker3Message = worker3Message+"{}".format(fileMessage)
    #sending file to client
    print(worker1Message)
    #UDPServerSocket.sendto(fileMessage, clientAddress)

