__all__ = ["_MgGetSocket"]

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from typing import Optional

from date_obj import DataForSocket


class _MgGetSocket:
    Is_ImLive = True

    def __init__(self, Host, Port):
        self.Host: str = Host
        self.Port: int = Port

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
    def connect_to_client(self):
        def thread_for_wait_client():
            self.user, self.address = self.server_sock.accept()  # Ждет данные от клиентов, не проходит дальше пока нет данных
            self.user.send(DataForSocket.true_connect_server())  # Отправлять можно только байты

            print(f"{self.Port}:{self.user.fileno()} ", "[CONNECTED] ", self.address)

        Thread(target=thread_for_wait_client, daemon=True).start()

    def user_close(self):
        self.user.close()
        self.user = None

    def __repr__(self)->str:
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
