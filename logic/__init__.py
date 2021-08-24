from os.path import dirname
from sys import path
from .debugger import *

dirs = dirname(__file__).replace("\\", "/").split("/")[:-1]
dirs.append("helpful")
path.append("/".join(dirs))

