from sys import path

from console_debugger.helpful.template_obj import add_sys_path_if_not, rel_path

add_sys_path_if_not(rel_path(-2), path)

from console_debugger.tui.urwid_terminal import ViewTui
