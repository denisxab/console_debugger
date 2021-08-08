# Что это?

Это подключаемая библиотека, для удобного вывода  
отладочной информации.

---

# Как использовать ?

## 1 Сначала нужно создать экземпляры класса Debugger

Можно вручную указать параметры экземпляра

- `Debug_Name = Debugger(title_name: str, consoleOutput: bool = True, fileConfig: Optional[Dict] = None, active: bool = True, style_text: Optional[dstyle] = None)`
    - `title_name` = Уникальное имя экземпляра которое будет отображаться в выводе.  
    
    - `consoleOutput` = on/off отображения в консоль или другие
    визуальные выходы, **не влияет на запись в файл!**.  
    
    - `fileConfig` = Конфигурация записи в файл, входные параметры такие же как и у стандартной функции `open()`  
        передавать в формате `Dict{"file":"test.log", ... }`. Для удобного формирования параметров можно  
         пользоваться функцией `dopen()`.  
    
    - `active` = on/off жизни экземпляра, Если `False` экземпляр 
    будет равен `lambda *args: None`, а также будет добавлен в массив `Debugger.AllCountSleepInstance`.  
    
    - `style_text` = Стиль отображения текста. Для удобного формирования параметров можно  
        пользоваться функцией `dstyle`.  


Или использовать готовые параметры

- `Debug_Name = Debugger(**dDEBUG)`
    - dDEBUG
    - dINFO
    - dWARNING
    - dEXCEPTION

## 2 Установить глобальный стиль для всех экземпляров

Эта команда влияет на все экземпляры `Debugger`

- `Debugger.GlobalManager(global_disable=False, typePrint: Optional[str] = "grid"):`
    - `global_disable` = Вы можете отключить все экземпляры разом, они будут равны `lambda *args: None`
    - `typePrint=` = Глобальный стиль отображения данных
        - `"grid"` = Стиль таблица 
        
        ![](https://i.imgur.com/EwePtfk.png)
        
        - `"tk"` = Будет открыто **Tkinter** окно и 
        все записи будут направлены в него
        
        ![](https://i.imgur.com/OJP19OR.png)
        
        - `None` = Без стиля 
        
        ![](https://i.imgur.com/6BXZOBc.png)

## 3 Использовать в коде

Вызывать экземпляр напрямую

- `Debug_Name(text,*args, sep=' ', end='\n')`
    - `Debug_Name` = Имя экземпляра `Debugger`
    - `text` = Строка
    - `*args, sep=' ', end='\n'` = такие же, как и у встроенной функции `print()`

Либо использовать функцию для однородности

- `printD(Debug_Name, text, *args, sep=' ', end='\n')`
    - `Debug_Name` = Имя экземпляра `Debugger`
    - `text` = Строка
    - `*args, sep=' ', end='\n'` = такие же, как и у встроенной функции `print()`

---

# Примеры

## Использовать свои стили, вызывать экземпляры напрямую


Для наглядности создадим функцию для генерации случайного слово
```python
import random
import string             
# Сгенерировать случайное слово
random_word = lambda: "".join(random.choice(string.ascii_letters) for j in range(random.randint(1, 40)))
```

```python
from debugger import *

Debug = Debugger(title_name="[DEBUG]",

                 fileConfig=dopen(file="debug.log",
                                  mode="a",
                                  encoding="utf-8"),

                 style_text=dstyle(bg_color="bg_blue",
                                   len_word=21)
                 )
Info = Debugger(title_name="[INFO]",

                fileConfig={"file": "info.log",
                            "mode": "a", "encoding": "utf-8"},
                style_text=dstyle(len_word=25),

                consoleOutput=False
                )
Warning = Debugger("[WARNING]", style_text=dstyle(len_word=25))

Debugger.GlobalManager(typePrint="grid")

if __name__ == '__main__':
    for i in range(10):
        Warning(random_word())
        Debug(random_word())
        Info(random_word())
```

## Использовать готовые стили, вызывать `printD`

```python
from debugger import *

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

## Использовать GUI Tkinter
```python
from debugger import *


Debug = Debugger(**dDEBUG)
Info = Debugger(**dINFO)
Warning = Debugger(**dWARNING)
TEST = Debugger("TEST")

Debugger.GlobalManager(typePrint="tk")


for i in range(10):
    printD(Debug, random_word())
    printD(Info, random_word())
    printD(Warning, random_word())
    printD(TEST, random_word())
    time.sleep(0.3) # Задержка для наглядности поступления сообщений
```


## Советы

### Про интерфейс GUI Tkinter
- Tkinter запускается в новом потоке
- Если нажать на заголовок консоли, то она отчистится
- Если нажать нижнею кнопку `save geometry` то вы
сохраните положение окна на следующий запуск
- Если закрыть окно, то данные будут отправляться в консоль


### Про доступную информации об экземпляре `Debugger`
- public set:
    + `consoleOutput` = Вывод в консоль
    + `style_text` = Стиль отображения текста
    + `active()` = Включить дебагер
    + `deactivate()` = Отключить дебагер

- public get:
    + `title_name` = Уникальное имя дебагера
    + `fileConfig` = Конфигурация для файла
    + `AllCountActiveInstance` = Все активные дебагеры
    + `AllCountSleepInstance` = Все приостановленный дебагиры
    + `AllUseFileName` = Все используемые имена файлов
    + `AllInstance` = Все экземпляры дебагеров
