import socket
import socket, ssl
from _thread import *
from threading import Thread
from time import sleep

connections=0
HOST, PORT = '127.0.0.1', 443
n_con = input("Insert the number of simultaneous connections to create: ")

def stress():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode=ssl.CERT_NONE
    context.set_ciphers('AES256+SHA384')
    conn = context.wrap_socket(sock, server_hostname=HOST)
    conn.connect((HOST, PORT))
    while True:
        sleep(1)

if __name__ == '__main__':
    try:
        for i in range(int(n_con)):
            sleep(0.1)
            t = Thread(target=stress)
            t.start()
            connections+=1
            print("[+] Number of simultaneous connections: " + str(connections))
    except:
        print("Insert a valid number")