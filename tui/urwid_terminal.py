__all__ = ["run", ]

import asyncio
from pickle import UnpicklingError
from typing import List, Optional

import urwid
from __init__ import *

from date_obj import DataForSocket, DataFlag, InitTitleNameFlag, EndSend
from logic.mg_get_socket import _MgGetSocket

palette = [
	('label_text1', 'black', 'dark cyan',),
	('label_text2', 'black', 'light cyan',),
	('button1', 'black', 'dark cyan',),
	('button2', 'black', 'light cyan',),
]


class ConsoleFrame(urwid.Frame):
	"""
	Объект консоль
		- Заголовок
		- Многострочное текстовое поле
		- Однострочное текстовое поле
	"""
	__index_style = 0

	def __init__(self, title: str):
		header = urwid.Text((self.__next__style(), title), align="center")
		body = ConversationListBox()

		atr = urwid.LineBox(EditLine(edit_text="clear", root_=self))
		footer = atr
		super().__init__(body, header, footer, focus_part='body')

	@classmethod
	def __next__style(cls) -> str:
		if cls.__index_style == 0:
			cls.__index_style = 1
			return "button1"
		else:
			cls.__index_style = 0
			return "button2"

	def ExecuteCommand(self, command: str):

		"""
		Обработчик ввода

		- clear = Отчистить консоль

		- save <name> <path> = сохранить в файл
			- `name` имя файла
			- `path` путь к папке

			save test.txt D:\
		"""

		command = command.split()

		if command[0] == "clear":
			self.body.txt.set_edit_text('')

		elif len(command) == 3 and command[0] == "save":
			self.body.txt.set_edit_pos(0)
			try:
				path_ = "{}/{}".format(command[2].replace("\\", "/"), command[1])
				with open(path_, "w", encoding="utf-8")as f:
					f.write(self.body.txt.get_edit_text())
				self.body.txt.set_edit_text(f"# Save {command[1]} >> {path_}")
			except (FileNotFoundError, FileExistsError, PermissionError) as e:
				self.body.txt.set_edit_text(f"# {e}")
			self.body.txt.set_edit_pos(0)


class EditLine(urwid.Edit):
	"""
	Однострочное поле для ввода текста | команд
	"""

	def __init__(self, caption="", edit_text="", align="left", root_=Optional[ConsoleFrame]):
		self.root = root_
		super().__init__(caption, edit_text, multiline=False, align=align)

	def keypress(self, size, key):
		if key == "enter":
			self.root.ExecuteCommand(self.get_edit_text())
			self.set_edit_text('')
		super(EditLine, self).keypress(size, key)


class ConversationListBox(urwid.ListBox):
	"""
	Многострочное текстовое поле
	"""
	__index_style = 0

	def __init__(self):
		self.__index_style = 0
		self.txt = urwid.Edit(multiline=True, align="left")
		at = urwid.AttrMap(self.txt, self.__next__style())
		body = urwid.SimpleFocusListWalker([at])
		super(ConversationListBox, self).__init__(body)

	def keypress(self, size, key):
		super(ConversationListBox, self).keypress(size, key)

	@classmethod
	def __next__style(cls) -> str:
		if cls.__index_style == 0:
			cls.__index_style = 1
			return "label_text1"
		else:
			cls.__index_style = 0
			return "label_text2"


