import socket

localIP     = "worker1"
localPort   = 50001
bufferSize  = 1024
serverAddressPort   = ("server", 50000)

filename = "info.txt"
#filesize = os.path.getsize(filename)

UDPWorkerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPWorkerSocket.bind((localIP, localPort))

print("Worker 1 listening for request")

#message sent from server will cause worker to reply with text file
while(True):
    bytesAddressPair = UDPWorkerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    
    ServerMsg = "Message from server:{}".format(message)
    print(ServerMsg)
    
    UDPWorkerSocket.sendto(str.encode("placeholder for file from worker1"), serverAddressPort)
    print("file sent!")
    #with open(filename, "rb") as f:
    #    bytes_read = f.read(4096)
    #    UDPWorkerSocket.sendto(bytes_read)
    
    
    