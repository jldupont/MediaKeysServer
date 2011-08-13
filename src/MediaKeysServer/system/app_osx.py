'''
Created on 2011-08-11

@author: jldupont

http://pyobjc.sourceforge.net/

KeyCode   What
20        previous
19        next
16        play-pause
7         volume-mute
1         volume-down
0         volume-up

keyState  What
11        key-depressed
10        key-pressed
'''
import webbrowser

#import pyobjc #@UnresolvedImport
from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper  #@UnresolvedImport

from app import BaseApp
from ..system import mswitch as mswitch

TranslationMap={
                 0: "volume-up"
                ,1: "volume-down"
                ,7: "mute"
                ,16:"play-pause"
                ,19:"next"
                ,20:"previous"
                }

class App(NSApplication, BaseApp): #@UndefinedVariable

    def finishLaunching(self):
        print self.icon_path
        
        statusbar = NSStatusBar.systemStatusBar() #@UndefinedVariable
        self.statusitem = statusbar.statusItemWithLength_(NSSquareStatusItemLength) #@UndefinedVariable

        self.icon = NSImage.alloc().initByReferencingFile_(self.icon_path) #@UndefinedVariable
        self.icon.setSize_((20, 20))
        self.statusitem.setImage_(self.icon)

        menu = NSMenu.alloc().init() #@UndefinedVariable
        
        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('exit', 'terminate:', '')  #@UndefinedVariable
        menu.addItem_(menuitem)

        #menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('show', 'show', '') #@UndefinedVariable
        #menu.addItem_(menuitem)

        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('help', 'help', '') #@UndefinedVariable
        menu.addItem_(menuitem)
        
        self.statusitem.setMenu_(menu)

    def sendEvent_(self, event):
        if event.type() is NSSystemDefined and event.subtype() is 8:  #@UndefinedVariable
                    data = event.data1()
                    keyCode = (data & 0xFFFF0000) >> 16
                    keyFlags = (data & 0x0000FFFF)
                    keyState = (keyFlags & 0xFF00) >> 8
                    _keyRepeat = keyFlags & 0x1
        
                    if keyState==11: #depressed
                        tkey=TranslationMap.get(keyCode, None)
                        if tkey is not None:
                            mswitch.publish("mk_key_press", tkey, "osx", 0)
                            #print "keycode(%s) keystate(%s): %s" % (keyCode, keyState, tkey)
        
        NSApplication.sendEvent_(self, event)        #@UndefinedVariable

    def show(self):
        mswitch.publish(self, "app_show")

    def help(self):
        webbrowser.open(self.help_url)

class Ticker(NSObject): #@UndefinedVariable
    
    def __init__(self):
        NSObject.__init__(self) #@UndefinedVariable
    
    def dosetup(self, time_base, clock_obj, ui_obj):
        self.clock_obj=clock_obj
        self.ui_obj=ui_obj
        self.time_base=time_base
    
    @objc.signature("v@:@")  #@UndefinedVariable
    def tick_(self, timer):
        self.clock_obj.tick()
        if self.ui_obj is not None:
            self.ui_obj.tick()
        

def create():
    app = App.sharedApplication()
    return app
    
def run(app, time_base, clock_class, ui_class):
    clock_obj=clock_class(time_base)
    
    ticker=Ticker.alloc().init()
    ticker.dosetup(time_base, clock_obj, None)
    
    NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(time_base/1000, ticker, 'tick:', None, True) #@UndefinedVariable
    AppHelper.runEventLoop(installInterrupt=True)
