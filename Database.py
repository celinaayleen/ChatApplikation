import sqlite3
import time
import datetime
import os
from PIL import Image

# Datenbank User wird erstellt
def createUsersTable():
    connection = sqlite3.connect("database.db")
    sql = "CREATE TABLE IF NOT EXISTS users(" \
          "user_id INTEGER PRIMARY KEY AUTOINCREMENT, " \
          "username TEXT, " \
          "password TEXT," \
          "phone TEXT)"
    connection.execute(sql)
    connection.commit()
    connection.close()

# Datenbank Chats wird erstellt
def createChatsTable():
    connection = sqlite3.connect("database.db")
    sql = "CREATE TABLE IF NOT EXISTS chats(" \
          "chat_id INTEGER PRIMARY KEY AUTOINCREMENT, " \
          "user1_id INTEGER, " \
          "user2_id INTEGER)"
    connection.execute(sql)
    connection.commit()
    connection.close()

# Datenbank Nachrichten wird erstellt
def createMessagesTable():
    connection = sqlite3.connect("database.db")
    sql = "CREATE TABLE IF NOT EXISTS messages(" \
          "message_id INTEGER PRIMARY KEY AUTOINCREMENT, " \
          "chat_id INTEGER, " \
          "sender_id INTEGER, " \
          "message TEXT, " \
          "timestamp TIMESTAMP)"
    connection.execute(sql)
    connection.commit()
    connection.close()

