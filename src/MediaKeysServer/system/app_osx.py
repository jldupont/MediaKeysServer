'''
Created on 2011-08-11

@author: jldupont

http://pyobjc.sourceforge.net/
'''
import webbrowser
from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper  #@UnresolvedImport

from app import BaseApp
from ..system import mswitch as mswitch

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

        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('show', 'show', '') #@UndefinedVariable
        menu.addItem_(menuitem)

        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('help', 'help', '') #@UndefinedVariable
        menu.addItem_(menuitem)
        
        self.statusitem.setMenu_(menu)

    def show(self):
        mswitch.publish(self, "app_show")

    def help(self):
        webbrowser.open(self.help_url)


def create():
    app = App.sharedApplication()
    return app
    
def run(app):
    AppHelper.runEventLoop()
