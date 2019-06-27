import socket
from pathlib import Path
import sys
import time


class Client:
    def __init__(self, name, sock=None):
        self.name = name
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))
        self.sock.sendall(bytes(self.name, 'utf8'))

    def mysend(self, msg):
        self.sock.sendall(msg)

    def myrecive(self, textArea, usersNames):
        while True:
            try:
                msg = self.sock.recv(1024).decode("utf8")
                if msg.startswith('list'):
                    usersNames.append(msg[4:])
                    usersNames = list(set(usersNames))
                else:
                    textArea.append(msg)
            except OSError:
                break

    def getUsers(self):
        return self.usersNames

