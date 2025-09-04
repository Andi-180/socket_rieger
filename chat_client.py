import struct
from socket import socket,AF_INET,SOCK_STREAM
from datetime import datetime
from utility import send,recv
from chat import ChatMessage,ChatServerResponse
class Send_Message:
    def __init__(self,s):
        self.s = s
    def sendmsg(self):
        self.s.send(b'\x01')
        name = input("Your Name: ")
        message = input("message: ")
        cm = ChatMessage(name,message,datetime.now().timestamp())
        send(self.s,cm.serialize())
        csr = ChatServerResponse.deserialize(recv(self.s,257))
        print(f"Ergebnis von Server: {csr}")
class Message_Log:
    def __init__(self,s):
        self.s = s
    def sendmsg(self):
        self.s.send(b'\x02')
        number = struct.unpack('>i',recv(self.s,4))
        print(f"Anzahl der Nachrichten: {number[0]}")
        for i in range(number[0]):
            cm = ChatMessage.deserialize(recv(self.s, 277))
            print(f"Message {i}: {cm}")
        csr = ChatServerResponse.deserialize(recv(self.s, 257))
        print(f"Ergebnis von Server: {csr}")
class Bye_Msg:
    def __init__(self,s):
        self.s = s
    def sendmsg(self):
        self.s.send(b'\x00')
        csr = ChatServerResponse.deserialize(recv(self.s,257))
        print(f"Ergebnis von Server: {csr}")
s = socket(AF_INET,SOCK_STREAM)
s.connect(('localhost',8080))
while True:
    text = input("Your input (snd/log/bye): ")
    if(text == "snd"):
        sendmsg = Send_Message(s)
        sendmsg.sendmsg()
    elif(text == "log"):
        msglog = Message_Log(s)
        msglog.sendmsg()
    elif(text == "bye"):
        byemsg = Bye_Msg(s)
        byemsg.sendmsg()
        break
    else:
        print("Fehlerhafte Eingabe")
s.close()
        