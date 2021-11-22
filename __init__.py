import os
from sys import path

path.insert(0, os.path.dirname(__file__))

from .logic.debugger import printD, Debugger
from helpful.template_obj import dINFO, dWARNING, dDEBUG, dEXCEPTION, dopen

if __name__ == '__main__':
	# Защита чтобы ide не убирал импорт
	print(dINFO, dWARNING, dDEBUG, dEXCEPTION, dopen, printD, Debugger.AllActiveInstance)
