"""
    MediaKeys Dbus Agent
    
    Messages Generated:
    - "mk_key_press" (key, source, priority)
        priority: 1 -> low, 5 -> high
    
    Created on 2010-10-22
    @author: jldupont
"""
import dbus.service #@UnresolvedImport
    
from ..system.base import AgentThreadedBase
from ..system import mswitch

__all__=[]

TranslationMap={
                 "next-song":     "next"
                ,"previous-song": "previous"
                ,"play":          "play-pause"
                ,"stop-cd":       "stop"
                }


class Filter:
    """
    - if same key, different source, different seq => pass
    - if same key, different source                => block
    - if same key, same source,      different seq => pass
    -    same key, same source,      same seq      : not possible
    - if different key                             => pass
    """
    prev=(None, None, None)
    
    @classmethod
    def do(cls, key, source, seq):
        """ True => pass
        """
        key=unicode(key)

        pkey, psource, pseq=cls.prev
        if pkey is None or psource is None or pseq is None:
            cls.prev=(key, source, seq)
            return True
        
        pkey, psource, _pseq=cls.prev
        cls.prev=(None, None, None)
        #print "key(%s) pkey(%s) source(%s) psource(%s)" % (key, pkey, source, psource)
        #print "key==pkey: %s" % (key==pkey)
        #print "source==psource: %s" % (source==psource)        
        
        # same key, same source... can't be at the same time!
        if pkey==key and psource==source:
            return True
        
        # same key, different source => block and reset
        if pkey == key and psource != source:
            return False
        
        cls.prev=(key, source, seq)
        return True


class MKSignalRx1(dbus.service.Object):
    """ works under ubuntu < 10.10
    
        - play-pause
        - previous, next, stop
        - volume-up, volume-down
    """
    PATH=None
    
    def __init__(self, agent):
        dbus.service.Object.__init__(self, dbus.SystemBus(), self.PATH) ## not sure we need this just to receive signals...
        self.agent=agent
        self.seq=0
        
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
                self._send(p[1].lower(), "source1", self.seq)
                #mswitch.publish(self.agent, "mk_key_press", p[1], "source1", 5)
                
    def _send(self, key, source, seq):
        tkey=TranslationMap.get(key, key)
        
        if Filter.do(tkey, source, seq):
            mswitch.publish(self.agent, "mk_key_press", tkey, "source1", self.seq)
            self.seq=self.seq+1

class MKSignalRx2(dbus.service.Object):
    """ works on ubuntu >= 10.10
        
        - play-pause
        - previous, next, stop
        *** doesn't catch 'volume-*'...
    """
    PATH=None #"/org/gnome/SettingsDaemon/MediaKeys"
    
    
    def __init__(self, agent):
        dbus.service.Object.__init__(self, dbus.SessionBus(), self.PATH) ## not sure we need this just to receive signals...
        self.agent=agent
        self.seq=0
        
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
            self._send(p[1].lower(), "source2", self.seq)

    def _send(self, key, source, seq):
        tkey=TranslationMap.get(key, key)
        
        if Filter.do(tkey, source, seq):
            mswitch.publish(self.agent, "mk_key_press", tkey, "source2", self.seq)
            self.seq=self.seq+1


    


class DbusAgent(AgentThreadedBase):
    
    def __init__(self):
        AgentThreadedBase.__init__(self)

        self.srx1=MKSignalRx1(self)
        self.srx2=MKSignalRx2(self)
        
                   
_=DbusAgent()
_.start()
