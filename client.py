import socket
import threading


nickname = input('choose a nickname: ')
if nickname == 'admin':
    password = input("Enter password for admin: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))

stop_thread = False

def receive():
    while 1:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    if client.send(password.encode('ascii')) == 'REFUSE':
                        print("Connection was refused! Wrong password.")
                        stop_thread = True
            else:
                print(message)
        except:
            print('An error occurred')
            client.close()
            break



def write():
    while 1:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
