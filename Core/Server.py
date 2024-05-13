from Core.Client import Client
from Helpers.Logger import Logger
from socket import socket

class Server(object):
    
    def __init__(self, data):
        self.data = data
        self.ip = self.data['IP']
        self.port = self.data['Port']
        self.thread_count = self.data['ThreadCount']
        self.socket = socket()
        
    def Start(self):
        is_connected = False
        server = self.socket
        Logger.LogServer(self, 'Awaiting connection to {}:{} ...'.format(self.ip, self.port))
        while not is_connected:
            try:
                server.connect((self.ip, self.port))
                is_connected = True
            except:
                Logger.LogServer(self, 'Server {}:{} is not connected!'.format(self.ip, self.port))
                continue
        Logger.LogServer(self, 'Server {}:{} is connected!'.format(self.ip, self.port))
        server.close()
        server = self.socket
        for _ in range(self.thread_count):
            Client(self.data).start()