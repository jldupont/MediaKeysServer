'''
Created on 2011-08-09

@author: jldupont
'''   
import sys

APP_VERSION="0.1"
APP_NAME="MediaKeysServer"
ICON_NAME="mediakeysserver.png"
HELP_URL="http://www.systemical.com/doc/opensource/mediakeysserver"
TIME_BASE=5000

###<<< DEVELOPMENT MODE SWITCHES
MSWITCH_OBSERVE_MODE=True
MSWITCH_DEBUGGING_MODE=True
MSWITCH_DEBUG_INTEREST=False
DEV_MODE=True
###>>>

import MediaKeysServer.system.setup #@UnusedImport
from   MediaKeysServer.system import base as base
from   MediaKeysServer.system import mswitch #@UnusedImport

base.debug=DEV_MODE
base.debug_interest=MSWITCH_DEBUG_INTEREST

mswitch.observe_mode=MSWITCH_OBSERVE_MODE
mswitch.debugging_mode=MSWITCH_DEBUGGING_MODE

def main(debug=False):
    try:
        
        from   MediaKeysServer.res import get_res_path
        from   MediaKeysServer.agents.tray import TrayAgent
        import MediaKeysServer.agents.mk_dbus #@UnusedImport
        from   MediaKeysServer.agents.clock import Clock #@Reimport        
        from   MediaKeysServer.agents.notifier import notify, NotifierAgent #@Reimport
                
        icon_path=get_res_path()
        from MediaKeysServer.system import app as App
        
        _app=App.create()
        _app.app_name=APP_NAME
        _app.version=APP_VERSION
        _app.help_url=HELP_URL
        _app.icon_path=icon_path
        
        _na=NotifierAgent(APP_NAME, ICON_NAME)
        _na.start()

        _clk=Clock(TIME_BASE)
        _clk.init()
        
        mswitch.publish("__main__", "debug", debug)
        
        App.run(_app)
        #import gtk
        #gtk.main() #@UndefinedVariable
        
    except KeyboardInterrupt:
        mswitch.quit()
        sys.exit(1)        
        
    except Exception,e:
        try: 
            notify(APP_NAME, "There was an error: %s" % e)
        finally:
            print "Exception: %s" % e
        mswitch.quit()
        sys.exit(1)

