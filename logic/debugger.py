__all__ = ["dopen",
           "style_t",
           "dstyle",
           "Debugger",
           "printD",
           "dDEBUG",
           "dINFO",
           "dWARNING",
           "dEXCEPTION"]

import io
import os
import sys
import threading
import time
from datetime import datetime
from pprint import pformat
from typing import Union, TextIO, Tuple, Optional, Dict, List

from .coloring_text import StyleText, style_t
from .tk_gui import view_terminal


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


class Debugger:
    AllInstance: Dict[str, object] = {}
    AllActiveInstance: List[str] = []  # Имена активных дебагеров
    AllSleepInstance: List[str] = []  # Имена остановленных дебагеров
    AllUseFileName: Dict[str, str] = {}  # Используемые файлы для записи

    # Для таблицы
    GlobalLenRows: List[Tuple[str, int]] = []
    GlobalRowBoard: str = ""

    # Для Tkinter
    GlobalTkinterConsole: bool = False

    def __init__(self,
                 active: bool,
                 title_name: str,
                 *,
                 fileConfig: Optional[Dict] = None,
                 style_text: Optional[dstyle] = None,
                 consoleOutput: bool = True,
                 ):
        """
        public set:
            + consoleOutput = Вывод в консоль
            + style_text = Стиль отображения

        public get:
            + title_name = Уникальное имя дебагера
            + fileConfig = Конфигурация для файла
            + AllCountActiveInstance = Все активные дебагеры
            + AllCountSleepInstance = Все приостановленный дебагиры
            + AllUseFileName = Все используемые имена файлов
            + AllInstance = Все экземпляры дебагеров
        """

        # title_name
        self.__title_name: str = title_name

        # active
        self.__active: bool = active
        if self.__active:
            if self.__title_name not in Debugger.AllActiveInstance:
                Debugger.AllActiveInstance.append(self.__title_name)
            else:
                raise NameError("A instance of a class can only have to unique title_name")
        else:
            Debugger.AllSleepInstance.append(self.__title_name)

        # fileConfig
        self.__fileConfig: Optional[Dict] = fileConfig
        if fileConfig:
            self.__addFileName_in_AllUseFileName(self.__fileConfig["file"])

        # consoleOutput
        self.consoleOutput: Optional[TextIO] = sys.stdout if consoleOutput else None

        # style_text
        self.style_text: dstyle = dstyle(len_word=len(self.__title_name)) if not style_text else style_text
        # id
        self.__id = len(Debugger.AllActiveInstance) - 1

        Debugger.AllInstance[title_name] = self

    def active(self):
        self.__active = True
        if self.__title_name in Debugger.AllSleepInstance:
            Debugger.AllSleepInstance.remove(self.__title_name)

        if self.__title_name not in Debugger.AllActiveInstance:
            Debugger.AllActiveInstance.append(self.__title_name)

    def deactivate(self):
        self.__active = False
        if self.__title_name in Debugger.AllActiveInstance:
            Debugger.AllActiveInstance.remove(self.__title_name)

        if self.__title_name not in Debugger.AllSleepInstance:
            Debugger.AllSleepInstance.append(self.__title_name)

    def __getattribute__(self, item):
        res = {
            "AllCountActiveInstance": lambda: Debugger.AllActiveInstance.copy(),
            "AllCountSleepInstance": lambda: Debugger.AllSleepInstance.copy(),
            "AllUseFileName": lambda: Debugger.AllUseFileName.copy(),
            "AllInstance": lambda: Debugger.AllInstance.copy(),
            "fileConfig": lambda: self.__dict__["_Debugger__fileConfig"],
            "title_name": lambda: self.__dict__["_Debugger__title_name"]
        }.get(item, None)
        return res() if res else super().__getattribute__(item)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        self.__dict__[key] = value

    def __call__(self, textOutput: Union[str, StyleText], *args, sep=' ', end='\n'):
        if self.__active:

            if self.__fileConfig:
                with open(**self.__fileConfig) as f:
                    # Сохранять в файл не стилизованный текст
                    print(
                        f"|{self.__title_name}|{textOutput}|",
                        *args,
                        sep=sep, end=end, file=f)

            if self.consoleOutput:
                # Таблица
                if Debugger.GlobalLenRows:
                    print(self.__designerTable(style_t(textOutput.replace("\t", ""),
                                                       **self.style_text)), end='')
                # Tkinter если окно закрыто, то перенаправляем вывод в стандартную консоль
                elif Debugger.GlobalTkinterConsole and view_terminal.View.Arr_textWidget:
                    view_terminal.View.Arr_textWidget[self.__id].insert("end",
                                                                        f"[{datetime.now().strftime('%H:%M:%S')}]{textOutput}\n{'_' * 10}\n")
                # Без стилей
                else:
                    print(
                        "|{}|\t{}".format(self.__title_name, style_t(textOutput.replace('\t', ''), **self.style_text)),
                        *args,
                        sep=sep, end=end)

    def __repr__(self) -> str:
        res = {"AllCountActiveInstance": Debugger.AllActiveInstance,
               "AllUseFileName": Debugger.AllUseFileName,
               "AllCountSleepInstance": Debugger.AllSleepInstance}
        res.update(self.__dict__)
        return pformat(res, indent=1, width=30, depth=2)

    def __str__(self) -> str:
        return repr(self.__title_name)

    def __designerTable(self, textOutput: StyleText) -> str:
        """
        Dependencies:

        - Debugger.GlobalLenRows:
        - self.style_text:
        - self._title:
        """
        res_print: str = ""
        for height_item in textOutput.present_text.split('\n'):
            height_item = style_t(height_item, **self.style_text).style_text
            for item in Debugger.GlobalLenRows:
                if item[0] == self.__title_name:
                    res_print += f"|{height_item}"
                else:
                    res_print += f"|{' ' * item[1]}"
            res_print += '|\n'
        res_print += f"{Debugger.GlobalRowBoard}\n"
        return res_print

    def __addFileName_in_AllUseFileName(self, file_name: str):
        """
        Проверяет имя файла со всеми используемыми именами файлов
        Это необходимо для защиты от случайного параллельного доступа к файлам
        :param file_name: Имя файла
        """
        absFileName = os.path.abspath(file_name).replace("\\", "/")
        if not Debugger.AllUseFileName.get(absFileName, False):
            Debugger.AllUseFileName[absFileName] = self.__title_name.strip()
        else:
            raise FileExistsError("A single instance of a class can write to only one file")

    @classmethod
    def GlobalManager(cls, *, global_active: bool = None, typePrint: Optional[str] = "grid"):

        if global_active != None:
            if global_active:
                for k, v in cls.AllInstance.items():
                    if k not in cls.AllActiveInstance:
                        cls.AllActiveInstance.append(k)

                    if k in cls.AllSleepInstance:
                        cls.AllSleepInstance.remove(k)
                return None

            if not global_active:
                for k, v in cls.AllInstance.items():
                    if k not in cls.AllSleepInstance:
                        cls.AllSleepInstance.append(k)

                    if k in cls.AllActiveInstance:
                        cls.AllActiveInstance.remove(k)
                return None

        # Отображать таблицу в консоли
        if typePrint == "grid":
            rowBoard: str = ""
            rowWord: str = ""
            arr: List[str] = []
            for k, v in Debugger.AllInstance.items():
                if v.__active:
                    v1 = v.style_text.copy()
                    v1['agl'] = 'center'  # чтобы центрировать только заголовки а не весь текст
                    text = style_t(k, **v1).present_text
                    rowBoard += f"+{'-' * len(text)}"
                    rowWord += f"|{text}"
                    arr.append(text)
                    cls.GlobalLenRows.append((k, len(text)))

            rowWord += "|"
            rowBoard += "+"
            row: str = f"{rowBoard}\n{rowWord}\n{rowBoard.replace('-', '=')}"
            cls.GlobalRowBoard = rowBoard
            print(row)
            return None

        # Отображать в Tkinter
        elif typePrint == "tk":
            cls.GlobalTkinterConsole = True
            threading.Thread(name='Th_debugger_tkinter',
                             target=view_terminal.View,
                             args=(cls.AllActiveInstance,)).start()

            # Ждать пока окно создаться
            while view_terminal.View.Arr_textWidget == []:
                time.sleep(0.1)

            return None

        cls.GlobalTkinterConsole = False
        cls.GlobalLenRows.clear()
        cls.GlobalRowBoard = ""


def printD(name_instance: Debugger, text: str, *args, **kwargs):
    name_instance(textOutput=text, *args, **kwargs)


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

if __name__ == '__main__':
    ...
