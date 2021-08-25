__all__ = ["ViewTui", ]

import asyncio
import os
import socket
from pickle import UnpicklingError
from typing import List, Optional

import urwid
from urw_widget import ConsolesColumns

from __init__ import *
from date_obj import DataForSocket, DataFlag, InitTitleNameFlag, EndSend
from logic.mg_get_socket import _MgGetSocket
from tui.urw_widget import MenuConsole


class ViewTui:
	palette = [
		('label_text1', 'light cyan', 'black',),
	]
	urwid.set_encoding('utf8')

	SeverTk: Optional[_MgGetSocket] = None

	def __init__(self):
		alsop = asyncio.get_event_loop()

		self.console_columns = ConsolesColumns(["1", "2", "3", "4"], self)

		self.menu = MenuConsole(self.ExecuteCommand)

		self.gInfoOverlay = urwid.Overlay(self.menu,
		                                  self.console_columns,
		                                  align="center",
		                                  valign="middle",
		                                  width=("relative", 60),
		                                  height=("relative", 30),
		                                  )

		self.loop = urwid.MainLoop(self.console_columns,
		                           palette=ViewTui.palette,
		                           event_loop=urwid.AsyncioEventLoop(loop=alsop),

		                           )
		alsop.create_task(ViewTui.CheckUpdateServer(self.console_columns))
		try:
			self.loop.run()
		except KeyboardInterrupt:
			print("Exit")
			os.system("clear")
			exit()

	def ExecuteCommand(self, output_widget: object, command: str):

		"""
		Обработчик ввода
			- `info` = Информация о сокете
			- `close` = Скрыть меню
			- `server <HOST> <PORT>` = Назначить прослушивание нового сокета
			- `help` = Подсказка
		"""

		command: List[str] = command.split()

		if command[0] == "info":
			output_widget.set_text(f"{repr(ViewTui.SeverTk)}\n")

		elif command[0] == "close":
			self.loop.widget = self.console_columns

		elif command[0] == "help":

			output_widget.set_text(ViewTui.ExecuteCommand.__doc__)

		elif len(command) == 3 and command[0] == "server":
			try:
				ViewTui.SeverTk.UserClose()
				ViewTui.SeverTk = _MgGetSocket(Host=str(command[1]), Port=int(command[2]))
				output_widget.set_text(f"{repr(ViewTui.SeverTk)}\n")
				ViewTui.SeverTk.ConnectToClient()  # Ждем подключение клиента

			except (socket.gaierror, OSError) as e:
				output_widget.set_text(f"{e}")

	@classmethod
	async def CheckUpdateServer(cls, clm: ConsolesColumns):
		"""
		Асинхронная функция по получению данных из сокета
		"""

		ViewTui.SeverTk = _MgGetSocket()

		clm.SendSelfInfo("# Run Server")
		ViewTui.SeverTk.ConnectToClient()  # Ждем подключение клиента

		clm.SendSelfInfo(f"# {ViewTui.SeverTk.Host}:{ViewTui.SeverTk.Port}\n")
		title_name: List[str] = []

		while True:
			if ViewTui.SeverTk.user:
				if ViewTui.SeverTk.user.fileno() != -1:  # Если сервер не отсоединился от клиента
					try:
						flag, id_, data_l = DataForSocket.GetDataObj(ViewTui.SeverTk.user)

						if flag == DataFlag:
							clm.SendTextInIndex(id_, data_l[0])
							await asyncio.sleep(0)

						elif flag == InitTitleNameFlag:
							if title_name != data_l:
								title_name = data_l
								clm.CreateNewTitleName(data_l)
								await asyncio.sleep(0)

						elif flag == EndSend:
							ViewTui.SeverTk.UserClose()

					except ConnectionResetError:  # Если клиент разорвал соединение
						ViewTui.SeverTk.UserClose()  # Закрыть соединение с клиентом
						clm.SendSelfInfo("Клиент разорвал соединение")

					except (UnpicklingError, EOFError):  # Не получилось распаковать данные
						clm.SendSelfInfo("Ошибка распаковки")

					except ConnectionAbortedError:  # Если клиенту невозможно отправить данные от отключаемся
						ViewTui.SeverTk.UserClose()  # Закрыть соединение с клиентом
						clm.SendSelfInfo("Если клиенту невозможно отправить данные")
				else:  # Если сервер отсоединился от клиента, то ждать следующего подключение
					ViewTui.SeverTk.UserClose()

			await asyncio.sleep(0)


if __name__ == '__main__':
	print(path)
	...
