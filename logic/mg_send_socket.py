__all__ = ["MgSendSocket"]

import json
from datetime import datetime
from os.path import dirname
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
from typing import List

from console_debugger.helpful.template_obj import ServerError
from helpful.date_obj import DataForSocket


class MgSendSocket:

	def __init__(self):
		self.Host, self.Port = MgSendSocket._get_setting_socket()

		# Имя файла для записи данных на случай если возникнет критическая ошибка с сервером, а очередь полная
		self.FileNameSaveIfServerError: str = "{path_f}/save_file_name{name_f}.txt".format(
			path_f=dirname(argv[0]).replace('\\', '/'),
			name_f=datetime.now().strftime('%H_%M_%S'),
		)

		# Конфигурация сокета, конфигурации должны быть одинаковые между сервером и клиентов
		self.client_sock: socket = socket(
			family=AF_INET,
			type=SOCK_STREAM,
		)

	def PickleDataAndSendToServer(self, id_: int, text_send: List[str]):
		"""
		Сериализовать и отправить данные на сервер
		"""
		try:
			DataForSocket.SendDataObj(self.client_sock, id_, text_send)  # Отправить данные на сервер
		except BaseException as e:
			print(f"{e} | but data save to\n{self.FileNameSaveIfServerError}")
			self._save_output_to_file(text_send[0])

	def ConnectToServer(self, init_title_name: List[str]) -> bool:
		"""
		Соединиться с сервером
		"""

		try:
			self.client_sock.connect((self.Host, self.Port))
			data = self.client_sock.recv(1024)
			# Проверка того что мы подключились именно к нужному серверу
			if DataForSocket.CheckResponseWithServer(data):
				DataForSocket.SendInitTitleName(self.client_sock, init_title_name)
				print(data.decode("utf-8"))
				return True
			else:
				raise ServerError("Сервер отправил не верный ключ подтверждения подключения")

		except (ConnectionRefusedError, OSError, ServerError) as e:
			print(f"{e}\nServerError: Ошибка сервера")
			return False

	def _save_output_to_file(self, data_str: str):
		"""
		# Метод для сохранения данных в файл, вызывать при критических ошибках с сервером, и полной очередью
		"""
		with open(self.FileNameSaveIfServerError, 'a', encoding='utf-8') as f:
			f.write(data_str)

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
