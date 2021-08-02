




# Что это?
Это подключаемая библиотека, для удобного вывода
отладочной информации.
  

---
# Как использовать ?

## Cоздать экземпляры класса
Сначала нужно создать экземпляры класса Debugger, они имеют
следующие параметры

```python
Debugger(title: str,
         consoleOutput: bool = True,
         fileConfig: Optional[Dict] = None,
         active: bool = True,
         style_text: Optional[dstyle] = None)
```
- `title` = Уникальное имя экземпляра которое будет отображаться в выводе.

- `consoleOutput` = Переключатель режима отображения в консоль, **не влияет на запись в файл!**.

- `fileConfig` = Конфигурация записи в файл, входные параметры такие же как и у стандартной функции `open()`
передавать в формате Dict{"nameParams":"arg"}. Для удобного формирования параметров можно 
пользоваться функцией `dopen()`.

- `active` = Переключатель жизни экземпляра, Если `False` экземпляр не будет формирвоаться
 и будет равен `lambda *args: None`, а также будет добавлен в массив `Debugger.AllCountSleepInstance`.
 
- `style_text` = Стиль отображения текста. Для удобного формирования параметров можно 
пользоваться функцией `dstyle`.

## Установить глобальный стиль для всех экземпляров

```python
Debugger.GlobalManager(global_disable=False, 
                        typePrint: Optional[str] = "grid"):
```
- `global_disable` = Вы можете отключить все экземпляры разом, они дут равны `lambda *args: None`

- `typePrint` = Глобальный тип отображения данных
> `grid` 
>>![Debugger typePrint="grid"](https://i.imgur.com/XeOpvQO.png)

> `None` 
>>![Debugger](https://i.imgur.com/0n4G80k.png)

## Использовать в коде
```python
Debug(text,
      *args, sep=' ', end='\n')
```
- `text` = Строка
- `*args, sep=' ', end='\n'` = такие же, как и у встроенной функции `print()`

---


# Примеры

## Пример 1
```python
Debug = Debugger(title_id="[DEBUG]",

                 fileConfig=dopen(file="debug.log",
                                  mode="a",
                                  encoding="utf-8"),

                 style_text=dstyle(bg_color="bg_blue",
                                   len_word=21)
                 )

Info = Debugger(title_id="[INFO]",

                fileConfig={"file": "info.log",
                            "mode": "a",
                            "encoding": "utf-8"},

                style_text=dstyle(len_word=25),

                consoleOutput=False
                )

Warning = Debugger("[WARNING]", style_text=dstyle(len_word=25))

Debugger.GlobalManager(typePrint="grid")

for i in range(10):
    Warning(f"Warning \t{str(i)}")
    Debug(f"Debug \t{str(i)} \n your data")
    Info(f"Info \t{str(i)}")
```


## Пример работы в потоках
Дополнительной синхронизации потоков при выводе в консоль нет. Но так как 
таблицы формируется заранее, с обращением к глобальным данным на нее действуют 
встроенный GIL, потом уже готовую строку отображают функция `print()`. 
Благодаря этому данные не искажаются.
>Обычный print
>>![Обычный print](https://i.imgur.com/0ii66Ra.png)

>Debugger
>>![Debugger](https://i.imgur.com/0n4G80k.png)

>Debugger typePrint="grid"
>>![Debugger typePrint="grid"](https://i.imgur.com/XeOpvQO.png)



