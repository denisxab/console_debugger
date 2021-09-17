from sys import path

from .helpful.path_helper import add_sys_path_if_not, rel_path

add_sys_path_if_not(rel_path(0), path)

from .logic.debugger import *
from helpful.template_obj import *

if __name__ == '__main__':
	# Защита чтобы ide не убирал импорт
	print(Debugger.AllActiveInstance)
	print(dINFO)
