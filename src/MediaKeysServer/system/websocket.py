'''
    Websocket.py
    
    Created on 2011-08-08
    
    hybi-10:  sec-websocket-key
    "For this header, the server has to take the value (as present in the
   header, e.g. the base64-encoded [RFC4648] version minus any leading
   and trailing whitespace), and concatenate this with the GUID
   "258EAFA5-E914-47DA-95CA-C5AB0DC85B11" in string form, which is
   unlikely to be used by network endpoints that do not understand the
   WebSocket protocol.  A SHA-1 hash (160 bits), base64-encoded (see
   Section 4 of [RFC4648]), of this concatenation is then returned in
   the server's handshake [FIPS.180-2.2002]."
    
'''
import struct
import socket
import re
import logging
from select import select
import hashlib
import base64

logging.basicConfig(level=logging.DEBUG)

class WebSocket(object):
    
    ## hybi-10
    GUID="258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    
    handshake = (
        "HTTP/1.1 101 Web Socket Protocol Handshake\r\n"
        "Upgrade: WebSocket\r\n"
        "Connection: Upgrade\r\n"
        "WebSocket-Origin: %(origin)s\r\n"
        "WebSocket-Location: ws://%(bind)s:%(port)s/\r\n"
        "Sec-Websocket-Origin: %(origin)s\r\n"
        "Sec-Websocket-Location: ws://%(bind)s:%(port)s/\r\n"
        "\r\n"
    )
    
    handshake_10 = (
        "HTTP/1.1 101 Switching Protocols\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        "Sec-WebSocket-Protocol: chat\r\n"
        "Sec-Websocket-Accept: %(accept)s\r\n"
        "Sec-Websocket-Origin: %(origin)s\r\n"
        "Sec-Websocket-Location: ws://%(bind)s:%(port)s/\r\n"
        "\r\n"
    )
    
    def __init__(self, client, server):
        self.client = client
        self.server = server
        self.handshaken = False
        self.header = ""
        self.data = ""

    def feed(self, data):
        if not self.handshaken:
            self.header += data
            if self.header.find('\r\n\r\n') != -1:
                parts = self.header.split('\r\n\r\n', 1)
                self.header = parts[0]
                if self.dohandshake(self.header, parts[1]):
                    #logging.info("Handshake successful")
                    self.handshaken = True
        else:
            #print "data: %s" % data
            self.data += data
            msgs = self.data.split('\xff')
            self.data = msgs.pop()
            for msg in msgs:
                if msg[0] == '\x00':
                    self.onmessage(msg[1:])

    digitRe = re.compile(r'[^0-9]')
    spacesRe = re.compile(r'\s')

    def dohandshake(self, header, key=None):
        #logging.debug("Begin handshake: %s" % header)
        part_1 = part_2 = origin = None
        
        ## hybi-10
        part_3 = None
        
        for line in header.split('\r\n')[1:]:
            name, value = line.split(': ', 1)
            
            #print "name(%s) value(%s)" % (name, value)
            
            if name.lower() == "sec-websocket-key1":
                key_number_1 = int(self.digitRe.sub('', value))
                spaces_1 = len(self.spacesRe.findall(value))
                if spaces_1 == 0:
                    return False
                if key_number_1 % spaces_1 != 0:
                    return False
                part_1 = key_number_1 / spaces_1
            elif name.lower() == "sec-websocket-key2":
                key_number_2 = int(self.digitRe.sub('', value))
                spaces_2 = len(self.spacesRe.findall(value))
                if spaces_2 == 0:
                    return False
                if key_number_2 % spaces_2 != 0:
                    return False
                part_2 = key_number_2 / spaces_2
            elif name.lower() == "origin":
                origin = value
            elif name.lower() == "sec-websocket-key":
                part_3=value.rstrip().lstrip()
                part_3=part_3+self.GUID
                part_3=hashlib.sha1(part_3)
                part_3=base64.b64encode(part_3.digest())                
                
        if part_1 and part_2:
            #logging.debug("Using challenge + response")
            challenge = struct.pack('!I', part_1) + struct.pack('!I', part_2) + key
            response = hashlib.md5(challenge).digest()
            handshake = WebSocket.handshake % {
                'origin': origin,
                'port': self.server.port,
                'bind': self.server.bind
            }
            handshake += response
        elif part_3:
            handshake = WebSocket.handshake_10 % {
                'origin': origin,
                'port': self.server.port,
                'bind': self.server.bind,
                'accept':  part_3
            }            
        else:
            #logging.warning("Not using challenge + response")
            handshake = WebSocket.handshake % {
                'origin': origin,
                'port': self.server.port,
                'bind': self.server.bind
            }
        #logging.debug("Sending handshake %s" % handshake)
        self.client.send(handshake)
        return True

    def onmessage(self, data):
        print "onMessage: %s" % data
        #logging.info("Got message: %s" % data)

    def close(self):
        self.client.close()

    def send(self, data):
        logging.info("Sent message: %s" % data)
        #self.client.send("\x00"+data.encode('utf8')+"\xff")
        frame=self.buildFrame(data.encode('utf8'))
        #logging.info("Sent frame: %s" % frame)
        self.client.send(frame)

    def buildFrame(self, msg):
        """
        According to http://tools.ietf.org/html/draft-ietf-hybi-thewebsocketprotocol-10
        FIN=1
        Opcode=1
        Mask=0
        
        payload length encoding:
        0  ->125   :  7bits
        126->65535 :  7bits+16bits
        >65535     :  7bits+64bits
        """
        Opcode=1
        payload_len=len(msg)
        B1 = 0x80 | (Opcode & 0x0f)
        
        if payload_len < 126:
            frame=struct.pack(">BB",B1,payload_len)
        elif payload_len<65536:
            frame=struct.pack(">BBH",B1,126,payload_len)
        else:
            frame=struct.pack(">BBQ",B1,127,payload_len)
        
        return frame+msg


class WebSocketServer(object):
    def __init__(self, bind, port, cls, backlog=5):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((bind, port))
        self.bind = bind
        self.port = port
        self.cls = cls
        self.connections = {}
        self.listeners = [self.socket]
        self.socket.listen(backlog)
        
    def listen(self, timeout=1):

        #logging.info("Listening on %s" % self.port)

        rList, _wList, xList = select(self.listeners, [], self.listeners, timeout)
        for ready in rList:
            if ready == self.socket:
                logging.debug("New client connection")
                client, _address = self.socket.accept()
                fileno = client.fileno()
                self.listeners.append(fileno)
                self.connections[fileno] = self.cls(client, self)
            else:
                logging.debug("Client ready for reading %s" % ready)
                #logging.debug("Connections %s" % `self.connections`)
                client = self.connections[ready].client
                data = client.recv(1024)
                fileno = client.fileno()
                if data:
                    self.connections[fileno].feed(data)
                else:
                    logging.debug("Closing client %s" % ready)
                    self.connections[fileno].close()
                    del self.connections[fileno]
                    self.listeners.remove(ready)
        for failed in xList:
            if failed == self.socket:
                logging.error("Socket broke")
                for fileno, conn in self.connections:
                    conn.close()
                    
    def send(self, msg):
        for socket in self.connections.values():
            socket.send(msg)
