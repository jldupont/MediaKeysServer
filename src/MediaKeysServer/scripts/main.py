'''
Created on 2011-08-09

@author: jldupont
'''   
import sys

APP_VERSION="0.1"
APP_NAME="MediaKeysServer"
ICON_NAME="mediakeysserver.png"
HELP_URL="http://www.systemical.com/doc/opensource/mediakeysserver"
TIME_BASE=100

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
        import MediaKeysServer.system.util as util
        from   MediaKeysServer.agents.clock import Clock
        from   MediaKeysServer.res import get_res_path
        from   MediaKeysServer.system import app as App
                
        if util.isLinux():
            import MediaKeysServer.agents.mk_dbus #@UnusedImport
            from MediaKeysServer.agents.notifier import NotifierAgent
            _na=NotifierAgent(APP_NAME, ICON_NAME)
            _na.start()
            
        from MediaKeysServer.agents.uitk import UiAgent
                   
        icon_path=get_res_path(ICON_NAME)
        
        _app=App.create()
        _app.app_name=APP_NAME
        _app.version=APP_VERSION
        _app.help_url=HELP_URL
        _app.icon_path=icon_path
        
        mswitch.publish("__main__", "debug", debug)
                
        App.run(_app, TIME_BASE, Clock, UiAgent)
        
    except KeyboardInterrupt:
        mswitch.quit()
        sys.exit(1)        
        
    except Exception,e:
        try: 
            util.notify(APP_NAME, "There was an error: %s" % e)
        finally:
            print "Exception: %s" % e
        mswitch.quit()
        sys.exit(1)

