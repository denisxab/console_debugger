__all__ = ["dopen",
           "dstyle",
           "dDEBUG",
           "dINFO",
           "printD",
           "dWARNING",
           "dEXCEPTION",
           "ServerError",
           ]

from io import DEFAULT_BUFFER_SIZE

from typing import Union, List, Optional, Any


class ServerError(BaseException):    ...


class StyleText:
	def __init__(self, present_text: str, style_text: str):        ...

	def __repr__(self) -> str: ...

	def __str__(self) -> str: ...


class Debugger:
	def __call__(self, textOutput: Union[str, StyleText], *args, sep=' ', end='\n'): ...


class ViewRoot:

	def __init__(self):
		from console_debugger.logic.mg_get_socket import MgGetSocket
		self.SeverGet: Optional[MgGetSocket] = None

	def PrintInfo(self, text: str):        ...

	def UpdateTitle(self, l_text: List[str]):        ...

	def SendTextInIndex(self, index: int, data: str):        ...


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


def printD(name_instance: Debugger, text: Any, *args, **kwargs):
	name_instance(text, *args, **kwargs)
