import socket, ssl

HOST, PORT = '127.0.0.1', 443

def send_message(conn):
	
    user = input("\nEnter your username: ")
    password = input("\nEnter your password: ")
    message = input("\nEnter the message you want to send: ")

    total_message = user + ":" + password + ":" + message
    conn.send(total_message.encode())
    print(conn.recv(1024).decode())

def main():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode=ssl.CERT_NONE
    context.set_ciphers('AES256+SHA384')

    conn = context.wrap_socket(sock, server_hostname=HOST)

    try:
        conn.connect((HOST, PORT))
        check_conn = conn.recv(1024)
        print('\n' + check_conn.decode())
        send_message(conn)
    finally:
        conn.close()

if __name__ == '__main__':
    main()