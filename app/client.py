from app.server import HEADER_LENGTH
import socket
import select
import errno

HEADER_LENGTH = 10
IP = "100.116.154.43"
PORT = 1337

my_username = input("Username :")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

