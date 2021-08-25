__all__ = ["ViewTui", ]

from asyncio import sleep, get_event_loop
from os import system
from socket import gaierror
from pickle import UnpicklingError
from threading import Thread
from typing import List, Optional

import urwid
from console_debugger.tui.urw_widget import ConsolesColumns
from console_debugger.date_obj import DataForSocket, DataFlag, InitTitleNameFlag, EndSend
from console_debugger.tui.urw_widget import MenuConsole, ConsoleFrame
from console_debugger.logic.mg_get_socket import _MgGetSocket


class ViewTui:
	palette = [
		('label_text1', 'light cyan', 'black',),
	]
	urwid.set_encoding('utf8')

	SeverTu: Optional[_MgGetSocket] = None

	def __init__(self):

		self.console_columns: ConsolesColumns = ConsolesColumns(["1", "2", "3", "4"], self)

		self.menu = MenuConsole(self.ExecuteCommand, root_=self)

		self.gInfoOverlay = urwid.Overlay(self.menu,
		                                  self.console_columns,
		                                  align="center",
		                                  valign="middle",
		                                  width=("relative", 60),
		                                  height=("relative", 60),
		                                  )

		self.loop = urwid.MainLoop(self.console_columns,
		                           palette=ViewTui.palette, )

		self.loop.set_alarm_in(0.1, self.update_widget)
		try:
			self.__run_Thread()
			self.loop.run()
		except KeyboardInterrupt:
			print("Exit")
			system("clear")
			exit()

	def update_widget(self, loop=None, data=None):
		"""
		Пока нет обращений к приложению оно не обновляет состояние, поэтому имитируем
		обращение, для обновления данных.
		"""
		self.console_columns.update_widget()
		loop.set_alarm_in(0.1, self.update_widget)

	def ExecuteCommand(self, output_widget: object, command: str):
		"""Глобальная консоль ввода:
- `info` = Информация о сокете
- `close` = Скрыть меню
- `server <HOST> <PORT>` = Назначить прослушивание нового сокета
- `help` = Подсказка
- `run` = Перезапустить сервер"""

		command: List[str] = command.split()

		if command[0] == "info":
			output_widget.set_text(f"{repr(ViewTui.SeverTu)}\n")

		elif command[0] == "close":
			self.loop.widget = self.console_columns

		elif command[0] == "help":
			output_widget.set_text(
				f"{ConsolesColumns.keypress.__doc__}\n\n{ViewTui.ExecuteCommand.__doc__}\n\n{ConsoleFrame.ExecuteCommand.__doc__}")

		elif len(command) == 3 and command[0] == "server":
			try:
				ViewTui.SeverTu.UserClose()
				ViewTui.SeverTu = _MgGetSocket(Host=str(command[1]), Port=int(command[2]))
				output_widget.set_text(f"{repr(ViewTui.SeverTu)}\n")
				ViewTui.SeverTu.ConnectToClient()  # Ждем подключение клиента

			except (gaierror, OSError) as e:
				output_widget.set_text(f"{e}")

		elif command[0] == "run":
			if ViewTui.SeverTu is None:
				self.__run_Thread()
			else:
				output_widget.set_text(f"Сервер уже запущен")

	def __run_Thread(self):
		Thread(target=ViewTui.CheckUpdateServer,
		       args=(self.console_columns,),
		       daemon=True, ).start()

	@classmethod
	def CheckUpdateServer(cls, clm: ConsolesColumns):
		"""
		Проверять данные из сокета и обновлять внутреннею структуру
		"""

		# Server
		try:
			cls.SeverTu = _MgGetSocket()
		except OSError as e:
			cls.SeverTu = None
			clm.SendSelfInfo(f"# {e}")
			exit(0)

		clm.SendSelfInfo("# Run Server")
		cls.SeverTu.ConnectToClient()  # Ждем подключение клиента
		clm.SendSelfInfo(f"# {cls.SeverTu.Host}:{cls.SeverTu.Port}\n")
		#
		title_name: List[str] = []

		while True:
			if cls.SeverTu.user:
				if cls.SeverTu.user.fileno() != -1:  # Если сервер не отсоединился от клиента
					try:
						flag, id_, data_l = DataForSocket.GetDataObj(cls.SeverTu.user)

						if flag == DataFlag:
							clm.SendTextInIndex(id_, data_l[0])

						elif flag == InitTitleNameFlag:
							if title_name != data_l:
								title_name = data_l
								clm.CreateNewTitleName(data_l)

						elif flag == EndSend:
							cls.SeverTu.UserClose()

					except ConnectionResetError:  # Если клиент разорвал соединение
						cls.SeverTu.UserClose()  # Закрыть соединение с клиентом
						clm.SendSelfInfo("Клиент разорвал соединение")

					except (UnpicklingError, EOFError):  # Не получилось распаковать данные
						clm.SendSelfInfo("Ошибка распаковки")

					except ConnectionAbortedError:  # Если клиенту невозможно отправить данные от отключаемся
						cls.SeverTu.UserClose()  # Закрыть соединение с клиентом
						clm.SendSelfInfo("Если клиенту невозможно отправить данные")
				else:  # Если сервер отсоединился от клиента, то ждать следующего подключение
					cls.SeverTu.UserClose()


if __name__ == '__main__':
	...
