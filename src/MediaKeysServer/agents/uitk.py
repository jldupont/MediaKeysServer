'''
    Issue on osx...

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
        #self.button_quit=Tkinter.Button(self.frame, text="Quit", command=self.announceQuit)
        #self.button_quit.pack(side=Tkinter.LEFT)
        
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)
        print "uiagent.__init__: end"
        
    def hide_window(self):
        self.root.withdraw()

    def h_app_show(self):
        self.root.deiconify() 
        self.root.lift()
    
    ## AGENT api ====================================================    
        
    def beforeQuit(self):
        try:
            self.root.destroy()
        except:
            pass
        print "uitk.doQuit"
        
    def tick(self):
        if self.doPump():
            try: self.root.destroy()
            except: pass
        
    def onLoop(self, *p):
        try:
            self.root.update()
        except Exception, e:
            print "onLoop update error: %s" % e

