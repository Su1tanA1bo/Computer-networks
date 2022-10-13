import socket

localIP     = "worker1"
localPort   = 50001
bufferSize  = 1024
serverAddressPort   = ("server", 50000)
filename = "LoremIpsum.txt"

UDPWorkerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPWorkerSocket.bind((localIP, localPort))

print("Worker 1 listening for request")

#message sent from server will cause worker to reply with text file
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
    
print("file sent! -- sending ACK")
UDPWorkerSocket.sendto("SendingFinished".encode(), serverAddressPort)
#with open(filename, "rb") as f:
#    bytes_read = f.read(4096)
#    UDPWorkerSocket.sendto(bytes_read)
    
    
    