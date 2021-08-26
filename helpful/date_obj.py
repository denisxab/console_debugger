__all__ = ["DataForSocket",
           "DataFlag",
           "InitTitleNameFlag",
           "EndSend"]

from collections import deque
from pickle import dumps, loads
from socket import socket
from typing import List, Tuple, Final

DataFlag: Final[bytes] = b'\0'  # Обычные данные
InitTitleNameFlag: Final[bytes] = b'\1'  # Нужно создать консоли
EndSend: Final[bytes] = b'\2'  # Если данные не удалось распаковать
MyKey: Final[str] = "TRUE_CONNECT"  # Ключ подтверждения того что мы получились на правильный порт
SIZE_BUFFER: int = 8


class DataForSocket:

	# SERVER
	@staticmethod
	def SendTrueConnect(user: socket):
		"""
		Отправить ключевое слово, в подтверждение о подключение
		"""
		user.send(MyKey.encode("ascii"))

	@staticmethod
	def GetDataObj(user: socket) -> Tuple[bytes, int, List[str]]:
		"""
		Получить из сокета, данные сформированные `SendDataObj()`
		:return: флаг, id, данные
		"""
		size_data = user.recv(SIZE_BUFFER)
		if size_data:
			data_bytes = user.recv(int.from_bytes(size_data, byteorder="big"))
			# with open("test.txt", "a")as f:
			# 	print(f"{d}:{len(d)}", file=f)
			# 	print(f"{data}:{len(data)}", file=f)
			# return DataFlag, 0, ["0"]
			return loads(data_bytes)
		else:
			return EndSend, 0, [""]

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
		data = dumps(
			(InitTitleNameFlag, -1, init_title_name),
			protocol=3)
		len_ = len(data).to_bytes(SIZE_BUFFER, byteorder='big')
		# print("SendInitTitleName")
		# print(f"{data}:{len(data)}")
		# print(f"{len_}: {len(len_)}")
		client_socket.send(len_)
		client_socket.send(data)

	@staticmethod
	def SendDataObj(client_socket: socket, id_: int, text_send: List[str]):
		"""
		Отправить на сервер, данные для конкретной консоли
		"""
		data = dumps(
			(DataFlag, id_, text_send),
			protocol=3)
		len_ = len(data).to_bytes(SIZE_BUFFER, byteorder='big')
		# print("SendDataObj")
		# print(f"{data}:{len(data)}")
		# print(f"{len_}: {len(len_)}")
		client_socket.send(len_)
		client_socket.send(data)
