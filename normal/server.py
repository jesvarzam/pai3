import socket, ssl, os

CERT_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../utils/mycert.pem"

def recv_message(conn):
    message = conn.recv(1024)
    print('\n[*] Message received: ' + message.decode())
    conn.send(b'\n[+] Message received!')

if __name__ == '__main__':
  
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
  sock.bind(('', 443))
  print('\n[+] Waiting for client connection...')
  sock.listen(5)

  context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
  context.load_cert_chain(certfile=CERT_PATH) 
  context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2 | ssl.OP_NO_COMPRESSION
  context.set_ciphers('AES256+SHA384')
  
  while True:
    client, addr = sock.accept()
    print('\n[+] Connection received from {}'.format(addr))
    try:
      conn = context.wrap_socket(client, server_side=True)
      conn.send(b'[+] Connection accepted!')
      recv_message(conn)
    except ssl.SSLError as e:
      print(e)
    finally:
      if conn:
        conn.close()