class ConsolesColumns(urwid.Columns):
	"""
	Колоны с консолями
	"""

	def __init__(self, title_names: List[str], dividechars=0, focus_column=0, min_width=1, box_columns=None):
		widget_list = [ConsoleFrame(name) for name in title_names]
		self.__index_column = [focus_column, len(title_names) - 1]  # Для цикличного перемежения
		super().__init__(widget_list, dividechars, focus_column, min_width, box_columns)

	# self.keypress(1,1)

	def CreateNewTitleName(self, title_name: List[str]):
		"""
		Создать новые консоли
		"""
		for _ in range(self.__index_column[1] + 1):
			self.__del_widget_in_index(0)

		for name in title_name:
			self.__append_widget(name)

		self.set_focus(0)
		self.__index_column[0] = 0
		self.__index_column[1] = len(title_name) - 1

	def SendTextInIndex(self, index_: int, text_: str):
		"""
		Вставить текст в текстовое поле по его индексу:
		"""
		self.contents[index_][0].body.txt.set_edit_pos(0)
		self.contents[index_][0].body.txt.insert_text(text_)
		self.contents[index_][0].body.txt.set_edit_pos(0)

	def SendSelfInfo(self, text: str):
		self.SendTextInIndex(0, text)

	def keypress(self, size, key):

		"""
		Обработка перемещений между окнами
		"""
		if key == 'tab':
			self.set_focus(self.__next_focus())

		elif key == 'ctrl up':
			self.contents[self.focus_col][0].set_focus("body")

		elif key == 'ctrl down':
			self.contents[self.focus_col][0].set_focus("footer")

		elif key == 'ctrl left':
			self.set_focus(self.__last_focus())

		elif key == 'ctrl right':
			self.set_focus(self.__next_focus())

		"""
		Если в фокусе текстовое поле для команд то перенаправляет вывод клавиш в него
		"""
		if self.contents[self.focus_col][0].get_focus() == "footer":
			if key not in ("down", "up"):
				return self.contents[self.focus_col][0].footer.base_widget.keypress([size, ], key)
		else:
			"""		
			Отправляем кнопки в обработчики текстового поля
			"""
			return self.contents[self.focus_col][0].body.keypress(size, key)

	def __del_widget_in_index(self, index):
		self.contents.pop(index)

	def __append_widget(self, title):
		self.contents.append([ConsoleFrame(title), self.options()])

	def __next_focus(self):
		if self.__index_column[0] < self.__index_column[1]:
			self.__index_column[0] += 1
		else:
			self.__index_column[0] = 0
		return self.__index_column[0]

	def __last_focus(self):
		if self.__index_column[0] > 0:
			self.__index_column[0] -= 1
		else:
			self.__index_column[0] = self.__index_column[1]
		return self.__index_column[0]


async def CheckUpdateServer(clm: ConsolesColumns):
	"""
	Асинхронная функция по получению данных из сокета
	"""

	SeverTk = _MgGetSocket()
	clm.SendSelfInfo("# Run Server")
	SeverTk.ConnectToClient()  # Ждем подключение клиента

	clm.SendSelfInfo(f"# {SeverTk.Host}:{SeverTk.Port}\n")
	title_name: List[str] = []

	while True:
		if SeverTk.user:
			if SeverTk.user.fileno() != -1:  # Если сервер не отсоединился от клиента
				try:
					flag, id_, data_l = DataForSocket.GetDataObj(SeverTk.user)

					if flag == DataFlag:
						clm.SendTextInIndex(id_, data_l[0])
						await asyncio.sleep(0)

					elif flag == InitTitleNameFlag:
						if title_name != data_l:
							title_name = data_l
							clm.CreateNewTitleName(data_l)
							await asyncio.sleep(0)

					elif flag == EndSend:
						SeverTk.UserClose()

				except ConnectionResetError:  # Если клиент разорвал соединение
					SeverTk.UserClose()  # Закрыть соединение с клиентом
					clm.SendSelfInfo("Клиент разорвал соединение")

				except (UnpicklingError, EOFError):  # Не получилось распаковать данные
					clm.SendSelfInfo("Ошибка распаковки")

				except ConnectionAbortedError:  # Если клиенту невозможно отправить данные от отключаемся
					SeverTk.UserClose()  # Закрыть соединение с клиентом
					clm.SendSelfInfo("Если клиенту невозможно отправить данные")
			else:  # Если сервер отсоединился от клиента, то ждать следующего подключение
				SeverTk.UserClose()

		await asyncio.sleep(0)


def run():
	urwid.set_encoding('utf8')
	alsop = asyncio.get_event_loop()
	cl = ConsolesColumns(["1", "2"])
	loop = urwid.MainLoop(cl, palette=palette, event_loop=urwid.AsyncioEventLoop(loop=alsop))
	alsop.create_task(CheckUpdateServer(cl))
	try:
		loop.run()
	except KeyboardInterrupt:
		print("Exit")
		exit()


if __name__ == '__main__':
	print(path)
	...
