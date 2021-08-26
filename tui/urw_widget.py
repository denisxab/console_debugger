__all__ = [
	"ConsolesColumns",
	"ConsoleFrame",
	"EditLine",
	"EditListBox",
	"MenuConsole",
]

from typing import List, Callable

import urwid


class ConsolesColumns(urwid.Columns):
	"""
	Колоны с консолями
	"""

	def __init__(self, title_names: List[str], root_: object, focus_column=0, ):
		self.root = root_

		ConsoleFrame.new_max_column(len(title_names))
		widget_list = [ConsoleFrame(name, ) for name in title_names]
		self.__index_column = [focus_column, len(title_names) - 1]  # Для цикличного перемежения
		super().__init__(widget_list, dividechars=0, focus_column=focus_column, min_width=1,
		                 box_columns=None)

	# self.keypress(1,1)

	def UpdateTitle(self, title_names: List[str]):
		"""
		Создать новые консоли
		"""
		for _ in range(self.__index_column[1] + 1):
			self.__del_widget_in_index(0)

		ConsoleFrame.new_max_column(len(title_names))

		for name in title_names:
			self.__append_widget(name)

		self.set_focus(0)
		self.__index_column[0] = 0
		self.__index_column[1] = len(title_names) - 1

	def update_widget(self):
		self.get_focus()

	def SendTextInIndex(self, index_: int, text_: str):
		"""
		Вставить текст в текстовое поле по его индексу:
		"""
		self.contents[index_][0].body_txt.txt.set_edit_pos(0)
		self.contents[index_][0].body_txt.txt.insert_text(text_)
		self.contents[index_][0].body_txt.txt.set_edit_pos(0)

	def PrintInfo(self, text: str):
		self.SendTextInIndex(0, text)

	def keypress(self, size, key):
		"""Горячие клавиши:
- `f1` = Влево
- `f3` = Верх
- `f2` = Вниз
- `f4` = Вправо
- `Tab`= Вправо
- `shif + ЛКМ` = Выделить текст
- `shif + ctrl + C` = Копировать выделенный текст
- `shif + ctrl + V` = Вставить текст"""

		"""
		Обработка перемещений между окнами
		"""
		if key == 'tab':
			self.set_focus(self.__next_focus())
		elif key == 'f1':
			self.set_focus(self.__last_focus())
		elif key == 'f3':
			self.contents[self.focus_col][0].set_focus("body")
		elif key == 'f2':
			self.contents[self.focus_col][0].set_focus("footer")
		elif key == 'f4':
			self.set_focus(self.__next_focus())
		elif key == "f5":
			self.root.loop.widget = self.root.gInfoOverlay

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


