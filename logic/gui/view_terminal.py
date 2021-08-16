from collections import deque
from os.path import dirname
from tkinter import Tk, Frame, Button, scrolledtext, OUTSIDE, Text
from typing import List, Optional

from console_debugger.logic.stup_debugger import InitTitleName


class ViewTk:
    QueueSendWidget = deque()

    def __init__(self, names_console: List[str]):
        self.title_name: List[str] = []

        self.windowTk = Tk()
        self.windowTk.title("debugger_tk")
        # self.windowTk.iconbitmap(f"{dirname(__file__)}\icons.ico")
        self.windowTk.attributes("-topmost", True)
        self.windowTk.geometry(self.__get_geometer())

        self.ConstructWidget(names_console)

        self.windowTk.protocol("WM_DELETE_WINDOW", self.__del)

        self.CheckUpdateQueue()

        self.windowTk.mainloop()

    def CheckUpdateQueue(self):
        if ViewTk.QueueSendWidget:
            id_, data = ViewTk.QueueSendWidget.popleft()
            if id_ == InitTitleName:
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

        self.Arr_textWidget: List[scrolledtext.ScrolledText] = self._FormHorizonConsole(names_console,
                                                                                        self.frameConsole)

    def DeconstructWidget(self):
        self.bt1.destroy()
        self.frameConsole.destroy()

    def __get_geometer(self) -> str:
        try:
            with open(f"{dirname(__file__)}\config.txt", "r")as f:
                return f.read()

        except FileNotFoundError:
            return f"{600}x{600}+{self.windowTk.winfo_screenwidth() // 2 - 160}+{self.windowTk.winfo_screenheight() // 2 - 160}"

    def __set_geometer(self):
        with open(f"{dirname(__file__)}\config.txt", "w")as f:
            x = self.windowTk.winfo_x()
            y = self.windowTk.winfo_y()
            w = self.windowTk.winfo_width()
            h = self.windowTk.winfo_height()
            f.write(f"{w}x{h}+{x}+{y}")

    def clear_console(self, index_console: int):
        self.Arr_textWidget[index_console].delete(1.0, "end")

    def _FormHorizonConsole(self, names_console: List[str],
                            frameConsole: Frame,
                            ) -> List[scrolledtext.ScrolledText]:
        """
        Формирует горизонтально консоли и отображает её

        :type frameConsole: self.frameConsole = Frame(self.windowTk, width=100, height=200)
        :param count_console: Количество созданных консолей
        :return: список с экземплярами консолей
        """
        ptr_arr_textWidget: List[scrolledtext.ScrolledText] = []
        index = 0
        count_console = len(names_console)
        # нумерация строк здесь начинается с единицы, а нумерация столбцов – с нуля.
        for index_console, item in enumerate(names_console):
            ButtonLabel = Button(frameConsole, text=item, bg="#0e1117", fg="#cad0d9",
                                 height=1,
                                 command=lambda i=index_console: self.clear_console(i))

            ButtonLabel.place(
                relx=index,
                relwidth=(1 / count_console),
                bordermode=OUTSIDE,
            )

            txt = Text(frameConsole,
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


if __name__ == '__main__':
    ...
