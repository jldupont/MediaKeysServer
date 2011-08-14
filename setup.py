#!/usr/bin/env python
'''
Created on 2011-05-05

@author: jldupont
'''

__author__  ="Jean-Lou Dupont"
__version__ ="0.5"

from distutils.core import setup
from setuptools import find_packages

setup(name=         'mediakeysserver',
      version=      __version__,
      description=  'Media Keys websocket server',
      author=       __author__,
      author_email= 'jl@jldupont.com',
      url=          'http://www.systemical.com/doc/opensource',
      packages=     ["MediaKeysServer", 
                     "MediaKeysServer.agents", 
                     "MediaKeysServer.res",
                     "MediaKeysServer.scripts",
                     "MediaKeysServer.system"
                     ],
      package_dir=  {'MediaKeysServer': "src/MediaKeysServer",},
      scripts=      ['src/scripts/mediakeysserver',
                     ],
      package_data = {
                      '':[ "*.gif", 
                            "**.png", 
                            "*.jpg", 
                            "*.desktop" ],
                      },
      include_package_data=True,                      
      zip_safe=False
      )
