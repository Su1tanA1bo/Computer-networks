import socket

localIP     = "worker3"
localPort   = 50003
bufferSize  = 1024
serverAddressPort   = ("server", 50000)

filename = "info.txt"
#filesize = os.path.getsize(filename)

UDPWorkerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPWorkerSocket.bind((localIP, localPort))

print("Worker 3 listening for request")

#message sent from server will cause worker to reply with text file
while(True):
    bytesAddressPair = UDPWorkerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    
    ServerMsg = "Message from server:{}".format(message)
    print(ServerMsg)
    
    with open(filename, "rb") as file:
        while True:
            bytesToSend = file.read(bufferSize)
            if not bytesToSend:
                break #no more bytes left to send
            UDPWorkerSocket.sendto(bytesToSend, serverAddressPort)
            print("sent a packet!")
    
    print("file sent!")
    #with open(filename, "rb") as f:
    #    bytes_read = f.read(4096)
    #    UDPWorkerSocket.sendto(bytes_read)
    
    
    