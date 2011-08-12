'''
Created on 2011-08-12

@author: jldupont
'''
import Tkinter

from ..system.base import AgentPumped


class UiAgent(AgentPumped):
    
    def __init__(self, debug=False):
        AgentPumped.__init__(self, debug)
        
        self.root=Tkinter.Tk()
        self.frame=Tkinter.Frame(self.root)
        self.frame.pack()
        self.button_quit=Tkinter.Button(self.frame, text="Quit", command=self.announceQuit)
        self.button_quit.pack(side=Tkinter.LEFT)
        
        
    def announceQuit(self):
        self.pub("__quit__")
        
    def beforeQuit(self):
        self.root.destroy()
        print "uitk.doQuit"
        
    def h__tick__(self, *p):
        print "uitk.__tick__"
        self.root.update()

    def onLoop(self):
        print "onLoop"
        pass

    def start(self):
        pass
        
    
    
_=UiAgent()
_.start()

