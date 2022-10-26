import socket
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64decode, b64encode

localIP = "worker2"
localPort = 50002
bufferSize = 1024
serverAddressPort = ("server", 50000)
filename = "shrek.jpg"
key = "PublicKeyForNetwork"


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


UDPWorkerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPWorkerSocket.bind((localIP, localPort))

print("Worker 2 listening for request")

# message sent from server will cause worker to reply with text file
bytesAddressPair = UDPWorkerSocket.recvfrom(bufferSize)
message = bytesAddressPair[0]
address = bytesAddressPair[1]
encryptionProtocol = AESCipher(key=key)
message = message.decode()
message = encryptionProtocol.decrypt(message)
ServerMsg = "Message from server:{}".format(message)
print(ServerMsg)

with open(filename, "rb") as file:
    while True:
        bytesToSend = file.read(bufferSize)
        if not bytesToSend:
            break  # no more bytes left to send
        bytesToSend = (encryptionProtocol.encrypt(bytesToSend)).encode()
        UDPWorkerSocket.sendto(bytesToSend, serverAddressPort)
        print("sent a packet!")

print("file sent! -- sending ACK")
ack = (encryptionProtocol.encrypt("SendingFinished")).encode()
UDPWorkerSocket.sendto(ack, serverAddressPort)
# with open(filename, "rb") as f:
#    bytes_read = f.read(4096)
#    UDPWorkerSocket.sendto(bytes_read)
