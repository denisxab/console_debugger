__all__ = ["_MgGetSocket"]

from json import load
from os.path import dirname
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from typing import Optional

from date_obj import DataForSocket


class _MgGetSocket:

	def __init__(self, *, Host: str = None, Port: int = None):
		if not Host and not Port:
			self.Host, self.Port = _MgGetSocket._get_setting_socket()
		else:
			self.Host, self.Port = Host, Port

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
		self.user, self.address = self.server_sock.accept()  # Ждет данные от клиентов, не проходит дальше пока нет данных
		# print(f"{self.Port}:{self.user.fileno()} ", "[CONNECTED] ", self.address)
		DataForSocket.SendTrueConnect(self.user)  # Отправлять можно только байты

	def UserClose(self):
		if self.user:
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
			res = load(f)
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
