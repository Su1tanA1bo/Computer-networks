# based on https://pythontic.com/modules/socket/udp-client-server-example
import socket

localIP     = "server"
localPort   = 50000
bufferSize  = 1024

worker1Port = ("worker1", 50001)
worker2Port = ("worker2", 50002)
worker3Port = ("worker3", 50003)
targetPort = ("", 0)

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
    
    #file received
    fileFromWorker = UDPServerSocket.recvfrom(bufferSize)
    fileMessage = fileFromWorker[0]
    print("file from worker: {}".format(fileMessage))
    
    #sending file to client
    UDPServerSocket.sendto(fileMessage, clientAddress)
    
