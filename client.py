import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

DARK_GREY = '#0d0e0f'
MEDIUM_GREY = '#363a3a'
LIGHT_BLUE = '#7B68EE'
WHITE = 'white'
FONT = ("Helvetica, 10")
SMALL_FONT = ("Helvetica, 7")

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():
    print("Button is working")

def send_message():
    print("Sending message")

root = tk.Tk()
root.geometry("600x600")
root.title("ikrokegb messenger")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height= 100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height= 400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height= 100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text='Enter username: ', font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=26)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text='Join', font=FONT, bg=DARK_GREY, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=12)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=39)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text='Send', font=FONT, bg=LIGHT_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=15)

message_box = scrolledtext.ScrolledText(middle_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=23)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)

HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = [] #connected users


def listen_for_messages_from_server(client):

    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]  #name~message
            content = message.split("~")[1]
            print(f"[{username}] {content}")
        else:
            print("Message received from client is empty")


def send_message_to_server(client):

    while 1:

        message = input("Message: ")
        if message != '':
            client.sendall(message.encode()) #utf-8 default
        else:
            print("Empty message")
            exit(0)


def communicate_to_server(client):

    username = input("Enter username: ")
    if username != '':
        client.sendall(username.encode()) #send mes to server
    else:
        print("Username cannot be empty")
        exit(0)

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

    send_message_to_server(client)


def main():

    root.mainloop()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server")
    except:
        print(f"Unable to connect to server {HOST} {PORT}")

    communicate_to_server(client)

if __name__ == "__main__":
    main()