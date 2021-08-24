from os.path import dirname
from sys import path

dirs = dirname(__file__).replace("\\", "/").split("/")[:-1]
path.append("/".join(dirs))

