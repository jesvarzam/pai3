import socket, ssl

HOST, PORT = '127.0.0.1', 443

def send_message(conn):
    user = input("\n Enter your username: ")
    password = input("\n Enter your password: ")
    message = input("\n Enter the message you want to send: ")

    total_message = user + ":" + password + ":" + message
    conn.send(total_message.encode())
    print(conn.recv().decode())

def main():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode=ssl.CERT_NONE

    #context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 
    context.set_ciphers('AES256+SHA384')
    conn = context.wrap_socket(sock, server_hostname=HOST)

    try:
        conn.connect((HOST, PORT))
        send_message(conn)
    finally:
        conn.close()

if __name__ == '__main__':
    main()