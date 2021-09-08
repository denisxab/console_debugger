from sys import path

from helpful.template_obj import add_sys_path_if_not, rel_path

add_sys_path_if_not(rel_path(-2), path)

from console_debugger.logic.debugger import Debugger