class ConsoleFrame(urwid.Frame):
	"""
	Объект консоль
		- Заголовок
		- Многострочное текстовое поле
		- Однострочное текстовое поле
	"""

	__max_column: List[int] = [0, 0]

	def __init__(self, title: str, ):

		Ltop_top, Ltop_bot, Rtop_top, Rtop_bot, \
		bod_line, \
		Lbot_top, Lbot_bot, Rbot_top, Rbot_bot, = self.__get_char_table()

		header = urwid.LineBox(urwid.Text(title, align="center"),
		                       tlcorner=Ltop_top,
		                       blcorner=Ltop_bot,
		                       rline=bod_line,
		                       trcorner=Rtop_top,
		                       brcorner=Rtop_bot,
		                       )

		self.body_txt = EditListBox()

		body = urwid.LineBox(self.body_txt,
		                     bline='',
		                     tline='',
		                     rline=bod_line,
		                     )

		footer = urwid.LineBox(EditLine(fun_execute_command=self.ExecuteCommand, output_widget=self.body_txt.txt, ),
		                       tlcorner=Lbot_top,
		                       blcorner=Lbot_bot,
		                       rline=bod_line,
		                       trcorner=Rbot_top,
		                       brcorner=Rbot_bot,
		                       )

		super().__init__(body, header, footer, focus_part='body')

	@staticmethod
	def ExecuteCommand(output_widget: object, command: str):
		"""Локальная консоль ввода:
- `clear` = Отчистить консоль
- `save <name> <path>` = сохранить в файл"""

		command = command.split()

		if command[0] == "clear":
			output_widget.set_edit_text('')

		elif len(command) == 3 and command[0] == "save":

			output_widget.set_edit_pos(0)
			try:
				path_ = "{}/{}".format(command[2].replace("\\", "/"), command[1])
				with open(path_, "w", encoding="utf-8")as f:
					f.write(output_widget.get_edit_text())

				output_widget.text_menu.insert_text(f"# Save {command[1]} >> {path_}\n")

			except (FileNotFoundError, FileExistsError, PermissionError) as e:
				output_widget.insert_text(f"# {e}")

			output_widget.set_edit_pos(0)

	@classmethod
	def new_max_column(cls, i: int):
		cls.__max_column[0] = 0
		cls.__max_column[1] = i

	def __get_char_table(self):
		res = "┌", "├", "┐", "┤", \
		      "│", \
		      '├', "└", "┤", "┘",

		if self.__max_column[1] > 1:
			if self.__max_column[0] == 0:
				res = "┌", "├", "─", "─", \
				      " ", \
				      '├', "└", "─", "─",

			elif self.__max_column[0] + 1 == self.__max_column[1]:
				res = "┬", "┼", "┐", "┤", \
				      "│", \
				      '┼', "┴", "┤", "┘",

			else:
				res = "┬", "┼", "─", "─", \
				      " ", \
				      '┼', "┴", "─", "─",

		self.__max_column[0] += 1

		# print(res)
		# input()

		return res


class EditLine(urwid.Edit):
	"""
	Однострочное поле для ввода текста | команд
	"""

	def __init__(self, output_widget: object, fun_execute_command: Callable[[object, str], None], ):
		self.output_widget: object = output_widget
		self.fun_execute_command = fun_execute_command
		super().__init__(caption="", edit_text="", multiline=False, align="left")

	def keypress(self, size, key):
		"""
		Если нажать`Enter`, то выполнится  self.fun_execute_command

		Если нажать `F5`, то выполнится  self.fun_execute_command с парамером для скрытия окна
		"""
		if key == "enter":
			self.fun_execute_command(self.output_widget, self.get_edit_text())
			self.set_edit_text('')
		elif key == "f5":
			self.fun_execute_command(None, "close")

		super(EditLine, self).keypress(size, key)


class EditListBox(urwid.ListBox):
	"""
	Многострочное текстовое поле
	"""
	__index_style = 0

	def __init__(self):
		self.__index_style = 0
		self.txt = urwid.Edit(multiline=True, align="left")
		body = urwid.SimpleFocusListWalker([self.txt])
		super(EditListBox, self).__init__(body)

	def keypress(self, size, key):
		super(EditListBox, self).keypress(size, key)


class MenuConsole(urwid.LineBox):
	"""
	Меню:
		- Консоль
		- Текстовое поле для вывода
	"""

	def __init__(self, fun_execute_command, root_):
		self.output_menu = urwid.Text("", align="left")
		root_.ExecuteCommand(self.output_menu, "help")

		self.text_menu = EditLine(output_widget=self.output_menu, fun_execute_command=fun_execute_command, )

		line_menu = urwid.Divider("-")
		body = urwid.SimpleFocusListWalker([self.text_menu, line_menu, self.output_menu])
		self.list_box_menu = urwid.ListBox(body)
		super().__init__(self.list_box_menu, title="",
		                 title_align="center",
		                 title_attr=None,
		                 tlcorner=u'┌',
		                 tline=u'─',
		                 lline=u'│',
		                 trcorner=u'┐',
		                 blcorner=u'└',
		                 rline=u'│',
		                 bline=u'─',
		                 brcorner=u'┘')
