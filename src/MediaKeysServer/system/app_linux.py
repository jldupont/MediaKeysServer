'''
Created on 2011-08-11

@author: jldupont
'''
import gobject #@UnresolvedImport
import gtk #@UnusedImport
import gtk.gdk
import webbrowser
from ..system import mswitch as mswitch

from app import BaseApp

class AppPopupMenu:
    def __init__(self, app, version):
        if version is not None:
            self.item_version = gtk.MenuItem( "version: %s" % version, False) #@UndefinedVariable
            self.item_version.set_sensitive(False)
            
        self.item_exit = gtk.MenuItem( "exit", True) #@UndefinedVariable
        self.item_show = gtk.MenuItem( "show", True) #@UndefinedVariable
        self.item_help = gtk.MenuItem( "help", True) #@UndefinedVariable

        self.item_show.connect( 'activate', app.show)
        self.item_help.connect( 'activate', app.help)
        self.item_exit.connect( 'activate', app.exit)
        
        self.menu = gtk.Menu() #@UndefinedVariable
        self.menu.append( self.item_show)
        self.menu.append( self.item_help)
        self.menu.append( self.item_exit)
        if version is not None:
            self.menu.append( self.item_version)        
        self.menu.show_all()

    def show_menu(self, button, time):
        self.menu.popup( None, None, None, button, time)
        

class AppIcon(object):
    
    def __init__(self, icon_path):
        self.icon_path=icon_path
    
    def getIconPixBuf(self): 
        pixbuf = gtk.gdk.pixbuf_new_from_file( self.icon_path )   #@UndefinedVariable
        return pixbuf.scale_simple(24,24,gtk.gdk.INTERP_BILINEAR) #@UndefinedVariable



class TrayApp(BaseApp):
    def __init__(self):
        pass
    
    def prepare(self):
        self.popup_menu=AppPopupMenu(self, self.version)
        
        self.tray=gtk.StatusIcon() #@UndefinedVariable
        self.tray.set_visible(True)
        self.tray.set_tooltip(self.app_name)
        #self.tray.connect('activate', self.do_popup_menu_activate)
        self.tray.connect('popup-menu', self.do_popup_menu)
        
        scaled_buf = AppIcon(self.icon_path).getIconPixBuf()
        self.tray.set_from_pixbuf( scaled_buf )
        
    def do_popup_menu_activate(self, statusIcon):
        timestamp=gtk.get_current_event_time() #@UndefinedVariable
        self.popup_menu.show_menu(None, int(timestamp))
        
    def do_popup_menu(self, status, button, time):
        self.popup_menu.show_menu(button, time)

    def show(self, *_):
        mswitch.publish(self, "app_show")

    def exit(self, *p):
        mswitch.publish(self, "__quit__")
        gtk.main_quit() #@UndefinedVariable
        
    def help(self, *_):
        webbrowser.open(self.help_url)

def create():
    return TrayApp()

def run(app, time_base, clock_class, ui_class):
    
    app.prepare()
    #ui_obj=ui_class()
    clock_obj=clock_class(time_base)
    
    def doTick():
        #print "doTick!"
        clock_obj.tick()
        #ui_obj.tick()
        return True

    gobject.timeout_add(time_base, doTick)
    gtk.main() #@UndefinedVariable
    

