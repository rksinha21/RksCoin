from hashlib import sha256
from datetime import datetime

class InvalidTransactionException(Exception):pass
class InsufficientAmountException(Exception):pass

def updateHash(*args):

    hashing = ""
    h = sha256()
    for arg in args:
        hashing += str(arg)

    h.update(hashing.encode('utf-8'))
    return h.hexdigest()

class Block():

    def __init__(self,number=0,previousHash= "0" * 64,data=None,nonce=0,time=datetime.fromtimestamp(datetime.timestamp(datetime.now()))):
        self.number = number
        self.previousHash = previousHash
        self.data = data
        self.nonce = nonce
        self.time = time

    def hash(self):
        return updateHash(self.data,self.previousHash,self.number,self.nonce,self.time)

    def __str__(self):
        return str("\nBlock#: %s\nHash: %s\nPrevious Hash: %s\nData: %s\nNonce: %s\nTime Stamp: %s\n" %(self.number,self.hash(),self.previousHash,self.data,self.nonce,self.time))


class Blockchain():


    def __init__(self,chain=[]):

        self.chain = chain

    def addBlock(self,block):
        self.chain.append(block)

    def mine(self,block):
        try:
            block.previousHash = self.chain[-1].hash()
        except IndexError:
            pass

        while True:
            if block.hash()[:4] == "0" * 4:
                self.addBlock(block)
                break
            else:
                block.nonce += 1

    def isValid(self):
        for i in range(1,len(self.chain)):
            previous = self.chain[i].previousHash
            current = self.chain[i-1].hash()

            if previous != current or current[:4] != "0" * 4:
                return False
        return True

    def sendMoney(self,sender,reciever,amount):
        try:
            amount = float(amount)
        except ValueError:
            raise InvalidTransactionException("Invalid Transaction")

        if amount == 0.00:
            raise InsufficientAmountException("Invalid Amount")
        elif sender == reciever or amount <= 0.00:
            raise InvalidTransactionException("Invalid Transaction")

        number = len(self.chain) + 1
        data = "%s-->%s-->%s" %(sender,reciever,amount)

        if self.isValid():
            self.mine(Block(number,data=data,time=datetime.fromtimestamp(datetime.timestamp(datetime.now()))))
            print("Block is valid\n")
        else:
            print("Corrupted Blockchain\n")


        for block in self.chain:
            print(block)


    def getBalance(self,name):
        balance = 0.00
        for block in self.chain:
            data = block.data.split("-->")
            if name == data[0]:
                balance -= float(data[2])
            elif name == data[1]:
                balance += float(data[2])
        return balance


def main():
    blocks = Blockchain()
    ch = 'y'

    while ch == 'y' or ch == 'Y':
        sender = input("\nenter sender's name: ")
        reciever = input("enter reciever's name: ")
        amount = input("enter the amount: ")

        blocks.sendMoney(sender,reciever,amount)
        ch = input("do you want to make another transaction? press Y if yes: ")

    print("\nBalance for " + sender + " is " + str(blocks.getBalance(sender)))


if __name__ =="__main__":
    main()
