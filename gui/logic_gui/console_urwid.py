__all__ = ["run", ]

import asyncio
import sys
from collections import deque
from os.path import dirname
from pickle import UnpicklingError
from typing import List

import urwid

dirs = dirname(__file__).replace("\\", "/").split("/")[:-2]
sys.path.append("/".join(dirs))

from date_obj import DataForSocket, DataFlag, InitTitleNameFlag, EndSend
from gui.logic_gui.mg_get_socket import _MgGetSocket

palette = [
	('label_text1', 'black', 'dark cyan',),
	('label_text2', 'black', 'light cyan',),
	('button1', 'black', 'dark cyan',),
	('button2', 'black', 'light cyan',),
]


class BoxButton(urwid.WidgetWrap):
	def __init__(self, label, on_click):
		label_widget = urwid.Text(label, align='center')
		self.widget = urwid.LineBox(label_widget)
		self.hidden_button = urwid.Button('hidden button', on_click)

		super(BoxButton, self).__init__(self.widget)

	def selectable(self):
		return True

	def keypress(self, *args, **kwargs):
		return self.hidden_button.keypress(*args, **kwargs)

	def mouse_event(self, *args, **kwargs):
		return self.hidden_button.mouse_event(*args, **kwargs)


class ConsoleFrame(urwid.Frame):
	__index_style = 0

	def __init__(self, title_button: str, title_footer: str, focus_part='body'):
		self.button = BoxButton(title_button, self.ExecuteButton)
		header = urwid.AttrMap(self.button, self.__next__style(), "highlight")
		body = ConversationListBox()
		footer = urwid.Text(title_footer)
		super().__init__(body, header, footer, focus_part)

	@staticmethod
	def ExecuteButton(button):
		...

	@classmethod
	def __next__style(cls) -> str:
		if cls.__index_style == 0:
			cls.__index_style = 1
			return "button1"
		else:
			cls.__index_style = 0
			return "button2"


class ConversationListBox(urwid.ListBox):
	__index_style = 0

	def __init__(self):
		self.__index_style = 0
		self.txt = urwid.Edit(multiline=True, align="left")
		at = urwid.AttrMap(self.txt, self.__next__style())
		body = urwid.SimpleFocusListWalker([at])

		urwid.Pile([urwid.Edit(('I say', u"What is your name?\n"))])

		super(ConversationListBox, self).__init__(body)

	def keypress(self, size, key):
		key = super(ConversationListBox, self).keypress(size, key)

	@classmethod
	def __next__style(cls) -> str:
		if cls.__index_style == 0:
			cls.__index_style = 1
			return "label_text1"
		else:
			cls.__index_style = 0
			return "label_text2"


class Consoles(urwid.Columns):
	def __init__(self, title_names: List[str], dividechars=0, focus_column=0, min_width=1, box_columns=None):
		widget_list = [ConsoleFrame(name, name) for name in title_names]
		self.__index_column = [focus_column, len(title_names) - 1]  # Для цикличного перемежения
		super().__init__(widget_list, dividechars, focus_column, min_width, box_columns)

	# self.keypress(1,1)

	def keypress(self, size, key):
		"""
		Обработка перемещений между окнами
		"""
		if key == 'tab':
			self.set_focus(self.__next_focus())

		elif key == 'ctrl up':
			self.contents[self.focus_col][0].set_focus("header")

		elif key == 'ctrl down':
			self.contents[self.focus_col][0].set_focus("body")

		elif key == 'ctrl left':
			self.set_focus(self.__last_focus())

		elif key == 'ctrl right':
			self.set_focus(self.__next_focus())

		"""
		Если выбрана кнопка и пользователь нажимает `Enter` то представляем что он сделал нажатие на кнопку
		"""
		if key == "enter" and self.contents[self.focus_col][0].get_focus() == "header":
			self.contents[self.focus_col][0].ExecuteButton(self.contents[self.focus_col][0].button.hidden_button)
			return None

		"""
		Отправляем остальные кнопки в обработчики текстового поля
		"""
		return self.contents[self.focus_col][0].body.keypress(size, key)

	def CreateNewTitleName(self, title_name: List[str]):

		for _ in range(self.__index_column[1] + 1):
			self.__del_widget_in_index(0)

		for name in title_name:
			self.__append_widget(name, name)

		print(len(title_name))
		self.set_focus(0)
		self.__index_column[0] = 0
		self.__index_column[1] = len(title_name) - 1

	def SetTextInIndex(self, index_: int, text_: str):
		"""
		Вставить текст в текстовое поле по его индексу:
		"""

		self.contents[index_][0].body.txt.set_edit_pos(0)
		self.contents[index_][0].body.txt.insert_text(text_)
		self.contents[index_][0].body.txt.set_edit_pos(0)

	def __del_widget_in_index(self, index):
		self.contents.pop(index)

	def __append_widget(self, title_button: str, title_footer: str):
		self.contents.append([ConsoleFrame(title_button, title_footer), self.options()])

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


async def generate_output(clm: Consoles):
	SeverTk = _MgGetSocket()
	# print(SeverTk.Port, " Ran SeverMg")
	SeverTk.ConnectToClient()  # Ждем подключение клиента
	title_name = ""

	while True:

		if SeverTk.user:

			fragment = deque()

			if SeverTk.user.fileno() != -1:  # Если сервер не отсоединился от клиента
				try:

					flag, id_, data_l = DataForSocket.GetDataObj(SeverTk.user)

					# print(f"{self.SeverTk.Port}:{self.SeverTk.user.fileno()} ", id_, data_l[0])

					if flag == DataFlag:
						###
						clm.SetTextInIndex(id_, data_l[0])
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
				# print('{} {} {}'.format("*" * 40,
				#                         "Клиент разорвал соединение",
				#                         "*" * 40,
				#                         ))

				except (UnpicklingError, EOFError):
					...
				# user.close()  # Закрыть соединение с клиентом
				# print(fragment)
				# print('{} {} {}'.format("$" * 40,
				#                         "Ошибка распаковки",
				#                         "$" * 40,
				#                         ))

				except ConnectionAbortedError:  # Если клиенту невозможно отправить данные от отключаемся
					SeverTk.UserClose()  # Закрыть соединение с клиентом
			# print('{} {} {}'.format("$" * 40,
			#                         "Если клиенту невозможно отправить данные",
			#                         "$" * 40,
			#                         ))

			else:  # Если сервер отсоединился от клиента, то  ждать следующего подключение
				SeverTk.UserClose()

		await asyncio.sleep(0)


def run(init_title_name: List[str]):
	aloop = asyncio.get_event_loop()
	ev_loop = urwid.AsyncioEventLoop(loop=aloop)

	cl = Consoles(init_title_name)

	loop = urwid.MainLoop(cl, palette=palette, event_loop=ev_loop)

	aloop.create_task(generate_output(cl))

	loop.run()


if __name__ == '__main__':
	...
