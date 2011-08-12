'''
Created on 2011-08-11

@author: jldupont
'''
import sys

def isLinux():
    return sys.platform.startswith("linux")

def isOSX():
    return sys.platform.startswith("darwin")

try:
    import pynotify #@UnresolvedImport
    def notify(app_name, msg, icon_name="important", urgency=pynotify.URGENCY_CRITICAL):
        try:
            pynotify.init(app_name)
            n=pynotify.Notification(app_name, msg, icon_name)
            n.set_urgency(urgency)
            n.show()
            return n
        except:
            print "%s: %s" % (app_name, msg)
    
except:
    def notify(app_name, msg, icon_name="important", urgency=None):
        print "%s: %s" % (app_name, msg)
