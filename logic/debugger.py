__all__ = ["dopen",
           "style_t",
           "dstyle",
           "Debugger",
           "printD",
           "dDEBUG",
           "dINFO",
           "dWARNING",
           "dEXCEPTION"]

import inspect
from datetime import datetime
from os.path import abspath
from pprint import pformat
from sys import stdout
from threading import Thread
from time import sleep
from typing import TextIO, Tuple, Optional, Dict, List, Union

from console_debugger.tk_gui import view_terminal
from .coloring_text import style_t, StyleText
from .templates import *


class Debugger:
    AllInstance: Dict[str, object] = {}

    # Имена активных дебагеров
    AllActiveInstance: List[str] = lambda: [v.title_name for v in Debugger.AllInstance.values()
                                            if v.is_active]

    # Имена остановленных дебагеров
    AllSleepInstance: List[str] = lambda: [v.title_name for v in Debugger.AllInstance.values()
                                           if not v.is_active]

    # Используемые файлы для записи
    AllUseFileName: Dict[str, str] = lambda: {v.fileConfig["file"]: v.title_name for v in Debugger.AllInstance.values()
                                              if v.fileConfig}

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
        if self.__active and self.__title_name in self.AllActiveInstance:
            raise NameError("A instance of a class can only have to unique title_name")

        # fileConfig
        self.__fileConfig: Optional[Dict] = fileConfig
        if fileConfig:
            self.__addFileName_in_AllUseFileName(self.__fileConfig["file"])

        # consoleOutput
        self.consoleOutput: Optional[TextIO] = stdout if consoleOutput else None

        # style_text
        self.style_text: dstyle = dstyle(len_word=len(self.__title_name)) if not style_text else style_text

        # id
        Debugger.AllInstance[title_name] = self  # Это строчка должны быть выше назначения self.__id !
        self.__id = len(self.AllActiveInstance) - 1

    def active(self):
        self.__active = True

    def deactivate(self):
        self.__active = False

    def __getattribute__(self, item):
        res = {
            "AllActiveInstance": lambda: Debugger.AllActiveInstance(),
            "AllSleepInstance": lambda: Debugger.AllSleepInstance(),
            "AllUseFileName": lambda: Debugger.AllUseFileName(),
            "AllInstance": lambda: Debugger.AllInstance.copy(),
            "fileConfig": lambda: self.__dict__["_Debugger__fileConfig"],
            "title_name": lambda: self.__dict__["_Debugger__title_name"],
            "is_active": lambda: self.__active,
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
                    """
                    1. Отображать имя переменной, если у нее есть внешняя ссылка.
                    2. Если одному и тому же значению присвоено несколько переменных, 
                    вы будете получить оба этих имени переменных
                    """
                    callers_local_vars = inspect.currentframe().f_back.f_back.f_locals.items()
                    names_var: list = [var_name for var_name, var_val in callers_local_vars if var_val is textOutput]
                    names_var_str: str = "¦"
                    if names_var:
                        names_var_str = f"({', '.join(names_var)})¦"

                    res = "{next_steep}\n{data}{name_var}\n{textOutput}\n".format(
                        next_steep=f"{'-' * (len(names_var_str) + 7)}¬",
                        data=datetime.now().strftime('%H:%M:%S'),
                        name_var=names_var_str,
                        textOutput=f"{textOutput} {' '.join(str(item) for item in args)}",

                    )

                    view_terminal.View.Arr_textWidget[self.__id].insert("end", res)
                # Без стилей
                else:
                    print(
                        "|{}|\t{}".format(self.__title_name, style_t(textOutput.replace('\t', ''), **self.style_text)),
                        *args,
                        sep=sep, end=end)

    def __repr__(self) -> str:
        res = {"AllCountActiveInstance": self.AllActiveInstance,
               "AllUseFileName": self.AllUseFileName,
               "AllCountSleepInstance": self.AllSleepInstance}
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
        absFileName = abspath(file_name).replace("\\", "/")
        if not self.AllUseFileName.get(absFileName, False):
            self.__fileConfig["file"] = absFileName
        else:
            raise FileExistsError("A single instance of a class can write to only one file")

    @classmethod
    def GlobalManager(cls, *, global_active: Optional[bool] = None, typePrint: Optional[str] = "grid"):
        if global_active != None:
            if global_active:
                for k, v in cls.AllInstance.items():
                    v.__active = True
                return None

            if not global_active:
                for k, v in cls.AllInstance.items():
                    v.__active = False
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
            Thread(name='Th_debugger_tkinter',
                   target=view_terminal.View,
                   args=(cls.AllActiveInstance(),)).start()

            # Ждать пока окно создаться
            while view_terminal.View.Arr_textWidget == []:
                sleep(0.1)

            return None

        cls.GlobalTkinterConsole = False
        cls.GlobalLenRows.clear()
        cls.GlobalRowBoard = ""


if __name__ == '__main__':
    ...
