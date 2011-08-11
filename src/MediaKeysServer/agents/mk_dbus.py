"""
    MediaKeys Dbus Agent
    
    Messages Generated:
    - "mk_key_press" (key, source, priority)
        priority: 1 -> low, 5 -> high
    
    Created on 2010-10-22
    @author: jldupont
"""
import dbus.service
    
from ..system.base import AgentThreadedBase
from ..system import mswitch

__all__=[]

TranslationMap={
                 "next-song":     "next"
                ,"previous-song": "previous"
                ,"play":          "play-pause"
                ,"stop-cd":       "stop"
                }


class MKSignalRx1(dbus.service.Object):
    """ works under ubuntu < 10.10
    """
    PATH=None
    
    def __init__(self, agent):
        dbus.service.Object.__init__(self, dbus.SystemBus(), self.PATH) ## not sure we need this just to receive signals...
        self.agent=agent
        
        dbus.SystemBus().add_signal_receiver(self.sCondition,
                                       signal_name="Condition",
                                       dbus_interface="org.freedesktop.Hal.Device",
                                       bus_name=None,
                                       path=None
                                       )            
    def sCondition(self, *p):
        """
        DBus signal handler
        """
        if len(p) == 2:
            if (p[0]=="ButtonPressed"):
                self._send(p[1].lower())
                #mswitch.publish(self.agent, "mk_key_press", p[1], "source1", 5)
                
    def _send(self, key):
        tkey=TranslationMap.get(key, key)
        mswitch.publish(self.agent, "mk_key_press", tkey, "source1", 5)

class MKSignalRx2(dbus.service.Object):
    """ works on ubuntu >= 10.10
    """
    PATH=None #"/org/gnome/SettingsDaemon/MediaKeys"
    
    def __init__(self, agent):
        dbus.service.Object.__init__(self, dbus.SessionBus(), self.PATH) ## not sure we need this just to receive signals...
        self.agent=agent
        
        dbus.SessionBus().add_signal_receiver(self.sCondition,
                                       signal_name="MediaPlayerKeyPressed",
                                       dbus_interface="org.gnome.SettingsDaemon.MediaKeys",
                                       bus_name=None,
                                       path="/org/gnome/SettingsDaemon/MediaKeys"
                                       )            
    def sCondition(self, *p):
        """
        DBus signal handler
        """
        if len(p) == 2:
            #mswitch.publish(self.agent, "mk_key_press", p[1].lower(), "source2", 1)
            self._send(p[1].lower())

    def _send(self, key):
        tkey=TranslationMap.get(key, key)
        mswitch.publish(self.agent, "mk_key_press", tkey, "source1", 5)


class DbusAgent(AgentThreadedBase):
    
    def __init__(self):
        AgentThreadedBase.__init__(self)

        self.srx1=MKSignalRx1(self)
        self.srx2=MKSignalRx2(self)
        
                   
_=DbusAgent()
_.start()
