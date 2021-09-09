from sys import path

from .template_obj import add_sys_path_if_not, rel_path

add_sys_path_if_not(rel_path(0), path)

from .logic.debugger import *

if __name__ == '__main__':
	# Защита чтобы ide не убирал импорт
	print(Debugger.AllActiveInstance)
