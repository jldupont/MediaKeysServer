'''
Created on 2011-08-09

@author: jldupont
'''   
import sys

APP_VERSION="0.1"
APP_NAME="MediaKeysServer"
ICON_NAME="mediakeysserver.png"
DESKTOP_FILEPATH="mediakeysserver.desktop"
HELP_URL="http://www.systemical.com/doc/opensource/mediakeysserver"
TIME_BASE=500

options=[
        # name,    action,      default, help
         ( '-i',  'store_true', False,  "Install in Gnome"),
         ]


###<<< DEVELOPMENT MODE SWITCHES
MSWITCH_OBSERVE_MODE=False
MSWITCH_DEBUGGING_MODE=False
MSWITCH_DEBUG_INTEREST=False
DEV_MODE=True
###>>>

import MediaKeysServer.system.setup #@UnusedImport
from   MediaKeysServer.system import base as base
from   MediaKeysServer.system import mswitch #@UnusedImport
from   MediaKeysServer.res import get_res_path

base.debug=DEV_MODE
base.debug_interest=MSWITCH_DEBUG_INTEREST

mswitch.observe_mode=MSWITCH_OBSERVE_MODE
mswitch.debugging_mode=MSWITCH_DEBUGGING_MODE

def exit(code):
    mswitch.quit("__main__")
    sys.exit(code)


def install_and_exit():
    """ Install in Gnome and exit
    """
    import shutil
    try:
        dfile=get_res_path(DESKTOP_FILEPATH)
        shutil.copy(dfile, "/usr/share/applications/%s" % DESKTOP_FILEPATH)
    except Exception,e:
        print "* Can't copy .desktop file to /usr/share/applications (%s)" % e
        exit(1)

    try:
        dfile=get_res_path(ICON_NAME)
        shutil.copy(dfile, "/usr/share/applications/%s" % ICON_NAME)
    except Exception,e:
        print "* Can't copy icon file to /usr/share/icons (%s)" % e
        exit(1)
        
    exit(0)


def main(args, debug=False):
    
    if args.i:
        install_and_exit()
    
    try:
        import MediaKeysServer.system.util as util
        from   MediaKeysServer.agents.clock import Clock
        import MediaKeysServer.agents.socket_server #@UnusedImport
        
        from   MediaKeysServer.system import app as App
                
        if util.isLinux():
            import MediaKeysServer.agents.mk_dbus #@UnusedImport
            from MediaKeysServer.agents.notifier import NotifierAgent
            _na=NotifierAgent(APP_NAME, ICON_NAME)
            _na.start()
            
        #from MediaKeysServer.agents.uitk import UiAgent
                   
        icon_path=get_res_path(ICON_NAME)
        
        _app=App.create()
        _app.app_name=APP_NAME
        _app.version=APP_VERSION
        _app.help_url=HELP_URL
        _app.icon_path=icon_path
        
        mswitch.publish("__main__", "debug", debug)
                
        App.run(_app, TIME_BASE, Clock, None)
        
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

