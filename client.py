import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox


HOST = '127.0.0.1'
PORT = 1234

DARK_GREY = '#0d0e0f'
MEDIUM_GREY = '#363a3a'
LIGHT_BLUE = '#7B68EE'
WHITE = 'white'
FONT = ("Helvetica, 10")
SMALL_FONT = ("Helvetica, 7")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():
    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())  # send mes to server
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())  # utf-8 default
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

root = tk.Tk()
root.geometry("600x600")
root.title("ikrokegb messenger")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text='Enter username: ', font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=28)
username_textbox.pack(side=tk.LEFT)
username_textbox.config(highlightthickness=0, bd=0)

username_button = tk.Button(top_frame, text='Join', font=FONT, bg=LIGHT_BLUE, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=10)
username_button.config(highlightthickness=0, bd=0)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=41)
message_textbox.pack(side=tk.LEFT, padx=10)
message_textbox.config(highlightthickness=0, bd=0)

message_textbox.pack(side=tk.LEFT, padx=10)
message_textbox.config(highlightthickness=0, bd=0)

message_button = tk.Button(bottom_frame, text='Send', font=FONT, bg=LIGHT_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=2, pady=2)
message_button.config(highlightthickness=0, bd=0)

message_box = scrolledtext.ScrolledText(middle_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=50, height=23)
message_box.config(highlightthickness=0, bd=0)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)


def listen_for_messages_from_server(client):

    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]  #name~message
            content = message.split("~")[1]
            add_message(f"[{username}] {content}")
        else:
            messagebox.showerror("Error", "Message received from client is empty")


def main():

    root.mainloop()

if __name__ == "__main__":
    main()