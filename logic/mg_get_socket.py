__all__ = ["MgGetSocket"]

from os import path, remove
from pickle import UnpicklingError
from socket import socket, SOCK_STREAM, gaierror, AF_UNIX
from threading import Thread
from typing import Optional, List

from helpful.date_obj import DataForSocket, INIT_TITLE_NAME_FLAG, DATA_FLAG, END_SEND, SOCKET_FILE, ViewRoot


class MgGetSocket:
	
	def __init__(self):
		
		if path.exists(SOCKET_FILE):
			remove(SOCKET_FILE)
		
		self.user: Optional[socket] = None
		self.address = None
		
		# Конфигурация сокета, конфигурации должны быть одинаковые между сервером и клиентов
		self.server_sock: socket = socket(
				family=AF_UNIX,
				type=SOCK_STREAM,
		)
		
		# Адрес прослушивания
		self.server_sock.bind(SOCKET_FILE)
		
		# Разрешает сколько количество подключений
		self.server_sock.listen(1)
	
	# Ждать нового подключение от клиента
	def ConnectToClient(self):
		self.UserClose()
		self.user, self.address = self.server_sock.accept()  # Ждет данные от клиентов, не проходит дальше пока нет данных
		DataForSocket.SendTrueConnect(self.user)  # Отправлять можно только байты
	
	@staticmethod
	def RunThread(root_: ViewRoot):
		Thread(target=MgGetSocket.CheckUpdateServer,
		       args=(root_,),
		       daemon=True, ).start()
	
	def UserClose(self):
		if self.user:
			self.user.close()
			self.user = None
	
	@staticmethod
	def CheckUpdateServer(root_: ViewRoot):
		"""
		Проверять данные из сокета и обновлять внутреннею структуру
		"""
		
		# Server
		try:
			root_.SeverGet = MgGetSocket()
		except (gaierror, OSError) as e:
			root_.SeverGet = None
			root_.PrintInfo(f"# {e}")
			exit(0)
		
		root_.SeverGet.ConnectToClient()  # Ждем подключение клиента
		
		#
		titleName: List[str] = []
		
		while root_.SeverGet:
			
			if root_.SeverGet.user:
				if root_.SeverGet.user.fileno() != -1:  # Если сервер не отсоединился от клиента
					try:
						flag, id_, data_l = DataForSocket.GetDataObj(root_.SeverGet.user)
						
						if flag == DATA_FLAG:
							root_.SendTextInIndex(id_, data_l[0])
						
						elif flag == INIT_TITLE_NAME_FLAG:
							if titleName != data_l:
								titleName = data_l
								root_.UpdateTitle(data_l)
						
						elif flag == END_SEND:
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
		
		root_.SeverGet.close()
	
	def close(self):
		self.server_sock.close()


if __name__ == '__main__':
	...
