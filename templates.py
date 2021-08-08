import io
from typing import List


def dopen(file, mode='a', buffering=None, encoding=None, errors=None, newline=None, closefd=True):
    return {"file": file,
            "mode": mode,
            "buffering": buffering if buffering else io.DEFAULT_BUFFER_SIZE,
            "encoding": encoding,
            "errors": errors,
            "newline": newline,
            "closefd": closefd,
            }


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
            "height": height
            }


dDEBUG = {
    "bg_color": "bg_blue",
    "len_word": 25
}

dINFO = {
    "color": "blue",
    "len_word": 25
}

dWARNING = {
    # "bg_color": "bg_yellow",
    "color": "yellow",
    "attrs": ["bold"],
    "len_word": 31
}

dEXCEPTION = {

    "color": "red",
    "attrs": ["bold"],
    "len_word": 31
}
