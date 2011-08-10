'''
Created on Aug 10, 2011

@author: jldupont
'''
from MediaKeysServer.system.base import AgentThreadedBase
from MediaKeysServer.system.websocket import WebSocketServer, WebSocket

class SocketServerAgent(AgentThreadedBase):
    
    def __init__(self):
        AgentThreadedBase.__init__(self)

        self.server= WebSocketServer("localhost", 1337, WebSocket)
        
    def onLoop(self):
        self.server.listen(backlog=5, timeout=1)


_=SocketServerAgent()
_.start()
