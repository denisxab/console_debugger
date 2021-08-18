__all__ = ["SeverMg"]

from _pickle import UnpicklingError
from collections import deque
from pickle import loads
from socket import socket, AF_INET, SOCK_STREAM
from typing import Tuple, Any


class SeverMg:
    Is_ImLive = True

    def __init__(self, QueueSendWidget: deque, Host, Port):

        self.Pt_QueueSendWidget: deque = QueueSendWidget

        self.Host: str = Host
        self.Port: int = Port

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

        self.main_loop()

    # Ждать нового подключение от клиента
    def _connect_to_client(self) -> Tuple[socket, Any]:
        user, address = self.server_sock.accept()  # Ждет данные от клиентов, не проходит дальше пока нет данных
        user.send(f"[True] You connect: Port: {self.Port}\n".encode("utf-8"))  # Отправлять можно только байты

        print(f"{self.Port}:{user.fileno()} ", "[CONNECTED] ", address)
        return user, address

    # Разорвать соединение с клиентом
    @staticmethod
    def disconnect_client(user: socket) -> None:
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
        user, address = self._connect_to_client()  # Ждем подключение клиента

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
                        id_, data_l = loads(b"".join(fragment))
                        # print(f"{self.Port}:{user.fileno()} ", id_, data_l)
                        self.Pt_QueueSendWidget.append((id_, data_l))

                    fragment.clear()

                except ConnectionResetError:  # Если клиент разорвал соединение
                    user.close()  # Закрыть соединение с клиентом
                    print('{} {} {}'.format("*" * 40,
                                            "Клиент разорвал соединение",
                                            "*" * 40,
                                            ))

                except (UnpicklingError, EOFError):
                    #user.close()  # Закрыть соединение с клиентом
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
                user, address = self._connect_to_client()

        exit()


if __name__ == '__main__':
    ...
