import os
import random
import string
import unittest

from logic.debugger import *

# Сгенерировать случайное слово
random_word = lambda: "".join(random.choice(string.ascii_letters) for j in range(random.randint(4, 100)))


class MyTestCase(unittest.TestCase):

    def setUp(self):
        Debugger.AllActiveInstance = []
        Debugger.AllSleepInstance = []
        Debugger.AllUseFileName = {}

        self.Debug = Debugger(**dDEBUG)
        self.Info = Debugger(**dINFO)
        self.Warning = Debugger(**dWARNING)
        self.TEST = Debugger(False, "TEST")

        self.TEST_File = Debugger(True, "TEST_File", fileConfig=dopen(file="debug.log",
                                                                      mode="a",
                                                                      encoding="utf-8"))

    # Проверка внутренних переменных
    def test___addFileName_in_AllUseFileName(self):

        Debugger.GlobalManager(typePrint="grid")

        self.assertEqual(self.Debug.title_name, '[DEBUG]')
        self.assertEqual(self.Debug.AllActiveInstance, ['[DEBUG]', '[INFO]', '[WARNING]', 'TEST_File'])
        self.assertEqual(self.Debug.AllSleepInstance, ['TEST'])
        self.assertEqual(self.Debug.AllUseFileName,
                         {'C:/Users/denis/PycharmProjects/console_debugger/test/debug.log': 'TEST_File'})
        self.assertEqual(len(self.Debug.AllInstance), 5)
        self.assertEqual(self.Debug.GlobalLenRows,
                         [('[DEBUG]', 25), ('[INFO]', 25), ('[WARNING]', 31), ('TEST_File', 9)])
        self.assertEqual(self.Debug.GlobalRowBoard,
                         "+-------------------------+-------------------------+-------------------------------+---------+")
        self.assertEqual(self.Debug.GlobalTkinterConsole, True)
        self.assertEqual(self.TEST_File.fileConfig,
                         {'file': 'debug.log', 'mode': 'a', 'buffering': 8192, 'encoding': 'utf-8', 'errors': None,
                          'newline': None, 'closefd': True})

        # Нельзя добавлять дебагеры с одинаковым `title_name`
        with self.assertRaises(NameError):
            Debug2 = Debugger(True, title_name="[DEBUG]")

        # Нельзя добавлять дебагеры с одинаковым именем файла `fileConfig`
        with self.assertRaises(FileExistsError):
            Debug2 = Debugger(True, title_name="test",
                              fileConfig=dopen(file="debug.log",
                                               mode="w"), )

    def test__str__repr__(self):
        self.assertEqual(str(self.Debug), "'[DEBUG]'")
        self.assertEqual(len(repr(self.Debug)), 683)

    # @unittest.skip("grid")
    def test_GlobalManager_grid(self):
        global random_word
        Debugger.GlobalManager(typePrint="grid")
        for i in range(10):
            printD(self.Debug, random_word())
            printD(self.Info, random_word())
            printD(self.Warning, random_word())
            printD(self.TEST, random_word())
            printD(self.TEST_File, random_word())

    # @unittest.skip("None")
    def test_GlobalManager_none(self):
        global random_word
        Debugger.GlobalManager(typePrint=None)
        for i in range(10):
            printD(self.Debug, random_word())
            printD(self.Info, random_word())
            printD(self.Warning, random_word())
            printD(self.TEST, random_word())
            printD(self.TEST_File, random_word())

    # @unittest.skip("tk")
    def test_GlobalManager_tk(self):
        global random_word
        Debugger.GlobalManager(typePrint="tk")
        for i in range(10):
            printD(self.Debug, random_word())
            printD(self.Info, random_word())
            printD(self.Warning, random_word())
            printD(self.TEST_File, random_word())

    def test_GlobalManager(self):
        # Проверка off/on всех дебагеров
        self.assertEqual(self.Debug.AllActiveInstance, ['[DEBUG]', '[INFO]', '[WARNING]', 'TEST_File'])
        self.assertEqual(self.Debug.AllSleepInstance, ['TEST'])
        Debugger.GlobalManager(global_active=False)
        self.assertEqual(Debugger.AllActiveInstance, [])
        self.assertEqual(Debugger.AllSleepInstance, ['TEST', '[DEBUG]', '[INFO]', '[WARNING]', 'TEST_File'])
        Debugger.GlobalManager(global_active=True)
        self.assertEqual(Debugger.AllSleepInstance, [])
        self.assertEqual(Debugger.AllActiveInstance, ['[DEBUG]', '[INFO]', '[WARNING]', 'TEST', 'TEST_File'])

    def test_local_active_deactivate(self):
        self.assertIn(self.Debug.title_name, Debugger.AllActiveInstance)
        self.Debug.active()
        self.assertIn(self.Debug.title_name, Debugger.AllActiveInstance)
        self.Debug.deactivate()
        self.assertNotIn(self.Debug.title_name, Debugger.AllActiveInstance)
        self.Debug.active()
        self.assertIn(self.Debug.title_name, Debugger.AllActiveInstance)

    def test_templates(self):
        global random_word
        Debugger.AllActiveInstance = []
        Debugger.AllSleepInstance = []
        Debugger.AllUseFileName = {}

        print("*" * 40)
        DEBUG = Debugger(**dDEBUG)
        INFO = Debugger(**dINFO)
        WARNING = Debugger(**dWARNING)
        EXCEPTION = Debugger(**dEXCEPTION)
        Debugger.GlobalManager(typePrint=None)
        printD(DEBUG, random_word())
        printD(INFO, random_word())
        printD(WARNING, random_word())
        printD(EXCEPTION, random_word())
        print("*" * 40)

    def __del__(self):
        try:
            os.remove("debug.log")
        except FileNotFoundError:
            pass

        try:
            os.remove("debug1.log")
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    unittest.main()
