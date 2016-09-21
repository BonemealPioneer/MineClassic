import socket
import sys
from struct import pack, unpack_from, calcsize
from SocketServer import ThreadingTCPServer, BaseRequestHandler

class DataBuffer(object):
    __slots__ = (
        '_buffer', '_offset')

    def __init__(self, data=b'', offset=0):
        self._buffer = data
        self._offset = offset

    def bytes(self):
        return self.buffer

    def remaining(self):
        return self.buffer[self.offset:]

    @property
    def buffer(self):
        return self._buffer

    @buffer.setter
    def buffer(self, buffer):
        self._buffer = buffer

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        self._offset = offset

    def write(self, data):
        self.buffer += data

    def read(self, length):
        data = self.buffer[self.offset:][:length]; self.offset += length; return data

    def pack(self, fmt, *args):
        return pack('!%s' % (fmt), *args)

    def unpack(self, fmt):
        data = unpack_from('!%s' % (fmt), self.buffer, self.offset); self.offset += calcsize(
            '!%s' % (fmt)); return data

class RequestHandler(BaseRequestHandler):
    BUFFER_SIZE = 1024

    def setup(self):
        pass

    def handle(self):
        while True:
            try:
                data = self.request.recv(self.BUFFER_SIZE)
            except socket.error:
                break

            if not data:
                break

            data_buffer = DataBuffer()

    def finish(self):
        self.request.close()

class TCPServer(ThreadingTCPServer):
    allow_reuse_address = True; request_queue_size = 256

    def serve_forever(self, poll_interval=0.01):
        ThreadingTCPServer.serve_forever(self, poll_interval)

if __name__ == '__main__':
    server = TCPServer(('0.0.0.0', 25565), RequestHandler)
    server.serve_forever()