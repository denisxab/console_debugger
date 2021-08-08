# Что это?

Это подключаемая библиотека, для удобного вывода  
отладочной информации.

---

# Как использовать ?

## 1 Сначала нужно создать экземпляры класса Debugger

Можно вручную указать параметры экземпляра

- `Debug_Name = Debugger(title_id: str, consoleOutput: bool = True, fileConfig: Optional[Dict] = None, active: bool = True, style_text: Optional[dstyle] = None)`
    - `title_id` = Уникальное имя экземпляра которое будет отображаться в выводе.  
    
    - `consoleOutput` = Переключатель режима отображения в консоль, **не влияет на запись в файл!**.  
    
    - `fileConfig` = Конфигурация записи в файл, входные параметры такие же как и у стандартной функции `open()`  
        передавать в формате Dict{"nameParams":"arg"}. Для удобного формирования параметров можно  
         пользоваться функцией `dopen()`.  
    
    - `active` = Переключатель жизни экземпляра, Если `False` экземпляр не будет формироваться  
         и будет равен `lambda *args: None`, а также будет добавлен в массив `Debugger.AllCountSleepInstance`.  
    
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
        - `None` = Без стиля

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

```python
from debugger import *

Debug = Debugger(title_id="[DEBUG]",

                 fileConfig=dopen(file="debug.log",
                                  mode="a",
                                  encoding="utf-8"),

                 style_text=dstyle(bg_color="bg_blue",
                                   len_word=21)
                 )
Info = Debugger(title_id="[INFO]",

                fileConfig={"file": "info.log",
                            "mode": "a", "encoding": "utf-8"},
                style_text=dstyle(len_word=25),

                consoleOutput=False
                )
Warning = Debugger("[WARNING]", style_text=dstyle(len_word=25))

Debugger.GlobalManager(typePrint="grid")

if __name__ == '__main__':
    for i in range(10):
        Warning(f"Warning \t{str(i)}")
        Debug(f"Debug \t{str(i)} \n your data")
        Info(f"Info \t{str(i)}")
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
        printD(Debug, "123")
        printD(Warning, "123")
        printD(Info, "123")
```
