import tkinter as tk
from tkinter import messagebox
from PIL import Image,ImageTk
import time
from threading import Thread
from Connection import Connection

#
class Application:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Messages")
        self.bt_chat = tk.Button(text="Search", height="2", width="30")
        self.bt_message = tk.Button(text="Messages", height="2", width="30")

        self.conn = Connection()
        self.user = None
        self.images = []

    #Fehlermeldung
    def createErrorWindow(self,message):
        messagebox.showerror("Fehlermeldung", message)

    #Register Screen
    def createRegisterWindow(self):
        register_screen = tk.Toplevel(self.root)
        register_screen.title("Register")

        tk.Label(register_screen, text="username").grid(row=0)
        tk.Label(register_screen, text="password").grid(row=1)
        tk.Label(register_screen, text="phone number").grid(row=2)
        e1 = tk.Entry(register_screen)
        e2 = tk.Entry(register_screen)
        e3 = tk.Entry(register_screen)

        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)
        e3.grid(row=2, column=1)

        tk.Button(register_screen, text="Register",command = lambda: self.conn.sendRequest(("register",(e1.get(),e2.get(),e3.get())))).grid(row=3)

    #Login Screen
    def createLoginWindow(self):
        login_screen = tk.Toplevel(self.root)
        login_screen.title("Login")

        tk.Label(login_screen, text="Username").grid(row=0)
        tk.Label(login_screen, text="Password").grid(row=1)
        e1 = tk.Entry(login_screen)
        e2 = tk.Entry(login_screen)
        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)

        #Login Nachfrage
        def login_request(input):
            _,login = input
            user = login[0]

            success,message = self.conn.sendRequest(input)
            if success:
                self.bt_chat["state"] = "normal"
                self.bt_message["state"] = "normal"
                self.user = user
            else:
                self.bt_chat["state"] = "disabled"
                self.bt_message["state"] = "disabled"
                self.user = None
                self.createErrorWindow(message)

        tk.Button(login_screen, text="Login", command=lambda: login_request(("login", (e1.get(), e2.get())))).grid(row=2)

    # Login Screen
    def createMessageWindow(self):
        message_screen = tk.Toplevel(self.root)
        message_screen.title("Messages")

        _,OPTIONS = self.conn.sendRequest(("get_usernames", (self.user)))

        variable = tk.StringVar(message_screen)
        variable.set(OPTIONS[0]) # default value
        tk.OptionMenu(message_screen, variable, *OPTIONS).grid(row=0)

        tk.Label(message_screen, text="message").grid(row=1)
        e2 = tk.Entry(message_screen)
        e3 = tk.Entry(message_screen)
        e4 = tk.Entry(message_screen)

        e2.grid(row=1, column=1)
        e3.grid(row=3, column=1)
        #e4.grid(row=4, column=1)

        
        tk.Button(message_screen, text="Send message", command=lambda: self.conn.sendRequest(("message", (self.user,variable.get(),e2.get())))).grid(
            row=2)
        tk.Button(message_screen, text="Send file", command=lambda: self.conn.sendRequest(("send_file", (self.user,variable.get(),e3.get())))).grid(
            row=3)

        txtMessages = tk.Text(message_screen, width=50)
        txtMessages.grid(row=0, column=2, padx=10, pady=10)

        #Bilder empfangen
        def getImage(user,partner,file_path,txtMessages):
            success, file = self.conn.sendRequest(("get_file", (user, partner, file_path)))
            self.images.append(ImageTk.PhotoImage(file))
            txtMessages.image_create(tk.END, image=self.images[0])  # Example 1
            file.save("test.jpg")

        #Nachrichten empfangen
        def getMessages(user,partner):
            return self.conn.sendRequest(("get_messages", (user, partner)))

        def updateMessages(txtMessages,get_messages_response):
            txtMessages.delete('1.0', tk.END)
            id,messages = get_messages_response
            self.images = []
            self.image_num = 0

            image_count = 0
            for i,m in enumerate(messages):
                user_id,message,t = m

                if id == user_id:
                    txtMessages.insert(tk.INSERT, "\t\t\t" + self.user + ": ")
                else:
                    txtMessages.insert(tk.INSERT, variable.get() + ": ")

                if ".jpg" in message:

                    success, file = self.conn.sendRequest(("get_file", (self.user, variable.get(), message)))
                    img  = file.resize((150, 150))
                    img = ImageTk.PhotoImage(img)
                    self.images.append(img)

                    image_start = txtMessages.index(tk.INSERT)
                    tag = "{}".format(i)
                    print("Tag: {}".format(tag))
                    txtMessages.image_create(image_start, image=img)
                    image_end = txtMessages.index(tk.INSERT)
                    print(image_start, image_end)

                    txtMessages.tag_add(tag, image_start,image_end)


                    def on_click(event, file=file, index=image_count):
                        file.save("{}.jpg".format(index))
                        messagebox.showinfo(title="Download", message="Bild erfolgreich heruntergeladen.")

                    txtMessages.tag_bind(tag, "<Button-1>", on_click)

                    image_count += 1

                else:
                    txtMessages.insert(tk.INSERT,message)

                txtMessages.insert(tk.INSERT, "\n")

        #Automatisierung
        def automaticUpdate(txtMessages,user, partner_variable):
            print("Thread start")
            #time.sleep(3)
            num_messages = -1
            partner = partner_variable.get()
            try:
                while True:
                    txtMessages.get("1.0", "1.1")

                    success,res = getMessages(user, partner)
                    _,messages = res

                    if num_messages < len(messages):
                        num_messages = len(messages)
                        updateMessages(txtMessages,res)

                    if partner != partner_variable.get():
                        num_messages = -1
                        partner = partner_variable.get()

                    time.sleep(1)
            except Exception as e:
                print("Thread ended.")
                print(str(e))

        thread = Thread(target=automaticUpdate,args=(txtMessages,self.user,variable,))
        thread.start()
    


    # Login Screen
    def createChatWindow(self):
        chat_screen = tk.Toplevel(self.root)
        chat_screen.title("Search")

        tk.Label(chat_screen, text="user").grid(row=0)
        e1 = tk.Entry(chat_screen)

        e1.grid(row=0, column=1)

        tk.Button(chat_screen, text="Create chat", command=lambda: self.conn.sendRequest(("chat", (self.user, e1.get())))).grid(row=1)

    #Hauptscreen
    def start(self):
        self.root.geometry("400x400")
        self.root.title("LetsChat")
        tk.Label(text = "LetsChat", bg= "orange", font= ("Arial", 12)).pack()
        tk.Label(text= "").pack()
        tk.Button(text= "Login", height = "2", width = "30", command = self.createLoginWindow).pack()
        tk.Label(text= "").pack()
        tk.Button(text= "Register", height = "2", width = "30", command = self.createRegisterWindow).pack()
        tk.Label(text="").pack()

        self.bt_chat["state"] = "disabled"
        self.bt_chat.configure(command=self.createChatWindow)
        self.bt_chat.pack()

        tk.Label(text= "").pack()

        self.bt_message.configure(command=self.createMessageWindow)
        self.bt_message["state"] = "disabled"
        self.bt_message.pack()



        self.root.mainloop()