import socket, ssl, os

CERT_PATH = os.path.dirname(os.path.abspath(__file__)) + "../utils/mycert.pem"

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.load_cert_chain(certfile=CERT_PATH) 

def recv_message(conn):
    conn.recv(1024)
    conn.send(b'\n[+] Message received!')

while True:
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
  sock.bind(('', 443))
  print('\n[+] Waiting for client connection...')
  sock.listen(5)

  context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
  context.load_cert_chain(certfile="mycert.pem") 
  context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2 | ssl.OP_NO_COMPRESSION
  context.set_ciphers('AES256+SHA384')
  
  while True:
    client, addr = sock.accept()
    print('[+] Connection accepted!')
    try:
      conn = context.wrap_socket(client, server_side=True)
      recv_message(conn)
    except ssl.SSLError as e:
      print(e)
    finally:
      if conn:
        conn.close()