import socket # Sockets are used to handle the data sent to and from the host machine
import select # Select ensures that the program will run as intended across multiple operating systems

HEADER_LENGTH = 10
IP = '100.116.154.43'
PORT = 1337

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow for the server to reestablish connection to port and address 

server_socket.bind((IP, PORT)) # Set the socket connection to configured IP and PORT

server_socket.listen()