class Database:
    def __init__(self):
        createUsersTable()
        createChatsTable()
        createMessagesTable()

    def query(self,sql):
        connection = sqlite3.connect("database.db")
        res = list(connection.execute(sql))
        connection.close()

        return res

   
    def getUsers(self):
        return self.query("SELECT * from users")

    def createMessage(self,input):
        sender,receiver, message = input

        sender_id = self.query("SELECT user_id FROM users WHERE username = '{}'".format(sender))[0][0]
        print(sender_id)
        chat_id = self.getChatID(sender,receiver)

        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        connection = sqlite3.connect("database.db")
        sql = "INSERT INTO  messages (chat_id,sender_id,message,timestamp) VALUES({},{},'{}','{}')".format(chat_id,sender_id,message,timestamp)
        connection.execute(sql)
        connection.commit()
        connection.close()

        return (True, "Message created.")

    #Chat mit anderen Nutzern erstellen
    def createChat(self, input):
        user1, user2 = input

        id1 = self.query("SELECT user_id FROM users WHERE username = '{}'".format(user1))[0][0]
        id2 = self.query("SELECT user_id FROM users WHERE username = '{}'".format(user2))[0][0]

        if not self.isChatAvailable(id1, id2):
            return (False, "Chat already exists.")
        else:
            connection = sqlite3.connect("database.db")
            sql = "INSERT INTO  chats (user1_id,user2_id) VALUES({},{})".format(id1, id2)
            connection.execute(sql)
            connection.commit()
            connection.close()

            return (True, "Chat created.")

    #Registierung User
    def registerUser(self,input):
        username,password_hash,phone = input

        if not self.isUsernameAvailable(username):
            return (False, "Username not available.")
        else:
            connection = sqlite3.connect("database.db")

            sql = "INSERT INTO  users (username,password,phone) VALUES('{}','{}','{}')".format(username,password_hash,phone)
            connection.execute(sql)
            connection.commit()

            connection.close()

            return (True, "Registering successful.")


    #Login überprüfen
    def loginUser(self, input):
        username,password_hash = input
        password_db_hash = self.query("SELECT password FROM users WHERE username = '{}'".format(username))

        if len(password_db_hash) == 0:
            return (False, "Username or password wrong.")
        else:
            password_db_hash = password_db_hash[0][0]

        if password_hash == password_db_hash:
            return (True, "Login successful.")
        else:
            return (False, "Username or password wrong.")

    def isUsernameAvailable(self,username):
        connection = sqlite3.connect("database.db")

        sql = "SELECT *     FROM users     WHERE username = '{}';".format(username)
        users = connection.execute(sql)
        num_of_registered_users = len(list(users))
        connection.close()

        return num_of_registered_users == 0

    #User überprüfen
    def isChatAvailable(self,id1,id2):
        ids1 = [id[0] for id in self.query("SELECT user2_id     FROM chats     WHERE user1_id = {};".format(id1))]
        ids2 = [id[0] for id in self.query("SELECT user1_id     FROM chats     WHERE user2_id = {};".format(id1))]

        print(ids1,ids2)

        return not(id2 in ids1 or id2 in ids2)

    
    def getChatID(self,user1,user2):
        user1_id = self.query("SELECT user_id FROM users WHERE username = '{}'".format(user1))[0][0]
        user2_id = self.query("SELECT user_id FROM users WHERE username = '{}'".format(user2))[0][0]

        maybe_chat_id_1 = self.query(
            "SELECT chat_id FROM chats WHERE user1_id = {} AND user2_id = {}".format(user1_id, user2_id))
        maybe_chat_id_2 = self.query(
            "SELECT chat_id FROM chats WHERE user2_id = {} AND user1_id = {}".format(user1_id, user2_id))
        maybe_chat_id_1.extend(maybe_chat_id_2)

        return maybe_chat_id_1[0][0]

    #Nachrichten empfangen
    def getMessages(self,input):
        user1,user2 = input

        print(input,user1,user2)

        user1_id = self.query("SELECT user_id FROM users WHERE username = '{}'".format(user1))[0][0]
        chat_id = self.getChatID(user1,user2)

        messages = self.query("SELECT sender_id,message, timestamp from messages WHERE chat_id={} ORDER BY timestamp ASC".format(chat_id))
        print(messages)

        return (True, (user1_id,messages) )

    #Erstellte Chats
    def getChats(self,input):
        user = input

        user_id = self.query("SELECT user_id FROM users WHERE username = '{}'".format(user))[0][0]
        contact_ids_1 = self.query("SELECT user1_id FROM chats WHERE user2_id = {}".format(user_id))
        contact_ids_2 = self.query("SELECT user2_id FROM chats WHERE user1_id = {}".format(user_id))
        contact_ids = contact_ids_1 + contact_ids_2
        contact_ids = [id[0] for id in contact_ids]

        print(contact_ids)

        return (True,contact_ids)

    
    def getUsernames(self,input):
        user = input
        success, contact_ids = self.getChats(user)
        usernames = []
        for id in contact_ids:
            print("id: ", id, "name: ", self.query("SELECT username FROM users WHERE user_id = '{}'".format(id)))
            username = self.query("SELECT username FROM users WHERE user_id = '{}'".format(id))[0][0]
            usernames.append(username)
        
        print(usernames)

        return (True,usernames)

    #Speichern von Bildern
    def storeFile(self, input):
        user, partner, file = input

        chat_id = self.getChatID(user,partner)

        folder_name = './{}'.format(chat_id)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        _, _, folder_files = next(os.walk(folder_name))
        file_name = str(len(folder_files))
        file.save("{}/{}.jpg".format(folder_name,file_name))

        return self.createMessage((user, partner, "{}.jpg".format(file_name)))

    #Bilder empfangen
    def getFile(self, input):
        user, partner, file_name = input

        chat_id = self.getChatID(user,partner)

        file_path = './{}/{}'.format(chat_id,file_name)
        file = Image.open(file_path)

        return (True, file)

    #Username suchen
    def getUsernames(self, input):
        user = input
        success, contact_ids = self.getChats(user)
        usernames = []
        for id in contact_ids:
            print("id: ", id, "name: ", self.query("SELECT username FROM users WHERE user_id = '{}'".format(id)))
            username = self.query("SELECT username FROM users WHERE user_id = '{}'".format(id))[0][0]
            usernames.append(username)

        print(usernames)

        return (True, usernames)

    
    




