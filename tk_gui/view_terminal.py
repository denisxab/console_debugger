import _pickle
import pickle
import socket
from collections import deque
from os.path import dirname
from threading import Thread
from tkinter import Tk, Frame, Button, scrolledtext, OUTSIDE, Text
from typing import List, Tuple, Any, Optional


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


class SeverMg:
    InitTitleName = -1
    Exit = -2
    Is_ImLive = True

    def __init__(self, Host='localhost', Port=50007):
        self.View = self._initView()
        self.View.start()

        self.Host: str = Host
        self.Port: int = Port

        # Конфигурация сокета, конфигурации должны быть одинаковые между сервером и клиентов
        self.server_sock: socket.socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
        )

        # Адрес прослушивания
        self.server_sock.bind((
            self.Host,  # Адрес
            self.Port,  # Порт
        ))

        # Разрешает сколько количество подключений
        self.server_sock.listen(1)

        self.main_loop()

    # Ждать нового подключение от клиента
    def init_connect_to_client(self, port: int) -> Tuple[socket.socket, Any]:
        user, address = self.server_sock.accept()  # Ждет данные от клиентов, не проходит дальше пока нет данных
        user.send(f"[True] You connect: Port: {self.Port}\n".encode("utf-8"))  # Отправлять можно только байты

        print(f"{self.Port}:{user.fileno()} ", "[CONNECTED] ", address)
        return user, address

    # Разорвать соединение с клиентом
    @staticmethod
    def disconnect_client(user: socket.socket) -> None:
        user.send("[EXIT]".encode("utf-8"))
        user.close()

        print('{} {} {}'.format("*" * 40,
                                "Disconnect Client",
                                "*" * 40,
                                ))

    # Проверить данные, на условие разрыва соединения по инициативе клиента
    @staticmethod
    def is_connected(data: str) -> bool:
        return False if data == "exit" else True

    def main_loop(self) -> None:

        print(self.Port, " Ran SeverMg")
        user, address = self.init_connect_to_client(self.Port)  # Ждем подключение клиента

        fragment = deque()

        # Проверить то что окно не закрыто
        while SeverMg.Is_ImLive:
            if user.fileno() != -1:  # Если сервер не отсоединился от клиента
                try:
                    # Раскодировать данные в строку #data.decode("utf-8")  # Раскодировать данные в строку
                    d = b"\1"
                    while d != b".":
                        d = user.recv(1)
                        if not d:
                            user.close()  # Закрыть соединение с клиентом
                            break
                        fragment.append(d)
                    else:
                        id_, data_l = pickle.loads(b"".join(fragment))
                        # print(f"{self.Port}:{user.fileno()} ", id_, data_l)
                        ViewTk.QueueSendWidget.append((id_, data_l))

                    fragment.clear()

                except ConnectionResetError:  # Если клиент разорвал соединение
                    user.close()  # Закрыть соединение с клиентом
                    print('{} {} {}'.format("*" * 40,
                                            "Клиент разорвал соединение",
                                            "*" * 40,
                                            ))

                except (_pickle.UnpicklingError, EOFError):
                    user.close()  # Закрыть соединение с клиентом
                    print(fragment)
                    print('{} {} {}'.format("$" * 40,
                                            "Ошибка распаковки",
                                            "$" * 40,
                                            ))

                except ConnectionAbortedError:  # Если клиенту невозможно отправить данные от отключаемся
                    user.close()  # Закрыть соединение с клиентом
                    print('{} {} {}'.format("$" * 40,
                                            "Если клиенту невозможно отправить данные",
                                            "$" * 40,
                                            ))

            else:  # Если сервер отсоединился от клиента, то  ждать следующего подключение
                print("Ждем")
                user, address = self.init_connect_to_client(self.Port)

        exit()

    @staticmethod
    def _initView():
        return Thread(
            target=ViewTk,
            args=(["None"],),
            daemon=True,
        )


class MainView:
    ...


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
            if id_ == SeverMg.InitTitleName:
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
        SeverMg.Is_ImLive = False
        self.Arr_textWidget = []
        self.windowTk.destroy()


if __name__ == '__main__':
    SeverMg("localhost", 50007)
