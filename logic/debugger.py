__all__ = [

	"Debugger",
	"style_t",

]

from datetime import datetime
from inspect import currentframe
from os.path import abspath, dirname
from pprint import pformat
from sys import stdout
from typing import TextIO, Tuple, Optional, Dict, List, Union, Any

from helpful.coloring_text import style_t, StyleText
from helpful.date_obj import ServerError
from helpful.template_obj import dstyle
from logic.mg_send_socket import MgSendSocket


class Debugger:
	# Все экземпляры дебагеров
	_all_instance: Dict[str, object] = {}
	# Настройки для таблицы
	_global_len_rows: List[Tuple[str, int]] = []
	_global_row_board: str = ""
	# Экземпляр сокета
	_socket_obj: Optional[MgSendSocket] = None

	def write(self, __s: str) -> Any:
		"""
		Для работы с функцией print
		print("TEXT",file=a)
		"""
		if __s not in ("\n", "", " "):
			self.__call__(__s)

	def __init__(self,
	             active: bool,
	             title_name: str,
	             *,
	             fileConfig: Optional[Dict] = None,
	             style_text: Optional[dstyle] = None,
	             consoleOutput: bool = True,
	             ):
		"""
		public set:
			+ consoleOutput = Вывод в консоль
			+ style_text = Стиль отображения

		public get:
			+ title_name = Уникальное имя дебагера
			+ fileConfig = Конфигурация для файла
			+ AllInstance = Все экземпляры дебагеров
			+ AllActiveInstance() = Все активные дебагеры
			+ AllSleepInstance() = Все приостановленный дебагиры
			+ AllUseFileName() = Все используемые имена файлов
		"""

		# title_name
		self.__title_name: str = title_name

		# active
		self.__active: bool = active
		if self.__active and self.__title_name in Debugger.AllActiveInstance():
			raise NameError("A instance of a class can only have to unique title_name")

		# fileConfig
		self.__fileConfig: Optional[Dict] = fileConfig
		if fileConfig:
			self.__addFileName_in_AllUseFileName(self.__fileConfig["file"])

		# consoleOutput
		self.consoleOutput: Optional[TextIO] = stdout if consoleOutput else None

		# style_text
		self.style_text: dstyle = dstyle(len_word=len(self.__title_name)) if not style_text else style_text

		# id
		Debugger._all_instance[title_name] = self  # Это строчка должны быть выше назначения self.__id !
		self.__id = len(Debugger.AllActiveInstance()) - 1

	def __call__(self, textOutput: Union[str, StyleText], *args, sep=' ', end='\n'):
		"""
		Здесь все логика отправки данных, как вы файл, так и на экран
		"""
		if self.__active:
			if self.__fileConfig:
				with open(**self.__fileConfig) as f:
					# Сохранять в файл не стилизованный текст
					print(
						f"|{self.__title_name}|{textOutput}|",
						*args,
						sep=sep, end=end, file=f)

			if self.consoleOutput:
				# Вывод в виде Таблицы
				if Debugger._global_len_rows:
					print(self.__designerTable(style_t(textOutput.replace("\t", ""),
					                                   **self.style_text)), end='')

				#
				elif Debugger._socket_obj:
					"""
					Если сокет закрыт, то перенаправляем вывод в стандартную консоль
					"""

					"""
					# Трассировка переемных 
					1. Отображать имя переменной, если у нее есть внешняя ссылка.
					2. Если одному и тому же значению присвоено несколько переменных, 
					вы будете получить оба этих имени переменных
					"""
					callers_local_vars = currentframe().f_back.f_back.f_locals.items()
					names_var: list = [var_name for var_name, var_val in callers_local_vars if
					                   var_val is textOutput]
					names_var_str: str = f"({', '.join(names_var)})¦" if names_var else "¦"

					"""
					Чтобы данные не копировались каждый раз при передачи в функцию, делаем ссылку на текст
					"""
					res: List[str] = ["{next_steep}\n{data}{name_var}\n{textOutput}\n".format(
						next_steep=f"{'-' * (len(names_var_str) + 7)}¬",
						data=datetime.now().strftime('%H:%M:%S'),
						name_var=names_var_str,
						textOutput=f"{str(textOutput)} {' '.join(str(item) for item in args)}",
					)]

					Debugger._socket_obj.PickleDataAndSendToServer(self.__id, res)

				# Без стилей
				else:
					print(
						"|{}|\t{}".format(self.__title_name,
						                  style_t(f"{textOutput} {' '.join(str(item) for item in args)}",
						                          **self.style_text)),
						*args,
						sep=sep, end=end)

	@classmethod
	def GlobalManager(cls, *, global_status: Optional[bool] = None, typePrint: Optional[str] = "grid"):
		"""
		Глобальная настройка всех экземпляров
		:param: typePrint: Отвечает за стиль вывода данных на экран
		:param: global_active: Можно on/off все экземпляры разом
		"""

		# Логика on/off всех экземпляров
		if global_status is not None:
			if global_status:
				for k, v in cls._all_instance.items():
					v.__active = True
				return None

			if not global_status:
				for k, v in cls._all_instance.items():
					v.__active = False
				return None

		# Обрабатываем логику стилей вывода, только когда global_active == None|True
		elif global_status is None or global_status:

			if typePrint == "grid":  # Отображать таблицу в консоли
				rowBoard: str = ""
				rowWord: str = ""
				arr: List[str] = []
				for k, v in cls._all_instance.items():
					if v.__active:
						v1 = v.style_text.copy()
						v1['agl'] = 'center'  # что бы центрировать только заголовки, а не весь текст
						text = style_t(k, **v1).present_text
						rowBoard += f"+{'-' * len(text)}"
						rowWord += f"|{text}"
						arr.append(text)
						cls._global_len_rows.append((k, len(text)))

				rowWord += "|"
				rowBoard += "+"
				row: str = f"{rowBoard}\n{rowWord}\n{rowBoard.replace('-', '=')}"
				cls._global_row_board = rowBoard
				print(row)
				return None
			else:
				cls._global_len_rows.clear()
				cls._global_row_board = ""

			if typePrint == "socket":  # Запускам менеджер сокета

				cls._socket_obj = MgSendSocket()

				if not cls._socket_obj.ConnectToServer(cls.AllActiveInstance()):
					cls._socket_obj = None
					dirs = dirname(__file__).replace("\\", "/").split("/")[:-1]
					dirs.append("main.py tui")
					raise ServerError(
						'Вероятно сервер не запущен\n{0}\nВыполните команду:\n\npython {1}\n\n{0}\n'.format("*" * 80,
						                                                                                    "/".join(
							                                                                                    dirs)
						                                                                                    ))
				return None

			else:
				cls._socket_obj = None

	# --- Other method --- #

	def active(self):
		"""
		Активировать экземпляр
		"""
		self.__active = True

	def deactivate(self):
		"""
		Деактивировать экземпляр
		"""
		self.__active = False

	def __designerTable(self, textOutput: StyleText) -> str:
		"""
		Метод для создания таблицы
		"""
		"""
		Dependencies:
			- Debugger.GlobalLenRows:
			- self.style_text: Нужно знать размеры ячейки
			- self._title: Нужно знать заголовок для идентификации
		"""
		res_print: str = ""
		for height_item in textOutput.present_text.split('\n'):
			height_item = style_t(height_item, **self.style_text).style_text
			for item in Debugger._global_len_rows:
				if item[0] == self.__title_name:
					res_print += f"|{height_item}"
				else:
					res_print += f"|{' ' * item[1]}"
			res_print += '|\n'
		res_print += f"{Debugger._global_row_board}\n"
		return res_print

	def __addFileName_in_AllUseFileName(self, file_name: str):
		"""
		Проверяет имя файла со всеми используемыми именами файлов
		Это необходимо для защиты от случайного параллельного доступа к файлам
		"""
		absFileName = abspath(file_name).replace("\\", "/")
		if not self.AllUseFileName().get(absFileName, False):
			self.__fileConfig["file"] = absFileName
		else:
			raise FileExistsError("A single instance of a class can write to only one file")

	# --- Attribute ---#

	@staticmethod
	def AllActiveInstance() -> List[str]:
		"""
		# Имена активных дебагеров
		"""
		return [v.title_name for v in Debugger._all_instance.values()
		        if v.is_active]

	@staticmethod
	def AllSleepInstance() -> List[str]:
		"""
		# Имена остановленных дебагеров
		"""
		return [v.title_name for v in Debugger._all_instance.values()
		        if not v.is_active]

	@staticmethod
	def AllUseFileName() -> dict:
		"""
		# Используемые файлы для записи
		"""
		return {v.fileConfig["file"]: v.title_name for v in
		        Debugger._all_instance.values()
		        if v.fileConfig}

	@property
	def AllInstance(self) -> Dict[str, object]:
		"""
		Получить копию всех экземпляр дебагера
		"""
		return Debugger._all_instance.copy()

	@property
	def fileConfig(self) -> Optional[Dict]:
		"""
		Получить конфигурацию файла
		"""
		return self.__fileConfig

	@property
	def title_name(self) -> str:
		"""
		Получить уникальное имя экземпляра
		"""
		return self.__title_name

	@property
	def is_active(self) -> bool:
		"""
		Проверить активный ли экземпляр
		"""
		return self.__active

	# --- Info --- #
	def __repr__(self) -> str:
		res = {"AllActiveInstance": Debugger.AllActiveInstance(),
		       "AllUseFileName": Debugger.AllUseFileName(),
		       "AllCountSleepInstance": Debugger.AllSleepInstance()}
		res.update(self.__dict__)
		return pformat(res, indent=1, width=30, depth=2)

	def __str__(self) -> str:
		return self.__title_name


if __name__ == '__main__':
	...
