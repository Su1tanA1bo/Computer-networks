# based on https://pythontic.com/modules/socket/udp-client-server-example

# make new folder in client container to prove image existence
# test all threee workers inshallah
import socket
import os
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64decode, b64encode, decode

localIP = "server"
localPort = 50000
bufferSize = 1024

key = "PublicKeyForNetwork"  # public key
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


class AESCipher(object):
    def __init__(self, key):  # recieve key
        self.blockSize = AES.block_size
        # generate 256 bit hash key
        self.key = hashlib.sha256(key.encode()).digest()

    def pad(self, text):  # takes string and makes sure theres 128 bits in string
        bytesToPad = self.blockSize - len(text) % self.blockSize
        asciiString = chr(bytesToPad)
        paddingString = bytesToPad * asciiString
        paddedText = text + paddingString
        return paddedText

    @staticmethod
    def unpad(text):  # removes unused bits from padded string
        lastCharacter = text[len(text) - 1:]
        bytesToRemove = ord(lastCharacter)
        return text[:-bytesToRemove]

    def encrypt(self, text):
        text = self.pad(text)
        iv = Random.new().read(self.blockSize)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encryptedText = cipher.encrypt(text.encode())
        return b64encode(iv + encryptedText).decode("utf-8")

    def decrypt(self, encryptedText):
        encryptedText = b64decode(encryptedText)
        iv = encryptedText[:self.blockSize]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        text = cipher.decrypt(
            encryptedText[self.blockSize:]).decode("utf-8")
        return self.unpad(text)


encryptionProtocol = AESCipher(key=key)

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
    encryptedMessage = bytesAddressPair[0]
    global clientAddress
    clientAddress = bytesAddressPair[1]
    encryptedMessage = encryptedMessage.decode()
    message = encryptionProtocol.decrypt(encryptedMessage)

    print("message is {}".format(message))
    if (message == "worker1"):
        targetPort = worker1Port
        print("worker 1 has been selected")
    if (message == "worker2"):
        targetPort = worker2Port
        print("worker 2 has been selected")
    if (message == "worker3"):
        targetPort = worker3Port
        print("worker 3 has been selected")

    # requesting file
    requestMessage = str.encode(encryptionProtocol.encrypt("We need file"))
    UDPServerSocket.sendto(requestMessage, targetPort)
    # file received
    while True:
        fileFromWorker = UDPServerSocket.recvfrom(bufferSize)
        fileMessage = fileFromWorker[0]
        fileMessage = encryptionProtocol.decrypt(fileMessage.decode())
        WorkerPort = fileFromWorker[1]
        if ("{}".format(WorkerPort[1]) == "50001"):
            global workerOneOn
            workerOneOn = True
            if (fileMessage == "SendingFinished"):
                break
            with open("worker1File.txt", "a") as file:
                file.write(fileMessage)
        if ("{}".format(WorkerPort[1]) == "50002"):
            global workerTwoOn
            workerTwoOn = True
            if (fileMessage == "SendingFinished"):
                break
            with open("tempImage.jpg", "ab") as tempImage:
                tempImage.write(fileMessage)

        if ("{}".format(WorkerPort[1]) == "50003"):
            global workerThreeOn
            workerThreeOn = True
            if (fileMessage == "SendingFinished"):
                break
            with open("worker3File.txt", "a") as file:
                file.write(fileMessage)


server()
# sending to client
if workerOneOn == True:
    with open("worker1File.txt", "rb") as file:
        while True:
            bytesToSend = file.read(bufferSize)
            if not bytesToSend:
                break  # no more bytes left to send
            bytesToSend = (encryptionProtocol.encrypt(bytesToSend)).encode()
            UDPServerSocket.sendto(bytesToSend, clientAddress)
            print("sent a packet!")
    ack = (encryptionProtocol.encrypt("SendingFinished")).encode()
    UDPServerSocket.sendto(ack, clientAddress)
    print("worker1 file sent to client")

if workerTwoOn == True:
    with open("tempImage.jpg", "rb") as file:
        while True:
            bytesToSend = file.read(bufferSize)
            if not bytesToSend:
                break  # no more bytes left to send
            bytesToSend = (encryptionProtocol.encrypt(bytesToSend)).encode()
            UDPServerSocket.sendto(bytesToSend, clientAddress)
            print("sent a packet!")
    ack = (encryptionProtocol.encrypt("SendingFinished")).encode()
    UDPServerSocket.sendto(ack, clientAddress)
    print("worker2 image sent to client")

if workerThreeOn == True:
    with open("worker3File.txt", "rb") as file:
        while True:
            bytesToSend = file.read(bufferSize)
            if not bytesToSend:
                break  # no more bytes left to
            bytesToSend = (encryptionProtocol.encrypt(bytesToSend)).encode()
            UDPServerSocket.sendto(bytesToSend, clientAddress)
            print("sent a packet!")
    ack = (encryptionProtocol.encrypt("SendingFinished")).encode()
    UDPServerSocket.sendto(ack, clientAddress)
    print("worker3 file sent to client")

#UDPServerSocket.sendto(fileMessage, clientAddress)
