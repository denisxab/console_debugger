"""
Графическая оболочка
"""
__all__ = ["ViewTk"]

import json
from collections import deque
from os.path import dirname
from pickle import UnpicklingError
from tkinter import Tk, Frame, Button, OUTSIDE, Text, Entry, messagebox
from typing import List, Optional

from date_obj import DataForSocket, DataFlag, InitTitleNameFlag
from .mg_get_socket import _MgGetSocket


class ViewTk:

    def __init__(self, names_console: List[str]):

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

        # Server
        HOST, PORT = ViewTk.get_setting_socket()
        self.SeverTk = _MgGetSocket(HOST, PORT)
        print(self.SeverTk.Port, " Ran SeverMg")
        self.SeverTk.connect_to_client()  # Ждем подключение клиента
        self.CheckUpdateQueue()
        #################

        self.windowTk.mainloop()

    def CheckUpdateQueue(self):

        if self.SeverTk.user:

            fragment = deque()

            if self.SeverTk.user.fileno() != -1:  # Если сервер не отсоединился от клиента
                try:
                    # Раскодировать данные в строку #data.decode("utf-8")  # Раскодировать данные в строку
                    d = b"\1"
                    while d != b".":
                        d = self.SeverTk.user.recv(1)
                        if not d:
                            self.SeverTk.user.close()  # Закрыть соединение с клиентом
                            break
                        fragment.append(d)
                    else:
                        flag, id_, data_l = DataForSocket.decode_obj_server(b"".join(fragment))

                        # print(f"{self.SeverTk.Port}:{self.SeverTk.user.fileno()} ", id_, data_l[0])

                        if flag == DataFlag:
                            self.Arr_textWidget[id_].insert("0.1", data_l[0])

                        elif flag == InitTitleNameFlag:
                            if self.title_name != data_l:
                                self.title_name = data_l
                                self.DeconstructWidget()
                                self.ConstructWidget(data_l)

                    fragment.clear()
                except ConnectionResetError:  # Если клиент разорвал соединение
                    self.SeverTk.user_close()  # Закрыть соединение с клиентом
                    print('{} {} {}'.format("*" * 40,
                                            "Клиент разорвал соединение",
                                            "*" * 40,
                                            ))

                except (UnpicklingError, EOFError):
                    # user.close()  # Закрыть соединение с клиентом
                    print(fragment)
                    print('{} {} {}'.format("$" * 40,
                                            "Ошибка распаковки",
                                            "$" * 40,
                                            ))

                except ConnectionAbortedError:  # Если клиенту невозможно отправить данные от отключаемся
                    self.SeverTk.user_close()  # Закрыть соединение с клиентом
                    print('{} {} {}'.format("$" * 40,
                                            "Если клиенту невозможно отправить данные",
                                            "$" * 40,
                                            ))

            else:  # Если сервер отсоединился от клиента, то  ждать следующего подключение
                print("Ждем")
                self.SeverTk.user_close()
                self.SeverTk.connect_to_client()

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

    @staticmethod
    def display_info(message: str):
        messagebox.showinfo("Command", message)

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

    def __execute_button(self, event, index_console: int, EntryInput_obj: Entry):
        """
        # clear = Отчистить консоль

        # save <name> <path> = сохранить в файл
            - `name` имя файла
            - `path` путь к папке

            save test.txt D:\

        # g info = Показать глобальные настройки
        """

        command = EntryInput_obj.get().split()

        if command[0] == "clear":
            self.Arr_textWidget[index_console].delete(1.0, "end")
            EntryInput_obj.delete(0, "end")

        elif len(command) == 3 and command[0] == "save":
            path_ = "{}/{}".format(command[2].replace("\\", "/"), command[1])
            with open(path_, "w", encoding="utf-8")as f:
                f.write(self.Arr_textWidget[index_console].get(1.0, "end"))

            ViewTk.display_info(f"{index_console} >> {path_}")
            EntryInput_obj.delete(0, "end")

        elif command[0] == 'g' and command[1] == "info":
            ViewTk.display_info(f"{repr(self.SeverTk)}\n-----\nLen all debugger:\n {len(self.Arr_textWidget)}")
            EntryInput_obj.delete(0, "end")

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
            EntryInput = Entry(frameConsole,
                               bg="#0e1117", fg="#cad0d9",

                               )

            EntryInput.bind('<Return>', lambda v, i=index_console, e=EntryInput: self.__execute_button(None, i, e))

            EntryInput.insert(0, "clear")

            EntryInput.place(
                relx=index,

                relwidth=(1 / count_console),

                bordermode=OUTSIDE,
            )

            ButtonExecute: Button = Button(frameConsole,
                                           text=item,
                                           bg="#0e1117",
                                           fg="#cad0d9",
                                           height=1,
                                           command=lambda i=index_console, e=EntryInput: self.__execute_button(None, i,
                                                                                                               e))

            ButtonExecute.place(
                y=20,
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
                y=46,
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
        _MgGetSocket.Is_ImLive = False

    @staticmethod
    def get_setting_socket():
        """
        Получить настройки сокета
        """
        dirs = dirname(__file__).replace("\\", "/").split("/")[:-2]
        dirs.append("setting_socket.json")
        with open("/".join(dirs), "r") as f:
            res = json.load(f)
        return res["HOST"], res["PORT"]


if __name__ == '__main__':
    ...
