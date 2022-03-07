from os.path import dirname
from typing import List


def add_sys_path_if_not(add_path: str, sys_path: List[str]):
	"""
	Добавить путь если его нет
	:param add_path:
	:param sys_path:
	:return:
	"""
	if add_path not in sys_path:
		sys_path.append(add_path)


def root_path(slice_end: int = 0, add_path: str = ""):
	"""
	Внимание!!! Путь отображается от места где находится сам файл `path_helper.py`

	Обрезает относительный путь, и может добавлять к нему другой путь:
	:param slice_end: Срез с конца
	:param add_path: Добавить путь
	:return:
	"""
	p = dirname(__file__).replace("\\", "/").split("/")
	if slice_end:
		p = p[:slice_end]
	if add_path:
		p.append(add_path.replace("\\", "/"))
	return "/".join(p)
