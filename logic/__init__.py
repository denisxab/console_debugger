from os.path import dirname
from sys import path

dirs = dirname(__file__).replace("\\", "/").split("/")[:-2]
path.append("/".join(dirs))

from console_debugger.logic.debugger import Debugger
