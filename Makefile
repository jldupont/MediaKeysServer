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
	@rm -rf build
	@install -d build/osx/MediaKeysServer.app/Contents
	@install -d build/osx/MediaKeysServer.app/Contents/MacOs
	@install -d build/osx/MediaKeysServer.app/Contents/Resources
	
	@install Info.plist          build/osx/MediaKeysServer.app/Contents
	
	@install server/keysocket.py build/osx/MediaKeysServer.app/Contents/MacOs
	@install server/websocket.py build/osx/MediaKeysServer.app/Contents/MacOs
	@install server/app.py       build/osx/MediaKeysServer.app/Contents/MacOs

	@install server/icon.icns   build/osx/MediaKeysServer.app/Contents/Resources
	@install server/icon.png    build/osx/MediaKeysServer.app/Contents/Resources
	@install server/icon-hi.png build/osx/MediaKeysServer.app/Contents/Resources
	
	@echo "Finished building OSX .app"
	
egg:
	python setup.py sdist upload
