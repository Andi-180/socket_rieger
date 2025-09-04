import struct
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from utility import send, recv
from chat import ChatMessage,ChatServerResponse
from datetime import datetime

class Communication(Thread):
    msglist = []
    def __init__(self, client_socket, client_address):
        super().__init__()
        self.client_socket = client_socket
        self.client_address = client_address
        
    def run(self):
        while True:
            #print(self.client_address)
            code = recv(self.client_socket, 1)
            if code == b'\x01':
                #print('Received Code: 1')
                try:
                    message_data = recv(self.client_socket, 277)
                    cm = ChatMessage.deserialize(message_data)
                    print(cm)
                    response = ChatServerResponse(True, "Message received successfully")
                    send(self.client_socket, response.serialize())
                    Communication.msglist.append(cm)
                    #print(len(Communication.msglist))
                except Exception as e:
                    error_msg = f'An error occurred while trying to unpack the message: {e}'
                    print(error_msg)
                    response = ChatServerResponse(False, error_msg)
                    send(self.client_socket, response.serialize())

            elif code == b'\x02':
                print('Received Code: 2')
                try:  
                    response_number = struct.pack('>i', len(Communication.msglist))
                    send(self.client_socket, response_number)
                    print(len(Communication.msglist))
                    for msg in Communication.msglist:
                        print(msg)
                        send(self.client_socket, msg.serialize())
                    response_ok = ChatServerResponse(True, "msglog send was successful")
                    send(self.client_socket, response_ok.serialize())
                except Exception as e:
                    error_msg = f'An error occurred while trying to send the message log: {e}'
                    print(error_msg)
                    response = ChatServerResponse(False, error_msg)
                    send(self.client_socket, response.serialize())


            elif code == b'\x00':
                print('Received Code: 0')
                response = ChatServerResponse(False, "Bye, thank you for using this server.")
                send(self.client_socket, response.serialize())
                break
            else:
                print('Wrong input, please try another connection.')
                response = ChatServerResponse(False, 'Invalid code received')
                send(self.client_socket, response.serialize())

        self.client_socket.close()

s = socket(AF_INET, SOCK_STREAM)
s.bind(('localhost', 8080))
s.listen()
print("Server is listening...")
while True:
    client_socket, client_address = s.accept()
    c = Communication(client_socket, client_address)
    c.start()
