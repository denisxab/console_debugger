from sys import argv, path

from path_helper import add_sys_path_if_not, root_path

add_sys_path_if_not(root_path(0), path)

from gui.tk_terminal import ViewGui
from tui.urwid_terminal import ViewTui

if __name__ == '__main__':
	for param in set(argv):
		if param == "tui":
			ViewTui()
			break
		elif param == "gui":
			ViewGui()
			break
	else:
		print("tui OR gui")
