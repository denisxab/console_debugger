__all__ = ["ViewGui"]

from os.path import dirname
from tkinter import Tk, Frame, Button, Text, Entry, messagebox, PhotoImage
from typing import List, Optional

# from __init__ import *
from console_debugger.helpful.template_obj import ViewRoot
from console_debugger.logic.mg_get_socket import MgGetSocket

i = 0


class ViewGui(ViewRoot):
	GREEN = "#487861"
	BG_COLOR = "#171b22"
	BLOCK_COLOR = "#0e1117"
	TEXT_COLOR = "#cad0d9"
	SIZE_TEXT_CONSOLE = 7

	SeverGu: Optional[MgGetSocket] = None

	def __init__(self):

		self.windowTk = Tk()
		self.windowTk.title("debugger_tk")

		img = PhotoImage("{path_}/static/icons.ico".format(
			path_="/".join(dirname(__file__).replace("\\", "/").split("/")[:-1])
		))

		# self.windowTk.iconbitmap(img)
		self.windowTk.tk.call('wm', 'iconphoto', self.windowTk._w, img)
		self.windowTk.attributes("-topmost", True)
		self.windowTk.geometry(self.__get_geometer())

		self.frameConsole: Optional[Frame] = None
		self.bt1: Optional[Button] = None
		self.Arr_textWidget: List[Text] = []
		self.__construct_widget(["1", "2"])

		self.windowTk.protocol("WM_DELETE_WINDOW", self.__del)

		super().__init__()
		MgGetSocket.RunThread(self)

		self.windowTk.mainloop()

	def PrintInfo(self, text: str):
		print(text)

	def UpdateTitle(self, l_text: List[str]):
		self.__deconstruct_widget()
		self.__construct_widget(l_text)

	def SendTextInIndex(self, index: int, data: str):
		self.Arr_textWidget[index].insert("0.1", data)

	def __construct_widget(self, names_console: Optional[List[str]]):
		"""
		Создаем и размещаем виджеты
		"""

		self.frameConsole = Frame(self.windowTk,
		                          width=100,
		                          height=200)

		self.bt1 = Button(self.windowTk,
		                  text="save geometry",
		                  bg=ViewGui.GREEN,
		                  command=lambda: self.__set_geometer()
		                  )
		self.bt1.pack(fill="x")

		self.Arr_textWidget = self._form_horizon_console(names_console, self.frameConsole)

	def __deconstruct_widget(self):
		"""
		Удаляем виджеты
		"""
		self.bt1.destroy()
		self.frameConsole.destroy()

	@staticmethod
	def display_info(message: str):
		"""
		Всплывающее окно
		"""
		messagebox.showinfo("Command", message)

	def __get_geometer(self) -> str:
		"""
		Получить размер окна сохраненный в файле
		"""
		try:
			with open(f"{dirname(__file__)}/static/config.txt", "r")as f:
				return f.read()

		except FileNotFoundError:
			return "{X}x{Y}+{W}+{H}".format(
				X=600,
				Y=600,
				W=self.windowTk.winfo_screenwidth() // 2 - 160,
				H=self.windowTk.winfo_screenheight() // 2 - 160,
			)

	def __set_geometer(self):
		"""
		Записать положение и размер окна в файл
		"""
		with open(f"{dirname(__file__)}/static/config.txt", "w")as f:
			x = self.windowTk.winfo_x()
			y = self.windowTk.winfo_y()
			w = self.windowTk.winfo_width()
			h = self.windowTk.winfo_height()
			f.write(f"{w}x{h}+{x}+{y}")

	def ExecuteCommand(self, event, index_console: int, EntryInput_obj: Entry):
		"""
		Обработчик ввода

		- clear = Отчистить консоль

		- save <name> <path> = сохранить в файл
			- `name` имя файла
			- `path` путь к папке

			save test.txt D:\

		- g info = Показать глобальные настройки
		"""

		command = EntryInput_obj.get().split()

		if command[0] == "clear":
			self.Arr_textWidget[index_console].delete(1.0, "end")
			EntryInput_obj.delete(0, "end")

		elif len(command) == 3 and command[0] == "save":
			try:
				path_ = "{}/{}".format(command[2].replace("\\", "/"), command[1])
				with open(path_, "w", encoding="utf-8")as f:
					f.write(self.Arr_textWidget[index_console].get(1.0, "end"))

				ViewGui.display_info(f"{index_console} >> {path_}")
			except (FileNotFoundError, FileExistsError, PermissionError) as e:
				ViewGui.display_info(f"{e}")

			EntryInput_obj.delete(0, "end")

		elif command[0] == 'g' and command[1] == "info":
			ViewGui.display_info(f"{repr(self.SeverGet)}\n-----\nLen all debugger:\n {len(self.Arr_textWidget)}")
			EntryInput_obj.delete(0, "end")

		# elif command[0] == 'g' and command[1] == "run" and self.SeverGet == None:
		# 	self.__run_Thread()
		# 	EntryInput_obj.delete(0, "end")

	def _form_horizon_console(self, names_console: List[str],
	                          frameConsoles: Frame,
	                          ) -> List[Text]:
		"""
		Формирует горизонтально консоли и отображает её

		:type frameConsole: self.frameConsole = Frame(self.windowTk, width=100, height=200)
		:param count_console: Количество созданных консолей
		:return: список с экземплярами консолей
		"""
		ptr_arr_textWidget: List[Text] = []
		index: int = 0
		count_console: int = len(names_console)
		# нумерация строк здесь начинается с единицы, а нумерация столбцов – с нуля.

		for index_console, item in enumerate(names_console):
			Cons = Frame(frameConsoles)
			EntryInput = Entry(Cons,
			                   font=('consolas', f'{ViewGui.SIZE_TEXT_CONSOLE}'),
			                   bg=ViewGui.BLOCK_COLOR, fg=ViewGui.TEXT_COLOR,
			                   insertbackground=ViewGui.TEXT_COLOR, )
			###############
			ButtonExecute: Button = Button(Cons,
			                               text=item,
			                               bg=ViewGui.BLOCK_COLOR,
			                               fg=ViewGui.TEXT_COLOR,
			                               height=1,
			                               font=('consolas', f'{ViewGui.SIZE_TEXT_CONSOLE}'),
			                               command=lambda i=index_console, e=EntryInput: self.ExecuteCommand(None, i,
			                                                                                                 e))
			###############
			txt: Text = Text(Cons,
			                 width=80,  # Количество символов по вертикали
			                 height=20,  # Количество символов по горизонтали
			                 bg=ViewGui.BG_COLOR,
			                 fg=ViewGui.TEXT_COLOR,
			                 font=('consolas', f'{ViewGui.SIZE_TEXT_CONSOLE}'),
			                 insertbackground=ViewGui.TEXT_COLOR,
			                 )
			###############
			EntryInput.bind('<Return>', lambda v, i=index_console, e=EntryInput: self.ExecuteCommand(None, i, e))
			EntryInput.insert(0, "clear")
			###############

			ButtonExecute.pack(fill="both", )
			txt.pack(expand=True, fill="both", )
			EntryInput.pack(fill="both", )

			Cons.place(relheight=1,
			           relx=index,
			           relwidth=(1 / count_console),
			           )

			index += 1 / count_console
			ptr_arr_textWidget.append(txt)

		###############
		frameConsoles.pack(expand=True, fill="both", )
		return ptr_arr_textWidget

	def __del(self):
		self.windowTk.destroy()


if __name__ == '__main__':
	...
