from threading import Thread
from socket import socket
from Helpers.Logger import Logger
from Helpers.Reader import Reader
from Packets.Messages.Client.HelloMessage import Hello
from Packets.Messages.Client.AuthenticationMessage import Authentificate
import Helpers.Cryptography as crypto
import time


class Client(Thread):
    
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.major = self.data['Major']
        self.ip = self.data['IP']
        self.port = self.data['Port']
        self.seed = 1943172040 #хоть рандомом инициализируй
        self.client_sk, self.client_pk = crypto.get_keys(self.seed)
        self.server_pk = b'\xc4\x1cH.\xa2\xbb\xb5\x12\x19\xdd\x1a&p\x96\x0fG\tF.\xc4\xfd\xb6\xe7\xb6e!\xddU\xf37\xe69'
        self.nonce = crypto.get_nonce(self.client_pk, self.server_pk)

    def run(self):
        while True:

            self.socket = socket()
        
            Logger.LogServer(self, 'Connection to {}:{}'.format(self.ip, self.port))
            self.socket.connect((self.ip, self.port))

            hello = Hello.GetHeaderPacket(self, self.major, self.seed)
            self.socket.send(hello)
            Logger.LogServer(self, 'Sended 10100!')
            key = self.socket.recv(1024)[11:]

            auth = Authentificate.GetHeaderPacket(self, self.client_pk, self.client_sk, self.server_pk, self.nonce, key)
            self.socket.send(auth)
            Logger.LogServer(self, 'Sended 10101!')

            time.sleep(1/10)