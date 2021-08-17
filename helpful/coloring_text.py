__all__ = ["style_t", "cprint", "StyleText"]

from collections import deque
from os import getenv
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


def style_t(text: str,
            color: str = None,
            bg_color: str = None,
            attrs: List[str] = None,
            len_word: int = None,
            agl=None,
            height=2
            ):
    if len_word:
        # Выравнивание текста по центру
        if agl == 'center':

            if len(text) > len_word:
                # Если длинна слова больше разрешённой, то и центрировать не нужно, просто обрезаем строку
                text = f"{text[:len_word - 2]}.."

            else:
                # Если нужно центрировать строку меньше разрешённой длины
                text = text.center(len_word, ' ')

        else:

            # Заполняем динамический массив символами, если достигаем максимума длины то добавляем перенос строки
            arr_text: deque = deque()

            for index, sbl in enumerate(text):

                # Если слово достигла максимума по ширине и высоте, то обрезаем его
                if index + 2 > len_word * height:
                    for _ in range(-index % len_word):
                        arr_text.append(".")
                    break
                # Если слово достигло максимума по ширине, но не по высоте, то добавляем перенос строки
                if index % len_word == 0:
                    arr_text.append('\n')

                # Пользовательские переносы строк нарушают структуру, поэтому лучше их игнорировать, и
                # ставить переносы строки по правилам этого алгоритма
                if text[index] != '\n':
                    # Добавляем символы в динамический массив
                    arr_text.append(sbl)
            else:
                # Заполняем пустоту у последней строчки чтобы была одинаковая длинна столбцов
                for _ in range(-len(text) % len_word):
                    arr_text.append(" ")

            # Если будет не пустой массив
            if arr_text:
                # Убираем первый ненужный перенос строки
                arr_text.popleft()

            # Конвертируем массив в строку
            text = ''.join(arr_text)

    Style_text = text

    if getenv('ANSI_COLORS_DISABLED') is None:

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
           len_word: int = None,
           ):
    print(style_t(text, color, bg_color, attrs, len_word).style_text, sep=sep, end=end, file=file, flush=flush)


if __name__ == '__main__':
    ...
    # cprint('Hello, World!',
    #        color='red',
    #        bg_color="bg_blue",
    #        attrs=["concealed"],
    #        file=sys.stdout)
