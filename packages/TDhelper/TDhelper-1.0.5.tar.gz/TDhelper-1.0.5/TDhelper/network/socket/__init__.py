import socket
from TDhelper.network.socket.model.SOCKET_MODELS import SOCKET_TYPE, SOCKET_EVENT
from TDhelper.Event.Event import *


class base(Event):
    def __init__(self):
        self.__mysocket = None
        self._socket_type = SOCKET_TYPE.TCPIP
        super(base, self).__init__()

    def createsocket(self, sType=SOCKET_TYPE.TCPIP):
        self._socket_type = sType
        if self._socket_type == SOCKET_TYPE.TCPIP:
            self.__mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.__mysocket.setsockopt(socket.SOL___mysocket,socket.SO_REUSEADDR,1)
        else:
            self.__mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # self.__mysocket.setsockopt(socket.SOL___mysocket,socket.SO_REUSEADDR,1)

    def setTimeout(self, timeout):
        self.__mysocket.settimeout(timeout)

    def bind(self, uri):
        if self.__mysocket:
            self.__mysocket.bind(uri)

    def listen(self, count):
        if self.__mysocket:
            self.__mysocket.listen(count)

    def accept(self):
        return self.__mysocket.accept()

    def recv(self, connect, recvLen=100):
        if self._socket_type == SOCKET_TYPE.TCPIP:
            return connect.recv(recvLen)
        else:
            try:
                return self.__mysocket.recvfrom(recvLen)
            except Exception as e:
                raise Exception(e)
        
    def send(self, connect, buff):
        if self._socket_type == SOCKET_TYPE.TCPIP:
            connect.send(buff)
        else:
            self.__mysocket.sendto(buff, connect)

    def connection(self, uri):
        self.__mysocket.connect(uri)

    def getSocket(self):
        return self.__mysocket

    def close(self):
        # self.___mysocket.shutdown(socket.SHUT_RDWR)
        self.__mysocket.close()
