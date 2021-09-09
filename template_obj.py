__all__ = ["dopen",
           "dstyle",
           "dDEBUG",
           "dINFO",
           "printD",
           "dWARNING",
           "dEXCEPTION",
           ]

from io import DEFAULT_BUFFER_SIZE
from os.path import dirname
from typing import Union, List, Any


def add_sys_path_if_not(add_path: str, sys_path: List[str]):
	"""
	Добавить путь если его нет
	:param add_path: 
	:param sys_path: 
	:return: 
	"""
	if add_path not in sys_path:
		sys_path.append(add_path)


def rel_path(slice_end: int = 0, add_path: str = ""):
	"""
	Обрезает относительный путь, и может добавлять к нему другой путь:
	:param slice_end: Срез с конца
	:param add_path: Добавить путь
	:return:
	"""
	p = dirname(__file__).replace("\\", "/").split("/")
	if slice_end:
		p = p[:slice_end]
	if add_path:
		p.append(add_path.replace("\\", "/"))
	return "/".join(p)


class StyleText:
	def __init__(self, present_text: str, style_text: str):        ...

	def __repr__(self) -> str: ...

	def __str__(self) -> str: ...


class Debugger:
	def __call__(self, textOutput: Union[str, StyleText], *args, sep=' ', end='\n'): ...


def printD(name_instance: Debugger, text: Any, *args, **kwargs):
	name_instance(text, *args, **kwargs)


def dopen(file, mode='a', buffering=None, encoding=None, errors=None, newline=None, closefd=True):
	return {"file": file,
	        "mode": mode,
	        "buffering": buffering if buffering else DEFAULT_BUFFER_SIZE,
	        "encoding": encoding,
	        "errors": errors,
	        "newline": newline,
	        "closefd": closefd}


def dstyle(color: str = None,
           bg_color: str = None,
           attrs: List[str] = None,
           len_word: int = None,
           agl=None,
           height=2):
	return {"color": color,
	        "bg_color": bg_color,
	        "attrs": attrs,
	        "len_word": len_word,
	        "agl": agl,
	        "height": height}


dDEBUG = {"active": True,
          "title_name": "[DEBUG]",
          "style_text": dstyle(**{"len_word": 25})}
dINFO = {"active": True,
         "title_name": "[INFO]",
         "style_text": dstyle(**{"color": "blue", "len_word": 25})}
dWARNING = {"active": True,
            "title_name": "[WARNING]",
            "style_text": dstyle(**{"color": "yellow", "attrs": ["bold"], "len_word": 31})}
dEXCEPTION = {"active": True,
              "title_name": "[EXCEPTION]",
              "style_text": dstyle(**{"color": "red", "attrs": ["bold"], "len_word": 31})}
