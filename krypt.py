import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

import io
import os


class AESCipher():

    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()
        self.fileName = "Db.kr"

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode("utf-8")

    def addEntry(self, plainTextRow):

        if os.path.isfile(self.fileName) == False :
            textFile = io.open(self.fileName, "wb+")

            enc = self.encrypt(plainTextRow)
            textFile.write(enc)
        else:
            textFile = io.open(self.fileName, "rb+")

            raw = self.decrypt(textFile.read())
            raw = ";".join([raw,plainTextRow])

            enc = self.encrypt(raw)
            textFile.close()

            textFile = io.open(self.fileName, "wb")
            textFile.write(enc)

        textFile.close()

    def decryptAll(self, enc):
        if os.path.isfile(self.fileName) == True :
            textFile = io.open(self.fileName, "r")
            Db = self.decrypt(textFile.read())
            Db = self.parse(Db)
            textFile.close()
            return Db

    @staticmethod
    def parse(txt):
        return txt.replace(";", "\n")


    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
