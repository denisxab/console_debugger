from console_debugger.logic.debugger import *

if __name__ == '__main__':
    # Защита чтобы ide не убирал импорт
    print(Debugger.AllActiveInstance)
