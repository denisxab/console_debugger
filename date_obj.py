__all__ = ["DataForSocket",
           "DataFlag",
           "InitTitleNameFlag", ]

from collections import deque
from dataclasses import dataclass
from pickle import dumps, loads
from socket import socket
from typing import List, Tuple

DataFlag: bytes = b'\0'  # Обычные данные
InitTitleNameFlag: bytes = b'\1'  # Нужно создать консоли
MyKey = "TRUE_CONNECT"  # Ключ подтверждения того что мы получились на правильный порт



@dataclass
class DataForSocket:

    # SERVER
    @staticmethod
    def SendTrueConnect(user: socket):
        """
        Отправить ключевое слово, в подтверждение о подключение
        """
        user.send(MyKey.encode("ascii"))

    @staticmethod
    def GetDataObj(user: socket) -> Tuple[int, int, List[str]]:
        """
        Получить из сокета, данные сформированные `SendDataObj()`

        :return: флаг, id, данные
        """
        fragment = deque()
        d = b"\1"
        while d != b".":
            d = user.recv(1)
            if not d:
                user.close()  # Закрыть соединение с клиентом
                break
            fragment.append(d)
        return loads(b"".join(fragment))

    # CLIENT
    @staticmethod
    def CheckResponseWithServer(data_validate: bytes) -> bool:
        """
        Проверить ответ сервера на корректность.
        """
        return True if data_validate.decode("ascii") == MyKey else False

    @staticmethod
    def SendInitTitleName(client_socket: socket, init_title_name: List[str]):
        """
        Отправить заголовки консолей
        """
        client_socket.send(dumps(
            (InitTitleNameFlag, -1, init_title_name),
            protocol=3))

    @staticmethod
    def SendDataObj(client_socket: socket, id_: int, text_send: List[str]):
        """
        Отправить на сервер, данные для конкретной консоли
        """
        client_socket.send(dumps(
            (DataFlag, id_, text_send),
            protocol=3))
