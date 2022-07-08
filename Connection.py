import socket
import hashlib
import pickle
from PIL import Image

class Connection:
    def __init__(self):
        # The server's hostname or IP address
        self.host = "127.0.0.1"
        # The port used by the server
        self.port = 65432


    #Anfragen verschicken
    def sendRequest(self,request):
        type, input = request
        if type == "send_file":
            file_path = input[2]
            file = Image.open(file_path)
            request = (type,(input[0],input[1],file))
        elif type == "login":
            user,password = input
            request = (type,(user,hashlib.sha256(password.encode()).hexdigest()))
        elif type == "register":
            user,password,phone = input
            request = (type, (user,hashlib.sha256(password.encode()).hexdigest(),phone))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            request_pickled = pickle.dumps(request)
            print("Size of request: {} Bytes".format(len(request_pickled)))

            print("Client sending file size")
            s.sendall(pickle.dumps(len(request_pickled)))
            ack = pickle.loads(s.recv(3000))
            print(ack)
            print("Client sent file size.")
            print("Client should send request")
            s.sendall(request_pickled)
            print("Client sent request")

            print("Client loads size of response")
            file_size = pickle.loads(s.recv(3000))
            print("Client loaded size of response")
            print(file_size)
            buffer_size = file_size
            s.sendall(pickle.dumps("file_size received"))
            print("Client loads response")
            success, message = pickle.loads(s.recv(buffer_size))
            print("Client loaded response")

        print(success,message)
        return success, message
