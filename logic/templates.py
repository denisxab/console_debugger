__all__ = ["dopen",
           "dstyle",
           "dDEBUG",
           "dINFO",
           "printD",
           "dWARNING",
           "dEXCEPTION",
           ]

import io
from typing import List

from .stup_debugger import *


def dopen(file, mode='a', buffering=None, encoding=None, errors=None, newline=None, closefd=True):
    return {"file": file,
            "mode": mode,
            "buffering": buffering if buffering else io.DEFAULT_BUFFER_SIZE,
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
          "style_text": dstyle(**{"len_word": 25, "height": 5})}
dINFO = {"active": True,
         "title_name": "[INFO]",
         "style_text": dstyle(**{"color": "blue", "len_word": 25, "height": 2})}
dWARNING = {"active": True,
            "title_name": "[WARNING]",
            "style_text": dstyle(**{"color": "yellow", "attrs": ["bold"], "len_word": 31, "height": 10})}
dEXCEPTION = {"active": True,
              "title_name": "[EXCEPTION]",
              "style_text": dstyle(**{"color": "red", "attrs": ["bold"], "len_word": 31, "height": 20})}


def printD(name_instance: Debugger, text: str, *args, **kwargs):
    name_instance(textOutput=text, *args, **kwargs)
