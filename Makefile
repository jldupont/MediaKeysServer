#
# Makefile
#
# @author Jean-Lou Dupont
#
#

all:
	@echo "make options:"
	@echo " egg : release python egg"
	@echo " osx : release for OSX"
	
osx:
	@rm -Rf build
	@install -d build/osx/MediaKeysServer.app/Contents
	@install -d build/osx/MediaKeysServer.app/Contents/MacOs
	@install -d build/osx/MediaKeysServer.app/Contents/Resources
	
	@install -d build/osx/MediaKeysServer.app/Contents/Resources/MediaKeysServer/agents
	@install -d build/osx/MediaKeysServer.app/Contents/Resources/MediaKeysServer/res
	@install -d build/osx/MediaKeysServer.app/Contents/Resources/MediaKeysServer/scripts
	@install -d build/osx/MediaKeysServer.app/Contents/Resources/MediaKeysServer/system
	
	@install Info.plist          build/osx/MediaKeysServer.app/Contents
	@install src/MediaKeysServer/res/mediakeysserver.icns   build/osx/MediaKeysServer.app/Contents/Resources
	
	@cp src/scripts/mediakeysserver      build/osx/MediaKeysServer.app/Contents/MacOs/mks
	
	@cp -R src/MediaKeysServer build/osx/MediaKeysServer.app/Contents/MacOs
	@rm -Rf build/osx/MediaKeysServer.app/*.pyc
	
	
	@echo "Finished building OSX .app"
	
egg:
	python setup.py sdist upload
