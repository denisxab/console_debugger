__all__ = ["_MgGetSocket"]

import json
from os.path import dirname
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from typing import Optional

from date_obj import DataForSocket


class _MgGetSocket:

    def __init__(self):
        self.Host, self.Port = _MgGetSocket._get_setting_socket()

        self.user: Optional[socket] = None
        self.address = None

        # Конфигурация сокета, конфигурации должны быть одинаковые между сервером и клиентов
        self.server_sock: socket = socket(
            family=AF_INET,
            type=SOCK_STREAM,
        )

        # Адрес прослушивания
        self.server_sock.bind((
            self.Host,  # Адрес
            self.Port,  # Порт
        ))

        # Разрешает сколько количество подключений
        self.server_sock.listen(1)

    # Ждать нового подключение от клиента
    def ConnectToClient(self):
        def thread_for_wait_client():
            self.user, self.address = self.server_sock.accept()  # Ждет данные от клиентов, не проходит дальше пока нет данных
            DataForSocket.SendTrueConnect(self.user)  # Отправлять можно только байты
            # print(f"{self.Port}:{self.user.fileno()} ", "[CONNECTED] ", self.address)

        Thread(target=thread_for_wait_client, daemon=True).start()

    def UserClose(self):
        self.user.close()
        self.user = None
        # print("Ждем")
        self.ConnectToClient()

    @staticmethod
    def _get_setting_socket():
        """
        Получить настройки сокета
        """
        dirs = dirname(__file__).replace("\\", "/").split("/")[:-1]
        dirs.append("setting_socket.json")
        with open("/".join(dirs), "r") as f:
            res = json.load(f)
        return res["HOST"], res["PORT"]

    def __repr__(self) -> str:
        return f"Server:\n {self.Host}:{self.Port}\nConnect:\n {self.user.fileno() if self.user else None}"

    # Разорвать соединение с клиентом
    # @staticmethod
    # def disconnect_client(user: socket) -> None:
    #     user.send("[EXIT]".encode("utf-8"))
    #     user.close()
    #
    #     print('{} {} {}'.format("*" * 40,
    #                             "Disconnect Client",
    #                             "*" * 40,
    #                             ))
    # Проверить данные, на условие разрыва соединения по инициативе клиента
    # @staticmethod
    # def is_connected(data: str) -> bool:
    #     return False if data == "exit" else True


if __name__ == '__main__':
    ...
