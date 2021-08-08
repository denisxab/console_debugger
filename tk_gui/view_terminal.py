from tkinter import Tk, scrolledtext, Frame, Button
from typing import List


class View:
    Arr_textWidget: List[scrolledtext.ScrolledText] = []

    def __init__(self, names_console: List[str]):
        self.windowTk = Tk()
        self.windowTk.title("debugger_tk")
        self.windowTk.iconbitmap('icons.ico')
        self.windowTk.attributes("-topmost", True)
        self.windowTk.geometry(self.__get_geometer())

        self.frameConsole = Frame(self.windowTk,
                                  width=100,
                                  height=200)

        bt1 = Button(self.windowTk, bg="#171b22", command=lambda: None).pack(fill="x")

        View.Arr_textWidget = self._FormHorizonConsole(names_console, self.frameConsole)
        bt_save_geometry_windows = Button(self.windowTk,
                                          text="save geometry",
                                          bg="#487861",
                                          command=lambda: self.__set_geometer(False)).pack(fill="x")

        self.windowTk.protocol("WM_DELETE_WINDOW", self.__del)
        self.windowTk.mainloop()

    def __get_geometer(self) -> str:
        try:
            with open("config.txt", "r")as f:
                return f.read()

        except FileNotFoundError:
            return f"{600}x{600}+{self.windowTk.winfo_screenwidth() // 2 - 160}+{self.windowTk.winfo_screenheight() // 2 - 160}"

    def __set_geometer(self, is_exit=True):
        with open("config.txt", "w")as f:
            x = self.windowTk.winfo_x()
            y = self.windowTk.winfo_y()
            w = self.windowTk.winfo_width()
            h = self.windowTk.winfo_height()
            f.write(f"{w}x{h}+{x}+{y}")

    @classmethod
    def clear_console(cls, index_console: int):
        cls.Arr_textWidget[index_console].delete(1.0, "end")

    @staticmethod
    def _FormHorizonConsole(names_console: List[str],
                            frameConsole: Frame,
                            ) -> List[scrolledtext.ScrolledText]:
        """
        Формирует горизонтально консоли и отображает её

        :type frameConsole: self.frameConsole = Frame(self.windowTk, width=100, height=200)
        :param count_console: Количество созданных консолей
        :return: список с экземплярами консолей
        """
        ptr_arr_textWidget = []
        index = 0
        count_console = len(names_console)
        # нумерация строк здесь начинается с единицы, а нумерация столбцов – с нуля.
        for index_console, item in enumerate(names_console):
            txt = scrolledtext.ScrolledText(frameConsole,
                                            width=80,  # Количество символов по вертикали
                                            height=20,  # Количество символов по горизонтали
                                            bg="#171b22",
                                            fg="#cad0d9"
                                            )
            txt['font'] = ('consolas', '12')

            txt.place(
                rely=0.05,
                relx=index,
                relwidth=(1 / count_console),
                relheight=1)

            ButtonLabel = Button(frameConsole, text=item, bg="#0e1117", fg="#cad0d9",
                                 command=lambda i=index_console: View.clear_console(i))
            ButtonLabel.place(
                rely=0,
                relx=index,
                relwidth=(1 / count_console),
            )

            index += 1 / count_console

            ptr_arr_textWidget.append(txt)
            frameConsole.pack(fill="both", expand=True)
        return ptr_arr_textWidget

    def __del(self):
        View.Arr_textWidget = []
        self.windowTk.destroy()


if __name__ == '__main__':

    import random
    import string
    from debugger import *

    Debug = Debugger(**dDEBUG)
    Info = Debugger(**dINFO)
    Warning = Debugger(**dWARNING)
    TEST = Debugger("TEST")

    Debugger.GlobalManager(typePrint='tk')

    random_word = lambda: "".join(random.choice(string.ascii_letters) for j in range(random.randint(1, 40)))

    for i in range(5):
        printD(Debug, random_word())
        printD(Info, random_word())
        printD(Warning, random_word())
        printD(TEST, random_word())
        time.sleep(0.3)
