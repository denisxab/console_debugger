# Что это?

Это подключаемая библиотека, для удобного вывода  
отладочной информации.

---

# Как использовать ?

## 1 Сначала нужно создать экземпляры класса Debugger

Можно вручную указать параметры экземпляра

- `Debug_Name = Debugger(active: bool,,title_name: str, consoleOutput: bool = True, fileConfig: Optional[Dict] = None style_text: Optional[dstyle] = None)`

     - `active` = on/off жизни экземпляра, Если `False` экземпляр 
    будет игнорировать вызов, а также будет добавлен в массив `Debugger.AllCountSleepInstance`.  
       
    - `title_name` = Уникальное имя экземпляра которое будет отображаться в выводе.  
    
    - `consoleOutput` = on/off отображения в консоль или другие
    визуальные выходы, **не влияет на запись в файл!**.  
    
    - `fileConfig` = Конфигурация записи в файл, входные параметры такие же как и у стандартной функции `open()`  
        передавать в формате `Dict{"file":"test.log", ... }`. Для удобного формирования параметров можно  
         пользоваться функцией `dopen()`.  
    
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

- `Debugger.GlobalManager(global_active=None, typePrint: Optional[str] = "grid"):`
    - `global_active` = Вы можете on/off все экземпляры разом
    - `typePrint=` = Глобальный стиль отображения данных
        - `"grid"` = Стиль таблица 
        
        ![](https://i.imgur.com/Kif40aB.png)
        
        - `"tk"` = Будет открыто **Tkinter** окно и 
        все записи будут направлены в него
        
        ![](https://i.imgur.com/OJP19OR.png)
        
        - `None` = Без стиля 
        
        ![](https://i.imgur.com/byg84id.png)

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
from console_debugger import *

Debug = Debugger(True,title_name="[DEBUG]",

                 fileConfig=dopen(file="debug.log",
                                  mode="a",
                                  encoding="utf-8"),

                 style_text=dstyle(bg_color="bg_blue",
                                   len_word=21)
                 )
Info = Debugger(True,title_name="[INFO]",

                fileConfig={"file": "info.log",
                            "mode": "a", "encoding": "utf-8"},
                style_text=dstyle(len_word=25),

                consoleOutput=False
                )
Warning = Debugger(True,"[WARNING]", style_text=dstyle(len_word=25))

Debugger.GlobalManager(typePrint="grid")

if __name__ == '__main__':
    for i in range(10):
        Warning(random_word())
        Debug(random_word())
        Info(random_word())
```

## Использовать готовые стили, вызывать `printD`

```python
from console_debugger import *

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
from console_debugger import *


Debug = Debugger(**dDEBUG)
Info = Debugger(**dINFO)
Warning = Debugger(**dWARNING)
TEST = Debugger(True,"TEST")

Debugger.GlobalManager(typePrint="tk")


for i in range(10):
    printD(Debug, random_word())
    printD(Info, random_word())
    printD(Warning, random_word())
    printD(TEST, random_word())
    time.sleep(0.3) # Задержка для наглядности поступления сообщений
```

### Использование во Flask
```python
from console_debugger import *
from flask import * 

SECRET_KEY = "123_very_hard_password"
app = Flask(__name__)

cookDeb = Debugger(True, "[Cook]")
sessionDeb = Debugger(True, "[Session]")

@app.before_first_request
def deb():
    # Tkinter будет перезапускаться при каждом обновление сервера
    Debugger.GlobalManager(typePrint="tk")

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
