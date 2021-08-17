"""
Графическая оболочка
"""
__all__ = ["ViewTk"]

import json
from collections import deque
from os.path import dirname
from threading import Thread
from tkinter import Tk, Frame, Button, OUTSIDE, Text
from typing import List, Optional, Deque

from .mg_get_socket import SeverMg


class ViewTk:
    QueueSendWidget: Deque[Text] = deque()

    def __init__(self, names_console: List[str]):

        self.InitTitleName, HOST, PORT = ViewTk.get_setting_socket()

        Thread(
            target=SeverMg,
            args=(ViewTk.QueueSendWidget, HOST, PORT,),
            daemon=True,
        ).start()

        self.title_name: List[str] = []

        self.windowTk = Tk()
        self.windowTk.title("debugger_tk")
        self.windowTk.iconbitmap("{path_}/static/icons.ico".format(
            path_="/".join(dirname(__file__).replace("\\", "/").split("/")[:-1])
        ))
        self.windowTk.attributes("-topmost", True)
        self.windowTk.geometry(self.__get_geometer())

        self.frameConsole: Optional[Frame] = None
        self.bt1: Optional[Button] = None
        self.Arr_textWidget: List[Text] = []
        self.ConstructWidget(names_console)

        self.windowTk.protocol("WM_DELETE_WINDOW", self.__del)

        self.CheckUpdateQueue()

        self.windowTk.mainloop()

    def CheckUpdateQueue(self):
        if ViewTk.QueueSendWidget:
            id_, data = ViewTk.QueueSendWidget.popleft()
            if id_ == self.InitTitleName:
                if self.title_name != data:
                    self.title_name = data
                    self.DeconstructWidget()
                    self.ConstructWidget(data)

            else:
                self.Arr_textWidget[id_].insert("0.1", data)

        self.windowTk.after(30, self.CheckUpdateQueue)

    def ConstructWidget(self, names_console: Optional[List[str]]):

        self.frameConsole = Frame(self.windowTk,
                                  width=100,
                                  height=200)

        self.bt1 = Button(self.windowTk,
                          text="save geometry",
                          bg="#487861",
                          command=lambda: self.__set_geometer()
                          )
        self.bt1.pack(fill="x")

        self.Arr_textWidget = self._FormHorizonConsole(names_console, self.frameConsole)

    def DeconstructWidget(self):
        self.bt1.destroy()
        self.frameConsole.destroy()

    def __get_geometer(self) -> str:
        try:
            with open("{path_}/static/config.txt".format(
                    path_="/".join(dirname(__file__).replace("\\", "/").split("/")[:-1])), "r")as f:
                return f.read()

        except FileNotFoundError:
            return "{X}x{Y}+{W}+{H}".format(
                X=600,
                Y=600,
                W=self.windowTk.winfo_screenwidth() // 2 - 160,
                H=self.windowTk.winfo_screenheight() // 2 - 160,
            )

    def __set_geometer(self):
        with open("{path_}/static/config.txt".format(
                path_="/".join(dirname(__file__).replace("\\", "/").split("/")[:-1])), "w")as f:
            x = self.windowTk.winfo_x()
            y = self.windowTk.winfo_y()
            w = self.windowTk.winfo_width()
            h = self.windowTk.winfo_height()
            f.write(f"{w}x{h}+{x}+{y}")

    def clear_console(self, index_console: int):
        self.Arr_textWidget[index_console].delete(1.0, "end")

    def _FormHorizonConsole(self, names_console: List[str],
                            frameConsole: Frame,
                            ) -> List[Text]:
        """
        Формирует горизонтально консоли и отображает её

        :type frameConsole: self.frameConsole = Frame(self.windowTk, width=100, height=200)
        :param count_console: Количество созданных консолей
        :return: список с экземплярами консолей
        """
        ptr_arr_textWidget: List[Text] = []
        index: int = 0
        count_console: int = len(names_console)
        # нумерация строк здесь начинается с единицы, а нумерация столбцов – с нуля.
        for index_console, item in enumerate(names_console):
            ButtonLabel: Button = Button(frameConsole, text=item, bg="#0e1117", fg="#cad0d9",
                                         height=1,
                                         command=lambda i=index_console: self.clear_console(i))

            ButtonLabel.place(
                relx=index,
                relwidth=(1 / count_console),
                bordermode=OUTSIDE,
            )

            txt: Text = Text(frameConsole,
                             width=80,  # Количество символов по вертикали
                             height=20,  # Количество символов по горизонтали
                             bg="#171b22",
                             fg="#cad0d9",
                             font=('consolas', '11'),
                             insertbackground="white",
                             )

            txt.place(
                y=26,
                relheight=1,
                relx=index,
                relwidth=(1 / count_console),
            )
            index += 1 / count_console

            ptr_arr_textWidget.append(txt)
            frameConsole.pack(fill="both", expand=True)
        return ptr_arr_textWidget

    def __del(self):
        self.Arr_textWidget = []
        self.windowTk.destroy()
        SeverMg.Is_ImLive = False

    @staticmethod
    def get_setting_socket():
        """
        Получить настройки сокета
        """
        dirs = dirname(__file__).replace("\\", "/").split("/")[:-2]
        dirs.append("setting_socket.json")
        with open("/".join(dirs), "r") as f:
            res = json.load(f)
        return res["InitTitleName"], res["HOST"], res["PORT"]


if __name__ == '__main__':
    ...
