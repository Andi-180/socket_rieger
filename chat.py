import struct
class ChatMessage:
    fmt = '>d13p256p'
    def __init__(self,sender,message,timestamp):
        self.sender = sender
        self.message = message
        self.timestamp = timestamp
    @staticmethod
    def deserialize(b):
        timestamp, sender, message  = struct.unpack(ChatMessage.fmt,b)
        return ChatMessage(sender.decode(),message.decode(),timestamp)
    def serialize(self):
        return struct.pack(ChatMessage.fmt,self.timestamp,self.sender.encode(),self.message.encode())
    def __str__(self):
        return f'{self.sender} sends: \"{self.message}\"'

class ChatServerResponse:
    fmt = '?256p'
    def __init__(self,ok,msg):
        self.ok = ok
        self.msg = msg
    @staticmethod
    def deserialize(b):
        ok, msg = struct.unpack(ChatServerResponse.fmt,b)
        return ChatServerResponse(ok,msg)
    def serialize(self):
        return struct.pack(ChatServerResponse.fmt,self.ok,self.msg.encode())
    def __str__(self):
        return f'{self.msg.decode()}'