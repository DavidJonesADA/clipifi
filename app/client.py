import socket
import select
import errno
import sys
import time
from threading import Thread
import time
import pyperclip
import threading

HEADER_LENGTH = 10
IP = "100.116.154.43"
PORT = 1337

my_username = input("Username :")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)


def recieveCall():
    while True:
        try:
            while True:

                username_header = client_socket.recv(HEADER_LENGTH)
                if not len(username_header):
                    print("Connection closed by the server")
                    sys.exit()

                username_length = int(username_header.decode('utf-8').strip())
                username = client_socket.recv(username_length).decode('utf-8')

                message_header = client_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                message = client_socket.recv(message_length).decode('utf-8')
                
                pyperclip.copy(message)
                continue

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print ('Reading error', str(e))
                sys.exit()
            continue

        except Exception as e:
            print ('General Error', str(e))
            sys.exit()

def sendCall():
    while True:
        message = input(f"{my_username} > ")

        if message:
            message = message.encode("utf-8")
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
            client_socket.send(message_header + message)

def print_to_stdout(clipboard_content):
    message = clipboard_content.encode("utf-8")
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
    client_socket.send(message_header + message)


class ClipboardWatcher(threading.Thread):
    def __init__(self, predicate, callback, pause=5.):
        super(ClipboardWatcher, self).__init__()
        self._predicate = predicate
        self._callback = callback
        self._pause = pause
        self._stopping = False

    def run(self):       
        recent_value = ""
        while not self._stopping:
            tmp_value = pyperclip.paste()
            if tmp_value != recent_value:
                recent_value = tmp_value
                if self._predicate(recent_value):
                    self._callback(recent_value)
            time.sleep(0.5)

    def stop(self):
        self._stopping = True





th = Thread(target=recieveCall)
th.start()

watcher = ClipboardWatcher(print_to_stdout, 1.)
watcher.start()





