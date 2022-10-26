import socket
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64decode, b64encode

# class used for encrypting


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


text = "PublicKeyForNetwork"
encryptionProtocol = AESCipher(key=text)
awd = encryptionProtocol.encrypt(text="helloWorld")
print(awd)
decrypted = encryptionProtocol.decrypt(awd)
print(decrypted)
