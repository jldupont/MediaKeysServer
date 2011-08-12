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
        try:
            self.root.destroy()
        except:
            pass
        print "uitk.doQuit"
        
    def tick(self):
        self.doPump()
        
    def onLoop(self, *p):
        try:
            self.root.update()
        except:
            pass

