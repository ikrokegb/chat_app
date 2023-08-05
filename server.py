import socket
import threading
import tkinter as tk

DARK_GREY = '#0d0e0f'
MEDIUM_GREY = '#363a3a'
LIGHT_PURPLE = '#f4d8ff'
WHITE = 'white'
FONT = ("Helvetica, 10")
SMALL_FONT = ("Helvetica, 7")

def connect():
    print("Button is working")

root = tk.Tk()
root.geometry("600x600")
root.title("ikrokegb messenger")
#root.resizable(False, False)

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

HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = [] #connected users


def listen_for_messages(client, username):

    while 1:

        message = client.recv(2048).decode('utf-8') # listen messeges
        if message != '':

            final_message = username + '~' + message #name~mes
            send_messages_to_all(final_message)
        else:
            print(f'The message send from client {username} is empty')


def send_message_to_client(client, message): #for one client

    client.sendall(message.encode())  #utf-8 default


def send_messages_to_all(message):

    for user in active_clients:

        send_message_to_client(user[1], message)


def client_handler(client):
    while 1:

        username = client.recv(2048).decode('utf-8') # listen username
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} added to the chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username, )).start()


def main():

    root.mainloop()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #1 - IPv4    2 - TCP

    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except socket.error as e:
        print(e)
        #print(f'Unable to bind to host {HOST} and port {PORT} ')

    server.listen(LISTENER_LIMIT)

    while 1:

        client, address = server.accept()
        print(f"Succesfully connected to client {address[0]}, {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == "__main__":
    main()