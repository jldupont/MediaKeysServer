#
# Makefile
#
# @author Jean-Lou Dupont
#
#

all:
	@echo "make options:"
	@echo " egg : release python egg"
	
egg:
	python setup.py sdist upload
