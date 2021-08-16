import pickle
import socket
from collections import deque
from datetime import datetime
from os.path import dirname
from sys import argv
from typing import List


class ServerError(BaseException):
    ...


class _MgSendSocketData:
    QueueSendPort = deque()

    InitTitleName = -1
    Exit = -2

    def __init__(self, init_title_name: List[str], Host='localhost', Port=50007):

        _MgSendSocketData.Is_ImLive = True
        # Имя файла для записи данных на случай если возникнет критическая ошибка с сервером, а очередь полная
        self.FileNameSaveIfServerError = "{path_f}/save_file_name{name_f}.txt".format(
            path_f=dirname(argv[0]).replace('\\', '/'),
            name_f=datetime.now().strftime('%H_%M_%S'),
        )
        self.Port = Port
        self.Host = Host

        # Конфигурация сокета, конфигурации должны быть одинаковые между сервером и клиентов
        self.client_sock = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
        )

        self._init_connect_to_server()
        self._connect_to_server(init_title_name)

        # self._main_loop(init_title_name)

    def _init_connect_to_server(self):
        """
        # Подключиться к серверу
        """
        try:
            self.client_sock.connect((self.Host, self.Port))

        except ConnectionRefusedError as e:
            _MgSendSocketData.Is_ImLive = False
            print(f"ServerError: Сервер не отвечает")

    def pickle_data_and_send_to_server(self, id_: int, names_var: list, textOutput: str, *args: str):
        """
         # Сериализовать и отправить данные на сервер
        """

        names_var_str: str = "¦"
        if names_var:
            names_var_str = f"({', '.join(names_var)})¦"

        res = "{next_steep}\n{data}{name_var}\n{textOutput}\n".format(
            next_steep=f"{'-' * (len(names_var_str) + 7)}¬",
            data=datetime.now().strftime('%H:%M:%S'),
            name_var=names_var_str,
            textOutput=f"{textOutput} {' '.join(str(item) for item in args)}",
        )

        try:
            data = pickle.dumps((id_, res), protocol=3)
            self.client_sock.send(data)  # Отправить данные на сервер
        except BaseException as e:
            print(f"{e} | but data save to\n{self.FileNameSaveIfServerError}")
            self._SaveOutputToFile(res)

    def _connect_to_server(self, init_title_name: List[str]):
        """
        # Соединиться с сервером
        """

        data = self.client_sock.recv(1024)

        # Проверка того что мы подключились именно к нужному серверу
        if data.decode("utf-8")[:6] != "[True]":
            _MgSendSocketData.Is_ImLive = False
            print(f"ServerError: Сервер отправил не верный ключ подтверждения подключения")
        else:
            self.client_sock.send(pickle.dumps((_MgSendSocketData.InitTitleName, init_title_name), protocol=3))
            print(data.decode("utf-8"))

    def _SaveOutputToFile(self, data_str: str):
        """
        # Метод для сохранения данных в файл, вызывать при критических ошибках с сервером, и полной очередью
        """
        pass  ##!!!

        # with open(self.FileNameSaveIfServerError, 'a', encoding='utf-8') as f:
        #     f.write(data_str)
