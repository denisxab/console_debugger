__all__ = ["ViewTui", ]

from os import system
from typing import List

import urwid

from console_debugger.helpful.template_obj import ViewRoot
from console_debugger.logic.mg_get_socket import MgGetSocket
from console_debugger.tui.urw_widget import ConsolesColumns
from console_debugger.tui.urw_widget import MenuConsole, ConsoleFrame


class ViewTui(ViewRoot):
	palette = [
		('label_text1', 'light cyan', 'black',),
	]
	urwid.set_encoding('utf8')

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
			super().__init__()
			MgGetSocket.RunThread(self)
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
- `help` = Подсказка"""

		"""
		- `server <HOST> <PORT>` = Назначить прослушивание нового сокета
		- `run` = Перезапустить сервер
		"""

		command: List[str] = command.split()

		if command[0] == "info":
			output_widget.set_text(f"{repr(self.SeverGet)}\n")

		elif command[0] == "close":
			self.loop.widget = self.console_columns

		elif command[0] == "help":
			output_widget.set_text(
				f"{ConsolesColumns.keypress.__doc__}\n\n{ViewTui.ExecuteCommand.__doc__}\n\n{ConsoleFrame.ExecuteCommand.__doc__}")

	# elif len(command) == 2 and command[0] == "server":
	#
	# 	try:
	# 		self.SeverGet = MgGetSocket("localhost", int(command[1]))
	# 		output_widget.set_text(f"{repr(self.SeverGet)}\n")
	# 	except (gaierror, OSError) as e:
	# 		self.SeverGet = None
	# 		output_widget.set_text(f"# {e}")
	#
	# elif command[0] == "run":
	# 	if self.SeverGet is None:
	# 		MgGetSocket.RunThread(self)
	# 	else:
	# 		output_widget.set_text(f"Сервер уже запущен")

	def PrintInfo(self, text: str):
		self.console_columns.PrintInfo(text)

	def UpdateTitle(self, l_text: List[str]):
		self.console_columns.UpdateTitle(l_text)

	def SendTextInIndex(self, index: int, data: str):
		self.console_columns.SendTextInIndex(index, data)


if __name__ == '__main__':
	...
