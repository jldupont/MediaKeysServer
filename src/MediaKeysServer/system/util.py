'''
Created on 2011-08-11

@author: jldupont
'''
import sys

def isLinux():
    return sys.platform.startswith("linux")

def isOSX():
    return sys.platform.startswith("darwin")
