'''
Created on 2011-08-11

@author: jldupont
'''
import util

class BaseApp(object):
    
    def __init__(self):
        self.menu_items=[]

    def __setitem__(self, key, value):
        self.__dict__[key]=value
        
    def __getitem__(self, key):
        return self.__dict__.get(key, None)
        
    def run(self):
        raise RuntimeError("run: not implemented")
        

if util.isOSX():
    import app_osx as osapp #@UnusedImport
else:
    import app_linux as osapp #@Reimport
    

def create():
    return osapp.create()

def run(app, time_base, clock_class, ui_class):
    osapp.run(app, time_base, clock_class, ui_class)
