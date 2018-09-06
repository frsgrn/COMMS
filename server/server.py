import socket
from threading import Thread
import select
from message import *
from collections import deque
import sys
from router import route

HOST=''
PORT=8888
TIMEOUT=60
BUFSIZ=1024

class Session():
    def __init__(self, ip, port, connection, server):
        self.ip = ip
        self.port = port
        self.connection = connection
        self.server = server
    
    def send_message(self, message):
        self.server.send_message(message)

class Server():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sessions = {}
        self.connections = {}
        self.outgoing = deque()

    def listen(self):
        try:
            self.socket.bind((HOST, PORT))
        except:
            sys.exit()
        self.socket.listen(PORT)
        Thread(target=self.t_find_connections).start()
        Thread(target=self.t_broadcast).start()

    def send_message(self, message):
        self.outgoing.append(message)

    def t_find_connections(self):
        while True:
            readable,_,_ = select.select([self.socket], [], [])
            for s in readable:
                connection, addr = s.accept()
                session = Session(addr[0], addr[1], connection, self)
                self.sessions[connection] = session
                self.connections[session] = connection
                Thread(target=t_handle_connection, args=(self, connection)).start()

    def t_broadcast(self):
        while True:
            if len(self.connections) > 0 and len(self.outgoing) > 0:
                _,writeable,_ = select.select([], self.connections.values(), [], TIMEOUT)
                response = self.outgoing[0]
                for sock in writeable:
                    response.send_to(sock)
                self.outgoing.popleft()


def on_request(session, raw):
        request = Request.parse_request(raw)
        if request == None:
            return
        route(session, request)

def t_handle_connection(server, connection):
    while True:
        data = None
        try:
            data = connection.recv(BUFSIZ)
        except:
            data = None
        if not data:
            del server.connections[server.sessions[connection]]
            del server.sessions[connection]
            connection.close()
            break
        on_request(server.sessions[connection], data.decode())