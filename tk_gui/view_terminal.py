from os.path import dirname
from tkinter import Tk, Frame, Button, scrolledtext, OUTSIDE, Text
from typing import List


# class TextScrollCombo(ttk.Frame):
#
#     def __init__(self, root, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # ensure a consistent GUI size
#         self.grid_propagate(False)
#         # implement stretchability
#         self.grid_rowconfigure(0, weight=1)
#         self.grid_columnconfigure(0, weight=1)
#         # create a Text widget
#         self.txt = Text(self)
#         self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
#         style = ttk.Style(root)
#         style.configure("Vertical.TScrollbar",
#                         background="#487861",
#                         troughcolor="#171b22",
#                         gripcount=0,  # отключает лишнее на полосе прокрутки
#                         darkcolor="DarkGreen",
#                         lightcolor="LightGreen",
#                         bordercolor="#487861",
#                         arrowcolor="#171b22",
#                         )
#         style.theme_use("clam")
#         scrollb = ttk.Scrollbar(self, command=self.txt.yview, style='Vertical.TScrollbar')
#         scrollb.grid(row=0, column=1, sticky='nsew')
#         self.txt['yscrollcommand'] = scrollb.set


class View:
    Arr_textWidget: List[scrolledtext.ScrolledText] = []

    def __init__(self, names_console: List[str]):

        self.windowTk = Tk()
        self.windowTk.title("debugger_tk")
        self.windowTk.iconbitmap(f"{dirname(__file__)}\icons.ico")
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
            with open(f"{dirname(__file__)}\config.txt", "r")as f:
                return f.read()

        except FileNotFoundError:
            return f"{600}x{600}+{self.windowTk.winfo_screenwidth() // 2 - 160}+{self.windowTk.winfo_screenheight() // 2 - 160}"

    def __set_geometer(self, is_exit=True):
        with open(f"{dirname(__file__)}\config.txt", "w")as f:
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
        ptr_arr_textWidget: List[scrolledtext.ScrolledText] = []
        index = 0
        count_console = len(names_console)
        # нумерация строк здесь начинается с единицы, а нумерация столбцов – с нуля.
        for index_console, item in enumerate(names_console):
            ButtonLabel = Button(frameConsole, text=item, bg="#0e1117", fg="#cad0d9",
                                 height=1,
                                 command=lambda i=index_console: View.clear_console(i))

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
        View.Arr_textWidget = []
        self.windowTk.destroy()


if __name__ == '__main__':
    ...
