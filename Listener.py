import socket
import pickle
from Database import Database


#Reagiert auf Anfragen Außerhalb
class Listener:
    def __init__(self):
        # Standard loopback interface address (localhost)
        self.host = "127.0.0.1"
        # Port to listen on (non-privileged ports are > 1023)
        self.port = 65432
        self.db = Database()

    #Socket starten
    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            while True:
                conn, addr = s.accept() #Auf Anfrage warten

                with conn:
                    print("Connected by {}".format(addr))
                    print("Server loads file size")
                    file_size = pickle.loads(conn.recv(3000))
                    print("Server loaded file size")
                    print(file_size)
                    conn.sendall(pickle.dumps("file_size received"))
                    buffer_size = file_size

                    print("Server should load file")
                    request = pickle.loads(conn.recv(buffer_size))
                    print("Server loaded file")
                    print(request)
                    response = self.handleRequest(request)
                    response_pickled = pickle.dumps(response)

                    print("Server sending file size")
                    conn.sendall(pickle.dumps(len(response_pickled)))
                    print("Server sent file size.")
                    ack = pickle.loads(conn.recv(3000))
                    print(ack)

                    print("Server should send response")
                    conn.sendall(response_pickled)
                    print("Server sent response")

    #Anfragen behandeln
    def handleRequest(self,request):
        type,input = request
        response = None
        if type=="register":
            response = self.db.registerUser(input)
        elif type=="login":
            response = self.db.loginUser(input)
        elif type== "chat":
            response = self.db.createChat(input)
        elif type== "message":
            response = self.db.createMessage(input)
        elif type== "get_messages":
            response = self.db.getMessages(input)
        elif type== "get_chats":
            response = self.db.getChats(input)
        elif type== "get_usernames":
            response = self.db.getUsernames(input)
        elif type== "send_file":
            response = self.db.storeFile(input)
        elif type== "get_file":
            response = self.db.getFile(input)
        else:
            response = (False,"Invalid request!")

        return response

