# based on https://pythontic.com/modules/socket/udp-client-server-example
import socket
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64decode, b64encode

# class used for encrypting
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


serverAddressPortTuple = ("server", 50000)
bufferSize = 1024
fileName = "File.txt"

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
clientInput = input("Enter the worker number: ")
print("input ="+clientInput)

# encryption
key = "PublicKeyForNetwork"
encryptionProtocol = AESCipher(key=key)
message = "worker"+str(clientInput)
encryptedMessage = encryptionProtocol.encrypt(message)
bytesToSend = encryptedMessage.encode()

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPortTuple)

while True:
    fileFromWorker = UDPClientSocket.recvfrom(bufferSize)
    fileMessage = fileFromWorker[0]
    fileMessage = message.decode()
    fileMessage = encryptionProtocol.decrypt(message)
    if (fileMessage == "SendingFinished"):
        break
    if (clientInput == "1"):
        with open("./files/worker1File.txt", "a") as file:
            file.write(fileMessage)
    if (clientInput == "2"):
        with open("./files/tempImage.jpg", "ab") as file:
            file.write(fileMessage)
    if (clientInput == "3"):
        with open("./files/worker3File.txt", "a") as file:
            file.write(fileMessage)
