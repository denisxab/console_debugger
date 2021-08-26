__all__ = ["MgGetSocket"]

from json import load
from os.path import dirname
from pickle import UnpicklingError
from socket import socket, AF_INET, SOCK_STREAM, gaierror
from threading import Thread
from typing import Optional, List

from console_debugger.helpful.date_obj import DataForSocket, InitTitleNameFlag, DataFlag, EndSend
from console_debugger.helpful.template_obj import ViewRoot


class MgGetSocket:

	def __init__(self, Host: str = None, Port: int = None):
		if not Host and not Port:
			self.Host, self.Port = MgGetSocket._get_setting_socket()
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
		self.UserClose()
		self.user, self.address = self.server_sock.accept()  # Ждет данные от клиентов, не проходит дальше пока нет данных
		# print(f"{self.Port}:{self.user.fileno()} ", "[CONNECTED] ", self.address)
		DataForSocket.SendTrueConnect(self.user)  # Отправлять можно только байты

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

	@staticmethod
	def RunThread(root_: ViewRoot, Host: str = None, Port: int = None):
		Thread(target=MgGetSocket.CheckUpdateServer,
		       args=(root_, Host, Port),
		       daemon=True, ).start()

	def UserClose(self):
		if self.user:
			self.user.close()
			self.user = None

	@staticmethod
	def CheckUpdateServer(root_: ViewRoot, Host: str, Port: int):
		"""
		Проверять данные из сокета и обновлять внутреннею структуру
		"""

		# Server
		try:
			root_.SeverGet = MgGetSocket(Host, Port)
		except (gaierror, OSError) as e:
			root_.SeverGet = None
			root_.PrintInfo(f"# {e}")
			exit(0)

		root_.PrintInfo("# Run Server")
		root_.SeverGet.ConnectToClient()  # Ждем подключение клиента
		root_.PrintInfo(f"# {root_.SeverGet.Host}:{root_.SeverGet.Port}\n")

		#
		title_name: List[str] = []

		while root_.SeverGet:

			if root_.SeverGet.user:
				if root_.SeverGet.user.fileno() != -1:  # Если сервер не отсоединился от клиента
					try:
						flag, id_, data_l = DataForSocket.GetDataObj(root_.SeverGet.user)

						if flag == DataFlag:
							root_.SendTextInIndex(id_, data_l[0])

						elif flag == InitTitleNameFlag:
							if title_name != data_l:
								title_name = data_l
								root_.UpdateTitle(data_l)

						elif flag == EndSend:
							root_.SeverGet.ConnectToClient()

					except ConnectionAbortedError:  # Если клиенту невозможно отправить данные от отключаемся
						root_.PrintInfo("Если клиенту невозможно отправить данные")
						root_.SeverGet.ConnectToClient()

					except ConnectionResetError:  # Если клиент разорвал соединение
						root_.PrintInfo("Клиент разорвал соединение")
						root_.SeverGet.ConnectToClient()

					except (UnpicklingError, EOFError):  # Не получилось распаковать данные
						root_.PrintInfo("Ошибка распаковки")

				else:  # Если сервер отсоединился от клиента, то ждать следующего подключение
					root_.SeverGet.ConnectToClient()
			else:
				root_.SeverGet.ConnectToClient()


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
