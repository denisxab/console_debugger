from sys import path

from helpful.path_helper import add_sys_path_if_not, rel_path

add_sys_path_if_not(rel_path(-2), path)

from tui.urwid_terminal import ViewTui
