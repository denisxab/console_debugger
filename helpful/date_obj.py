__all__ = [
	"DATA_FLAG",
	"INIT_TITLE_NAME_FLAG",
	"END_SEND",
	"SOCKET_FILE",
	"DataForSocket",
	"ServerError",
	"ViewRoot",
]

from pickle import dumps, loads
from socket import socket
from typing import List, Tuple, Final, Optional

from path_helper import root_path

DATA_FLAG: Final[bytes] = b'\0'  # Обычные данные
INIT_TITLE_NAME_FLAG: Final[bytes] = b'\1'  # Нужно создать консоли
END_SEND: Final[bytes] = b'\2'  # Если данные не удалось распаковать
KEY_TRUE_CONNECT: Final[str] = "TRUE_CONNECT"  # Ключ подтверждения того что мы получились на правильный порт
SIZE_BUFFER: Final[int] = 8  # Размер для числа которое указывает размер следующего за ним сегмента (Размер в битах)
SOCKET_FILE: Final[str] = root_path(-1, "console_debugger.socket")  # Путь к сокет файлу


class ServerError(BaseException):    ...


class DataForSocket:

	# SERVER
	@staticmethod
	def SendTrueConnect(user: socket):
		"""
		Отправить ключевое слово, в подтверждение о подключение
		"""
		user.send(KEY_TRUE_CONNECT.encode("ascii"))

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
			return END_SEND, 0, [""]

	# CLIENT
	@staticmethod
	def CheckResponseWithServer(data_validate: bytes) -> bool:
		"""
		Проверить ответ сервера на корректность.
		"""
		return True if data_validate.decode("ascii") == KEY_TRUE_CONNECT else False

	@staticmethod
	def SendInitTitleName(client_socket: socket, init_title_name: List[str]):
		"""
		Отправить заголовки консолей
		"""
		data = dumps(
			(INIT_TITLE_NAME_FLAG, -1, init_title_name),
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
			(DATA_FLAG, id_, text_send),
			protocol=3)
		len_ = len(data).to_bytes(SIZE_BUFFER, byteorder='big')
		# print("SendDataObj")
		# print(f"{data}:{len(data)}")
		# print(f"{len_}: {len(len_)}")
		client_socket.send(len_)
		client_socket.send(data)


class ViewRoot:

	def __init__(self):
		from logic.mg_get_socket import MgGetSocket
		self.SeverGet: Optional[MgGetSocket] = None

	def PrintInfo(self, text: str):        ...

	def UpdateTitle(self, l_text: List[str]):        ...

	def SendTextInIndex(self, index: int, data: str):        ...
