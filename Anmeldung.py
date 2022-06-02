import tkinter as tk
import os, sys, sqlite3

#Datenbank wird erstellt
def createDatabase():
    connection = sqlite3.connect("user.db")
    sql = "CREATE TABLE IF NOT EXISTS user("       
    "pk INTEGER PRIMARY KEY AUTOINCREMENT, "     
    "username TEXT, " \
    "password TEXT)"
    connection.execute(sql)
    connection.commit()
    connection.close()

#Test ob User korrekt registriert werden können
def getAllUser():
    connection = sqlite3.connect("user.db")
    sql = "SELECT * from user"
    users = connection.execute(sql)
    for user in users:
        print(user)
    connection.commit()
    connection.close()

#Registierung User
def registerUser(username):
    
    if not isUsernameAvailable(username):
        #return (False, "Username not available.")
        print((False, "Username not available."))
    else:
        connection = sqlite3.connect("user.db")

        sql = "INSERT INTO  user (username) VALUES('{}')".format(username)
        connection.execute(sql)
        connection.commit()

        connection.close()
        
        #return (True, "Registering successful.")
        print((True, "Registering successful."))


#Login überprüfen       
def loginUser(username):
    if not isUsernameAvailable(username):
        #return (False, "Username not available.")
        print((True, "Login successful."))
    else:
        print((False, "Account not registered."))
    
#Mit Datenbank verbinden   
def isUsernameAvailable(username):
    connection = sqlite3.connect("user.db")
    
    sql = "SELECT *     FROM user     WHERE username = '{}';".format(username)
    users = connection.execute(sql)
    num_of_registered_users = len(list(users))
    connection.close()
    
    return num_of_registered_users == 0


#Register Screen
def register(root):
    register_screen = tk.Toplevel(root)
    register_screen.title("Register")
    
    tk.Label(register_screen, text="Username").grid(row=0)
    tk.Label(register_screen, text="Password").grid(row=1)
    tk.Label(register_screen, text="Telephonenumber").grid(row=2)
    e1 = tk.Entry(register_screen)
    e2 = tk.Entry(register_screen)
    e3 = tk.Entry(register_screen)
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e2.grid(row=2, column=1)
    
    tk.Button(register_screen, text="Register",command = lambda: registerUser(e1.get())).grid(row=3)

#Login Screen
def login():
    login_screen = tk.Toplevel(root)
    login_screen.title("Login")
    
    tk.Label(login_screen, text="Username").grid(row=0)
    tk.Label(login_screen, text="Password").grid(row=1)
    e1 = tk.Entry(login_screen)
    e2 = tk.Entry(login_screen)
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    
    tk.Button(login_screen, text="Login",command = lambda: loginUser(e1.get())).grid(row=2)

#Hauptscreen
def main_screen(root):
    root.geometry("400x350")
    root.title("Messages")
    tk.Label(text = "Messages", bg= "purple", font= ("Arial", 12)).pack()
    tk.Label(text= "").pack()
    tk.Button(text= "Login", height = "2", width = "30", command = login).pack()
    tk.Label(text= "").pack()
    tk.Button(text= "Register", height = "2", width = "30", command = lambda : register(root)).pack()
    
    root.mainloop()


root = tk.Tk()
root.title("Messages")
main_screen(root)

#Datenbank Anmeldung (Test ob Registierung funktioniert)
if os.path.exists("anmeldung.db"):
      print("Datei bereits vorhanden")
      sys.exit(0)
connection = sqlite3.connect("anmeldung.db")

sql = "CREATE TABLE IF NOT EXISTS anmeldung(" \
      "pk INTEGER PRIMARY KEY AUTOINCREMENT, "\
      "username TEXT, " \
      "password TEXT, " \
      "telephonenumber TEXT)"
connection.execute(sql)

sql = "INSERT INTO  anmeldung (username, password, telephonenumber) VALUES('eiswaffel02', " \
      "'python9', '01579318')"
connection.execute(sql)
connection.commit()

sql = "INSERT INTO anmeldung (username, password, telephonenumber) VALUES('butterfly5', " \
      "'helloworld123', '017843928')"
connection.execute(sql)
connection.commit()

sql = "UPDATE MYTable SET data = 'changeddata' WHERE pk = 1"
connection.execute(sql)
connection.commit()

connection.close()











#success, message = registerUser("name")
#getAllUser()
#createDatabase()





