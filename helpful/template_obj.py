__all__ = ["dopen",
           "dstyle",
           "dDEBUG",
           "dINFO",
           "dWARNING",
           "dEXCEPTION",
           ]

from io import DEFAULT_BUFFER_SIZE
from typing import Union, List


class StyleText:
	def __init__(self, present_text: str, styleText: str):        ...

	def __repr__(self) -> str: ...

	def __str__(self) -> str: ...


class Debugger:
	def __call__(self, textOutput: Union[str, StyleText], *args, sep=' ', end='\n'): ...


def dopen(file: str, mode: str = 'a', buffering=None, encoding=None, errors=None, newline=None, closefd=True):
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
          "titleName": "[DEBUG]",
          "styleText": dstyle(**{"len_word": 25})}
dINFO = {"active": True,
         "titleName": "[INFO]",
         "styleText": dstyle(**{"color": "blue", "len_word": 25})}
dWARNING = {"active": True,
            "titleName": "[WARNING]",
            "styleText": dstyle(**{"color": "yellow", "attrs": ["bold"], "len_word": 31})}
dEXCEPTION = {"active": True,
              "titleName": "[EXCEPTION]",
              "styleText": dstyle(**{"color": "red", "attrs": ["bold"], "len_word": 31})}
