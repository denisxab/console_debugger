from sys import path

from .path_helper import add_sys_path_if_not, rel_path

add_sys_path_if_not(rel_path(-1), path)
