import socket, ssl, os
from _thread import *

CERT_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../utils/mycert.pem"

def recv_message(conn):
    login = conn.recv(1024)
    conn.send(b'\n[+] Login successful!')

    message = conn.recv(1024)
    print('\n[*] Message received: ' + message.decode())
    conn.send(b'\n[+] Message received!')

if __name__ == '__main__':

  thread_count = 0
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
  try:
    sock.bind(('', 443))
  except socket.error as e:
    print(str(e))

  print('\n[+] Waiting for client connection...')
  sock.listen(5)

  context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
  context.load_cert_chain(certfile=CERT_PATH) 
  context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2 | ssl.OP_NO_COMPRESSION
  context.set_ciphers('AES256+SHA384')

  def threaded_client(connection):
    try:
      conn = context.wrap_socket(client, server_side=True)
      conn.send(b'[+] Connection accepted!')
      recv_message(conn)
      # ------- Only 1 message -------
      conn.close()
      exit() #Kill thread
    except ssl.SSLError as e:
      print(e)

while True:
  client, addr = sock.accept()
  print('\n[+] Connected to: ' + addr[0] + ':' + str(addr[1]))
  thread_id=start_new_thread(threaded_client, (client, ))
  print('User thread: ' + str(thread_id))