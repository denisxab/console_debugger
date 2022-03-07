# Что это?

:wrench: :pencil: :desktop_computer: Это библиотека для Python, которая выводит информации в несколько консолей. Путем обмена данных через Unix Socket

Установка через [pip - console-debugger](https://pypi.org/project/console-debugger/)

```bush
pip install console-debugger
```

![](https://i.imgur.com/w1DMqV5.png)

---

# Как использовать ?

## 1 Сначала нужно создать экземпляры класса Debugger

Debugger(`active: bool, titleName: str, consoleOutput: bool = True, fileConfig: Optional[Dict] = None, styleText: Optional[dstyle] = None`)

| Атрибут         | Описание                                                                                                                                                                                                                   |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `active`        | on/off жизни экземпляра, Если `False` экземпляр будет игнорировать вызов, а также будет добавлен в массив `Debugger.AllCountSleepInstance` .                                                                               |
| `titleName`    | Уникальное имя экземпляра которое будет отображаться в выводе.                                                                                                                                                             |
| `consoleOutput` | on/off отображения в консоль или другие визуальные выходы, **Не влияет на запись в файл!** .                                                                                                                               |
| `fileConfig`    | Конфигурация записи в файл, входные параметры такие же как и у стандартной функции `open()` передавать в формате `{"file":"test.log", ... }` . Для удобного формирования параметров можно пользоваться функцией `dopen()`. |
| `styleText`    | Стиль отображения текста. Для удобного формирования параметров можно пользоваться функцией `dstyle`.                                                                                                                       |

---

Также можно использовать готовые параметры

Debugger(`**dDEBUG`)

- `dDEBUG`
- `dINFO`
- `dWARNING`
- `dEXCEPTION`

---

Доступная информации об экземпляре `Debugger`

| public set      | Описание                           |
| --------------- | ---------------------------------- |
| `consoleOutput` | Переключить on/off вывод в консоль |
| `styleText`    | Задать другой стиль текста         |
| `active()`      | Включить дебагер                   |
| `deactivate()`  | Отключить дебагер                  |

| public get                 | Описание                                    |
| -------------------------- | ------------------------------------------- |
| `titleName`               | Уникальное имя дебагера                     |
| `fileConfig`               | Конфигурация для файла                      |
| `AllCountActiveInstance()` | Список со всеми активными экземплярами      |
| `AllCountSleepInstance() ` | Список со всеми остановленными экземплярами |
| `AllUseFileName()`         | Список всех имен используемых файлами       |
| `AllInstance()`            | Список всех экземпляров                     |

## 2 Создать глобальные правила для всех экземпляров

Эта команда влияет на все экземпляры `Debugger`

Debugger.GlobalManager(`global_status=None, typePrint: Optional[str] = "grid"`):

| Атрибут         | Описание                                                                  |
| --------------- | ------------------------------------------------------------------------- |
| `global_status` | Здесь вы можете Выключить/Включить все экземпляры                         |
| `typePrint`     | Глобальный стиль отображения данных  (`grid`/`socket`/`None`)             |

---

- `"grid"` = Стиль таблица
    ![](https://i.imgur.com/Kif40aB.png)
- `"socket"` = Данные будут отправляться по сокету, в данный момент есть два варианта прослушивания сокета.
    Через GUI [Tkinter](#про-режим-отображения-tkinter) `console_debugger/main.py gui` или через TUI [Urwid](#про-режим-отображения-urwid)
    `console_debugger/main.py tui`.
    Если в процессе отправки данных через сокет возникнут ошибки, данные будут сохранены в файл.
- `None` = Без стиля
    ![](https://i.imgur.com/byg84id.png)

---

## 3 Использовать в коде

Использовать стандартную функцию `print`.

print(`text, file= Debug_Name`)

- `text` = Строка
- `Debug_Name` = Имя экземпляра `Debugger`

---

Использовать функцию `printD`. Преимущество в том что может принимать несколько переменных и соеденять их.

printD(`Debug_Name, text, *args, sep=' ', end='\n'`)

- `Debug_Name` = Имя экземпляра `Debugger`
- `text` = Строка
- `*args` = Данные преобразуются в тип `str`
- `sep=' ', end='\n'` = такие же, как и у встроенной функции `print()`

---

# Примеры

## Использовать свои стили оформления

Для наглядности создадим функцию для генерации случайного слово

```python
import random
import string
# Сгенерировать случайное слово
random_word = lambda: "".join(random.choice(string.ascii_letters) for j in range(random.randint(1, 40)))
```

```python
from console_debugger import Debugger, printD
from console_debugger.helpful.template_obj import dopen, dstyle

Debug = Debugger(True,titleName="[DEBUG]",

                 fileConfig=dopen(file="debug.log",
                                  mode="a",
                                  encoding="utf-8"),

                 styleText=dstyle(bg_color="bg_blue",
                                   len_word=21)
                 )
Info = Debugger(True,titleName="[INFO]",

                fileConfig={"file": "info.log",
                            "mode": "a", "encoding": "utf-8"},
                styleText=dstyle(len_word=25),

                consoleOutput=False
                )
Warning = Debugger(True,"[WARNING]", styleText=dstyle(len_word=25))

Debugger.GlobalManager(typePrint="grid")

if __name__ == '__main__':
    for i in range(10):
        printD(Debug, random_word())
        printD(Warning, random_word())
        printD(Info, random_word())
```

## Использовать готовые стили, вызывать `printD`

```python
from console_debugger import Debugger, printD
from console_debugger.helpful.template_obj import dDEBUG, dWARNING, dINFO

Debug = Debugger(**dDEBUG)
Info = Debugger(**dINFO)
Warning = Debugger(**dWARNING)

Debugger.GlobalManager(typePrint="grid")

if __name__ == '__main__':
    for i in range(10):
        printD(Debug, random_word())
        printD(Warning, random_word())
        printD(Info, random_word())
```

## Использовать готовые стили, вызывать `print`

```python
from console_debugger import Debugger, printD
from console_debugger.helpful.template_obj import dDEBUG, dWARNING, dINFO

Debug = Debugger(**dDEBUG)
Info = Debugger(**dINFO)
Warning = Debugger(**dWARNING)

Debugger.GlobalManager(typePrint="socket")

if __name__ == '__main__':
    for i in range(10):
	print(random_word(), file=Debug)
	print(random_word(), file=Info)
	print(random_word(), file=Warning)
```

## Использовать `soket`

```python
from console_debugger import Debugger, printD
from console_debugger.helpful.template_obj import dDEBUG, dWARNING, dINFO

Debug = Debugger(**dDEBUG)
Info = Debugger(**dINFO)
Warning = Debugger(**dWARNING)
TEST = Debugger(True,"TEST")

Debugger.GlobalManager(typePrint="socket")


for i in range(10):
    printD(Debug, random_word())
    printD(Info, random_word())
    printD(Warning, random_word())
    printD(TEST, random_word())
```

Если вы не запустили сервер, у вас возникнет исключение `ServerError: Ошибка сервера`
Это специальное исключения для того чтобы вы лично выбрали интерфейс отображения.
Вы можете выполнить команду `python /.../.../.local/lib/python3.9/site-packages/console_debugger/main.py tui`
в любом терминале Linux, в нем запуститься псевдографический интерфейс.

Или вы можете выполнить команду `python /.../.../.local/lib/python3.9/site-packages/console_debugger/main.pyп gui`
Тогда у вас запуститься графический интерфейс Tkinter.

```
[Errno 2] No such file or directory
ServerError: Ошибка сервера
Traceback (most recent call last):
  File "/home/denis/Applications/test_imp.py", line 17, in <module>
    Debugger.GlobalManager(typePrint="socket")
  File "/.../.../.local/lib/python3.9/site-packages/console_debugger/logic/debugger.py", line 190, in GlobalManager
    raise ServerError(
helpful.date_obj.ServerError: Вероятно сервер не запущен
********************************************************************************
Выполните команду:

python /.../.../.local/lib/python3.9/site-packages/console_debugger/main.py tui

********************************************************************************
```

## Использование Глобального режима on/off

Создать два режима запуска Debug/Release
![](https://i.imgur.com/guFWf3O.png)

`main.pyw`

```python
import sys
from console_debugger import Debugger
from app.viwe import Windows # При импорте должны быть созданы все экземпляры

if __name__ == '__main__':
    for param in set(sys.argv):
        if param == "--d":
            Debugger.GlobalManager(typePrint="grid") # Задать глобальный стиль всем экземпляром
            break
    else:
        Debugger.GlobalManager(global_status=False) # Если нет параметров отключаем все экземпляры
    Windows()
```

В других модулях создаем необходимые экземпляры

```python
from console_debugger import Debugger, printD
from console_debugger.helpful.template_obj import dstyle, dINFO

HotKeyD = Debugger(True, "[HotKey]")
PressKeyD = Debugger(True, "[PressKey]")
InfoD = Debugger(**dINFO)
ResD = Debugger(True, "[Result]", styleText=dstyle(len_word=25, height=4))

printD(HotKeyD,"Crtl+c")
```

## Пример трассировки переменных

```python
from console_debugger import Debugger, printD
from console_debugger.helpful.template_obj import dDEBUG, dWARNING, dINFO

if __name__ == '__main__':
	a = Debugger(**dDEBUG)
	b = Debugger(**dINFO)
	c = Debugger(**dEXCEPTION)

	Debugger.GlobalManager(typePrint="socket")

	TracingName1 = "1"
	TracingName2 = ["1"]
	TracingName3 = "1",

	for x in range(10):
		printD(a, TracingName1)
		printD(b, TracingName2)
		printD(c, TracingName3)
```

![](https://i.imgur.com/8ctYa9G.png)

## Использование во `Flask`

Поместить `Debugger.GlobalManager` в `@app.before_first_request`

```python
from console_debugger import Debugger, printD

from flask import *

SECRET_KEY = "123_very_hard_password"
app = Flask(__name__)

 # Экземпляры в глобальной области видимости
cookDeb = Debugger(True, "[Cook]")
sessionDeb = Debugger(True, "[Session]")

@app.before_first_request
def deb():
    # Tkinter будет перезапускаться при каждом обновление сервера
    Debugger.GlobalManager(typePrint="socket")

@app.route("/login", methods=['POST', 'GET'])
def login():
    global data, cookDeb, sessionDeb
    cook = "no"
    ses = "no"

    # Получить куки если есть
    if request.cookies.get("logged"):
        cook = request.cookies.get("logged")

    # Получить данные из сессии если есть
    if "SessioN" in session:
        ses = session.get("SessioN")

    printD(cookDeb, cook)
    printD(sessionDeb, ses)

    res = make_response(render_template("login.html", cook=cook, session=ses))
    res.set_cookie(key="logged", value="yes", max_age=3)
    session["SessioN"] = "yes"
    return res

if __name__ == '__main__':
    app.run(debug=True)
```

`"login.html"`

```html
<script>
    document.cookie = "ex=1;";
    if (!document.cookie) {
        alert("Этот сайт требует включение cookie");
    }
</script>
Cook: {{ cook }}
<p></p>
Session: {{ session }}
<form action="/login" method="post" class="form-contact">
    <p><label>Name </label><input type="text" name="username" value="" required/>
    <p><label>Passwortitled </label><input type="text" name="password" value="" required/>
    <p><input type="submit" value="Send"/>
</form>
```

## Использование в `Django`

Добавить в самый конец `NameProj/settings.py`

```python
import os
from console_debugger import Debugger
from console_debugger.helpful.template_obj import dDEBUG, dWARNING, dINFO


DEBUG = True
...
...
...

if DEBUG:

    Info = Debugger(**dINFO)
    Debug = Debugger(**dDEBUG)
    Warning = Debugger(**dWARNING)
    
    if not os.environ.get('console_debugger', False): # Для защиты от двойного запуска Django
        os.environ['console_debugger'] = "True"
    else:
        Debugger.GlobalManager(typePrint="socket")
```

`NameApp/views.py`

```python
from NameProj.settings import Info,Debug,Warning
from console_debugger import printD

printD(Info,"1")
printD(Info,"2")
printD(Info,"3")
```

# Советы

## Вы можете использовать шаблон для комментирования `printD`

Так как входные параметры функции являются не изменяемыми обметками,
то они копируются в функцию `printD`, чтобы н тратить лишении наносекунды
на эту операцию, вы можете закомментировать все вызовы этой функции.

```cmd
\s{4}printD+
#none: printD
```

![Замена](https://i.imgur.com/cmzsU24.png)

А потом раскомментировать

```cmd
#none: printD
printD
```

![Замена](https://i.imgur.com/P0nugCD.png)

## Про режим отображения Tkinter

![](https://i.imgur.com/YJFYv57.png)

- Если нажать на заголовок консоли, то они выполнят команду из нижней консоли
- Если нажать нижнею кнопку `save geometry` то вы
    сохраните положение окна для следующих запусках, размеры сохранять в `console_debugger/gui/static/config.txt`
- Если закрыть окно `Tkinter`, до завершения главного потока, то данные будут отправляться в консоль `typePrint=None"`
- Можно сохранить весь текст из консоли в файл. Для этого нужно ввести в нижнею консоль `save <NAME_FILE> <PATH>` и нажать `Enter`
- Можно получить глобальную информацию о сокете, написав в любую нижнею консоль `g info` и нажать `Enter`
- Можно отчистить консоль вывода, если написать в нижнею консоль `clear` и нажать `Enter`

### Установка Tkinter на Linux

ArchLinux

```bush
sudo pacman -S tk

xrdb -load /dev/null
xrdb -query
```

## Про режим отображения Urwid

![](https://i.imgur.com/TQdW3by.png)

Работает также в терминале Pycharm
![](https://i.imgur.com/hJlPVZn.png)

Этот режим поддерживается в терминалах Linux. Программа находиться в `console_debugger/tui/main.py`.

- Можно сохранить весь текст из консоли в файл. Для этого нужно ввести `save <NAME_FILE> <PATH>`
- Горячие клавиши
    - `f1` = Влево
    - `f3` = Верх
    - `f2` = Вниз
    - `f4` = Вправо
    - `f5` = Меню
    - `Tab`= Вправо
    - `shif + ЛКМ` = Выделить текст
    - `shif + ctrl + C` = Копировать выделенный текст
    - `shif + ctrl + V` = Вставить текст
- Можно отчистить консоль вывода если написать в нижнею консоль `clear` и нажать `Enter`
