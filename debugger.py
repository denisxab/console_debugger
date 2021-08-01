import os
import sys
from pprint import pformat
from typing import Union, TextIO, Tuple, Optional, Dict

from coloring_text import *
from templates import *


class Debugger:
    AllCountActiveInstance: List[str] = []  # Имена активных дебагеров
    AllCountSleepInstance: List[str] = []  # Имена остановленных дебагеров
    AllUseFileName: Dict[str, str] = {}  # Используемые файлы для записи
    AllInstance: Dict[str, object] = {}

    GlobalLenRows: List[Tuple[str, int]] = []
    GlobalRowBoard: str = ""

    def __init__(self,
                 title: str,
                 *,
                 consoleOutput: bool = True,
                 fileConfig: Optional[Dict] = None,
                 active: bool = True,
                 style_text: Optional[dstyle] = None
                 ):

        if active:
            #
            self.title: str = title
            Debugger.AllCountActiveInstance.append(self.title.strip())
            #
            self.__fileConfig: Optional[Dict] = None
            if fileConfig:
                self.__addFileName_in_AllUseFileName(fileConfig["file"])
                self.__fileConfig = fileConfig
            #
            self.consoleOutput: Optional[TextIO] = sys.stdout if consoleOutput else None
            self.style_text: dstyle = dstyle(len_word=len(self.title)) if not style_text else style_text

            Debugger.AllInstance[title.strip()] = self
        else:
            Debugger.AllCountSleepInstance.append(title)

    def __getattribute__(self, item):
        res = {
            "AllCountActiveInstance": lambda: Debugger.AllCountActiveInstance,
            "AllCountSleepInstance": lambda: Debugger.AllCountSleepInstance,
            "AllUseFileName": lambda: Debugger.AllUseFileName,
            "AllInstance": lambda: Debugger.AllInstance,
            "GlobalLenRows": lambda: Debugger.GlobalLenRows,
            "fileConfig": lambda: self.__dict__["_Debugger__fileConfig"],
        }.get(item, None)
        return res() if res else super().__getattribute__(item)

    def __setattr__(self, key, value):
        res = {
            "AllCountActiveInstance": lambda: AttributeError("You cannot manually change the values"),
            "AllCountSleepInstance": lambda: AttributeError("You cannot manually change the values"),
            "AllUseFileName": lambda: AttributeError("You cannot manually change the values"),
            "AllInstance": lambda: AttributeError("You cannot manually change the values"),
            "GlobalLenRows": lambda: AttributeError("You cannot manually change the values"),
            "fileConfig": lambda: AttributeError("You cannot manually change the values"),
        }.get(key, None)
        if res:
            if isinstance(res(), Exception):
                raise res()
        else:
            super().__setattr__(key, value)
            self.__dict__[key] = value

    def __call__(self, textOutput: Union[str, StyleText], *args, sep=' ', end='\n'):
        textOutput = textOutput.replace("\t", "")
        textOutput = style_t(textOutput, **self.style_text)

        if self.__fileConfig:
            with open(**self.__fileConfig) as f:
                # Сохранять в файл не стилизованный текст
                print(
                    f"|{self.title}|{repr(textOutput)}|",
                    *args,
                    sep=sep, end=end, file=f)

        if self.consoleOutput:

            if Debugger.GlobalLenRows:
                print(self.__designerTable(textOutput), end='')
            else:
                print(f"|{self.title}|{textOutput}|", *args, sep=sep, end=end)

    def __repr__(self) -> str:
        res = {"AllCountActiveInstance": Debugger.AllCountActiveInstance,
               "AllUseFileName": Debugger.AllUseFileName,
               "AllCountSleepInstance": Debugger.AllCountSleepInstance}
        res.update(self.__dict__)
        return pformat(res, indent=1, width=30, depth=2)

    def __str__(self) -> str:
        return repr(self.title)

    def __designerTable(self, textOutput: StyleText) -> str:
        """
        Dependencies:

        - Debugger.GlobalLenRows:
        - self.style_text:
        - self.title:
        """
        res_print: str = ""
        for height_item in textOutput.present_text.split('\n'):
            height_item = style_t(height_item, **self.style_text).style_text
            for item in Debugger.GlobalLenRows:
                if item[0] == self.title:
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
            Debugger.AllUseFileName[absFileName] = self.title.strip()
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
                    text = style_t(k, agl="center", **v.style_text).present_text
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


if __name__ == '__main__':
    Debug = Debugger(title="[DEBUG]",

                     fileConfig=dopen(file="debug.log",
                                      mode="a",
                                      encoding="utf-8"),

                     style_text=dstyle(bg_color="bg_blue",
                                       len_word=21)
                     )

    Info = Debugger(title="[INFO]",

                    fileConfig={"file": "info.log",
                                "mode": "a",
                                "encoding": "utf-8"},

                    style_text=dstyle(len_word=25),

                    consoleOutput=False
                    )

    Warning = Debugger("[WARNING]", style_text=dstyle(len_word=25))

    Debugger.GlobalManager(typePrint="grid")

    for i in range(10):
        # print(f"Warning \t{str(i)}")
        Warning(f"Warning \t{str(i)}")
