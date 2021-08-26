from os.path import dirname
from sys import path

dirs = dirname(__file__).replace("\\", "/").split("/")[:-2]
p = "/".join(dirs)
if p not in path:
	path.append(p)

from console_debugger.tui.urwid_terminal import ViewTui
