import io
import os
import sys
from pprint import pformat
from typing import Union, TextIO, Tuple, Optional, Dict, List

from coloring_text import *


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
    AllCountActiveInstance: List[str] = []  # Имена активных дебагеров
    AllCountSleepInstance: List[str] = []  # Имена остановленных дебагеров
    AllUseFileName: Dict[str, str] = {}  # Используемые файлы для записи
    AllInstance: Dict[str, object] = {}

    GlobalLenRows: List[Tuple[str, int]] = []
    GlobalRowBoard: str = ""

    def __init__(self,
                 title_id: str,
                 *,
                 consoleOutput: bool = True,
                 fileConfig: Optional[Dict] = None,
                 active: bool = True,
                 style_text: Optional[dstyle] = None
                 ):
        """
        public set:
            + consoleOutput = Вывод в консоль
            + style_text = Стиль отображения

        public get:
            + title_id = Уникальное имя дебагера
            + fileConfig = Конфигурация для файла
            + AllCountActiveInstance = Все активные дебагеры
            + AllCountSleepInstance = Все приостановленный дебагиры
            + AllUseFileName = Все используемые имена файлов
            + AllInstance = Все экземпляры дебагеров
        """

        # active
        self.__active: bool = active
        if self.__active:
            Debugger.AllInstance[title_id.strip()] = self
        else:
            Debugger.AllCountSleepInstance.append(title_id)
        # title_id
        self.__title_id: str = title_id
        if self.__title_id not in Debugger.AllCountActiveInstance:
            Debugger.AllCountActiveInstance.append(self.__title_id.strip())
        else:
            raise NameError("A instance of a class can only have to unique title_id")
        # fileConfig
        self.__fileConfig: Optional[Dict] = fileConfig
        if fileConfig:
            self.__addFileName_in_AllUseFileName(fileConfig["file"])

        # consoleOutput
        self.consoleOutput: Optional[TextIO] = sys.stdout if consoleOutput else None
        # style_text
        self.style_text: dstyle = dstyle(len_word=len(self.__title_id)) if not style_text else style_text

    def active(self):
        self.__active = True
        Debugger.AllCountSleepInstance.remove(self.__title_id)
        Debugger.AllInstance[self.__title_id] = self

    def deactivate(self):
        self.__active = False
        Debugger.AllInstance.pop(self.__title_id)
        Debugger.AllCountSleepInstance.append(self.__title_id)

    def __getattribute__(self, item):
        res = {
            "AllCountActiveInstance": lambda: Debugger.AllCountActiveInstance.copy(),
            "AllCountSleepInstance": lambda: Debugger.AllCountSleepInstance.copy(),
            "AllUseFileName": lambda: Debugger.AllUseFileName.copy(),
            "AllInstance": lambda: Debugger.AllInstance.copy(),
            "fileConfig": lambda: self.__dict__["_Debugger__fileConfig"],
            "title": lambda: self.__dict__["_Debugger__title_id"]
        }.get(item, None)
        return res() if res else super().__getattribute__(item)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        self.__dict__[key] = value

    def __call__(self, textOutput: Union[str, StyleText], *args, sep=' ', end='\n'):
        if self.__active:
            textOutput = textOutput.replace("\t", "")
            textOutput = style_t(textOutput, **self.style_text)

            if self.__fileConfig:
                with open(**self.__fileConfig) as f:
                    # Сохранять в файл не стилизованный текст
                    print(
                        f"|{self.__title_id}|{repr(textOutput)}|",
                        *args,
                        sep=sep, end=end, file=f)

            if self.consoleOutput:

                if Debugger.GlobalLenRows:
                    print(self.__designerTable(textOutput), end='')
                else:
                    print(f"|{self.__title_id}|{textOutput}|", *args, sep=sep, end=end)

    def __repr__(self) -> str:
        res = {"AllCountActiveInstance": Debugger.AllCountActiveInstance,
               "AllUseFileName": Debugger.AllUseFileName,
               "AllCountSleepInstance": Debugger.AllCountSleepInstance}
        res.update(self.__dict__)
        return pformat(res, indent=1, width=30, depth=2)

    def __str__(self) -> str:
        return repr(self.__title_id)

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
                if item[0] == self.__title_id:
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
            Debugger.AllUseFileName[absFileName] = self.__title_id.strip()
        else:
            raise FileExistsError("A single instance of a class can write to only one file")

    @classmethod
    def GlobalManager(cls, *, global_disable=False, typePrint: Optional[str] = "grid"):
        if global_disable:
            Debugger.__call__ = lambda *args, **kwargs: None
            cls.AllCountSleepInstance = ["GLOBAL_DISABLE"]
            cls.AllCountActiveInstance = ["GLOBAL_DISABLE"]
            return None

        if typePrint == "grid":
            rowBoard: str = ""
            rowWord: str = ""
            arr: List[str] = []
            for k, v in Debugger.AllInstance.items():
                if v.consoleOutput:
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
        else:
            cls.GlobalLenRows.clear()
            cls.GlobalRowBoard = ""


def printD(name_instance: Debugger, text: str, *args, **kwargs):
    name_instance(textOutput=text, *args, **kwargs)


dDEBUG = {"title_id": "[DEBUG]", "style_text": dstyle(**{"len_word": 25})}
dINFO = {"title_id": "[INFO]", "style_text": dstyle(**{"color": "blue", "len_word": 25})}
dWARNING = {"title_id": "[WARNING]", "style_text": dstyle(**{"color": "yellow", "attrs": ["bold"], "len_word": 31})}
dEXCEPTION = {"title_id": "[EXCEPTION]", "style_text": dstyle(**{"color": "red", "attrs": ["bold"], "len_word": 31})}

if __name__ == '__main__':
    ...
    # Debug = Debugger(title_id="[DEBUG]", style_text=dstyle(len_word=10, height=8))
    # Info = Debugger(title_id="[INFO]", style_text=dINFO)
    # Warning = Debugger(title_id="[WARNING]", style_text=dWARNING)

    # dDEBUG.active()
    # dINFO.active()
    # Debugger.GlobalManager(typePrint="grid")
    #
    # for i in range(2):
    #     printD(dDEBUG, "qwertyuiopasdfddsDXWqeqewqweqweqwewqdwQ")
    #     printD(dINFO, "12312")
    #     printD(dWARNING, "1234")
