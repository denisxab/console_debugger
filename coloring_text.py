import os
import sys

__all__ = ["style_t", "cprint", "StyleText"]

from typing import List

ATTRIBUTES = {'bold': 1,
              'dark': 2,
              'underline': 3,
              'blink': 4,
              'reverse': 5,
              'concealed': 6}

BG_COLOR = {'bg_grey': 40,
            'bg_red': 41,
            'bg_green': 42,
            'bg_yellow': 43,
            'bg_blue': 44,
            'bg_magenta': 45,
            'bg_cyan': 46,
            'bg_white': 47}

COLORS = {'grey': 30,
          'red': 31,
          'green': 32,
          'yellow': 33,
          'blue': 34,
          'magenta': 35,
          'cyan': 36,
          'white': 37}


class StyleText:
    __slots__ = ("present_text", "style_text")

    def __init__(self, present_text: str, style_text: str):
        self.present_text: str = present_text
        self.style_text: str = style_text

    def __repr__(self) -> str:
        return self.present_text

    def __str__(self) -> str:
        return self.style_text

    def strip(self, *args, **kwargs):
        return self.present_text.strip(*args, **kwargs)


def style_t(text: str,
            color: str = None,
            bg_color: str = None,
            attrs: List[str] = None,
            len_word: int = None,
            agl=None,
            height=1
            ):
    if len_word:

        if len(text) > len_word:

            # for index in range(height - 1):
            #
            #     text[:len_word] + '\n' + text[len_word:]
            #
            #     if len(text) < len_word:



            text = f"{text[: len_word - 2]}.."



        elif len(text) < len_word:
            if agl == 'center' and (len_word - len(text)) % 2 == 0:
                text = f"{' ' * ((len_word - len(text)) // 2)}{text}{' ' * ((len_word - len(text)) // 2)}"
            else:
                text = f"{text}{' ' * (len_word - len(text))}"

    Style_text = text

    if os.getenv('ANSI_COLORS_DISABLED') is None:

        fmt_str = '\033[%dm%s'

        if color is not None:
            Style_text = fmt_str % (COLORS[color], Style_text)

        if bg_color is not None:
            Style_text = fmt_str % (BG_COLOR[bg_color], Style_text)

        if attrs is not None:
            for attr in attrs:
                Style_text = fmt_str % (ATTRIBUTES[attr], Style_text)

        if Style_text != text:
            Style_text += '\033[0m'

    return StyleText(text, Style_text)


def cprint(text, color: str = None,
           bg_color: str = None,
           attrs: List[str] = None,
           sep=' ',
           end='\n',
           file=None,
           flush=False,
           len_word: int = None):
    print((style_t(text, color, bg_color, attrs, len_word)), sep=sep, end=end, file=file, flush=flush)


if __name__ == '__main__':
    cprint('Hello, World!',
           color='red',
           bg_color="bg_blue",
           attrs=["concealed"],
           file=sys.stdout)
