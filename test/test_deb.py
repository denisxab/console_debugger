import os
import random
import string
import time
import unittest
from os.path import dirname

from console_debugger.helpful.coloring_text import StyleText, cprint
from console_debugger.logic.debugger import printD, Debugger, dINFO, dWARNING, dDEBUG, dEXCEPTION, dopen, style_t

# Сгенерировать случайное слово
random_word = lambda: "".join(random.choice(string.ascii_letters) for j in range(random.randint(30, 100)))


PATH_TEST = "/".join(dirname(__file__).replace("\\", "/").split("/"))

class Test_debugger(unittest.TestCase):

    def setUp(self):

        Debugger._all_instance = {}

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
        self.assertEqual(self.Debug.AllActiveInstance(), ['[DEBUG]', '[INFO]', '[WARNING]', 'TEST_File'])
        self.assertEqual(self.Debug.AllSleepInstance(), ['TEST'])
        self.assertEqual(self.Debug.AllUseFileName(),
                         {f'{PATH_TEST}/debug.log': 'TEST_File'})
        self.assertEqual(len(self.Debug._all_instance), 5)
        self.assertEqual(self.Debug._global_len_rows,
                         [('[DEBUG]', 25), ('[INFO]', 25), ('[WARNING]', 31), ('TEST_File', 9)])
        self.assertEqual(self.Debug._global_row_board,
                         "+-------------------------+-------------------------+-------------------------------+---------+")
        # self.assertEqual(self.Debug.is_SendDataToSocket, True)
        self.assertEqual(self.TEST_File.fileConfig,
                         {'buffering': 8192,
                          'closefd': True,
                          'encoding': 'utf-8',
                          'errors': None,
                          'file': f'{PATH_TEST}/debug.log',
                          'mode': 'a',
                          'newline': None})

        # Нельзя добавлять дебагеры с одинаковым `title_name`
        with self.assertRaises(NameError):
            Debug2 = Debugger(True, title_name="[DEBUG]")

        # Нельзя добавлять дебагеры с одинаковым именем файла `fileConfig`
        with self.assertRaises(FileExistsError):
            Debug2 = Debugger(True, title_name="test",
                              fileConfig=dopen(file="debug.log",
                                               mode="w"), )

    def test__str__repr__(self):
        self.assertEqual(str(self.Debug), "[DEBUG]")
        
        
        self.assertEqual(len(repr(self.Debug)), 675)
        printD(self.Debug, '1', '2', '3')

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

    # @unittest.skip("socket")
    def test_GlobalManager_socket(self):
        global random_word
        Debugger.GlobalManager(typePrint="socket")

        test_name1 = "123"
        TEST_NAME2 = "".join([str(x % 10) for x in range(50)])
        TEST_NAME3 = "123"
        TEST_NAME4 = random_word()

        for i in range(10):
            printD(self.Debug, test_name1)
            printD(self.Debug, '1', '2', '3')
            printD(self.Debug, {'1', '2'}, ('2',), ['3'], "4")  # Обрабатывать любой тип
            printD(self.Info, TEST_NAME2)
            printD(self.Warning, TEST_NAME3)
            printD(self.TEST, random_word())
            printD(self.TEST_File, TEST_NAME4)

        for i in range(10):
            printD(self.Debug, i)
            printD(self.Info, i)
            printD(self.Warning, i)
            printD(self.TEST, i)
            printD(self.TEST_File, i)

    # Проверка off/on всех дебагеров
    def test_GlobalManager(self):

        self.assertEqual(self.Debug.AllActiveInstance(), ['[DEBUG]', '[INFO]', '[WARNING]', 'TEST_File'])
        self.assertEqual(self.Debug.AllSleepInstance(), ['TEST'])

        Debugger.GlobalManager(global_status=False)

        self.assertEqual(Debugger.AllActiveInstance(), [])
        self.assertEqual(Debugger.AllSleepInstance(), ['[DEBUG]', '[INFO]', '[WARNING]', 'TEST', 'TEST_File'])
        for k, v in Debugger._all_instance.items():
            self.assertEqual(v._Debugger__active, False)

        Debugger.GlobalManager(global_status=True)

        self.assertEqual(Debugger.AllSleepInstance(), [])
        self.assertEqual(Debugger.AllActiveInstance(), ['[DEBUG]', '[INFO]', '[WARNING]', 'TEST', 'TEST_File'])
        for k, v in Debugger._all_instance.items():
            self.assertEqual(v._Debugger__active, True)

    def test_local_active_deactivate(self):
        self.assertIn(self.Debug.title_name, Debugger.AllActiveInstance())
        self.Debug.active()
        self.assertIn(self.Debug.title_name, Debugger.AllActiveInstance())
        self.Debug.deactivate()
        self.assertNotIn(self.Debug.title_name, Debugger.AllActiveInstance())
        self.Debug.active()
        self.assertIn(self.Debug.title_name, Debugger.AllActiveInstance())

    def test_templates(self):
        global random_word
        Debugger._all_instance = {}
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


class Test_coloring_text(unittest.TestCase):

    def test_style_t(self):
        """
        1. Выравнивание текста
        2. Перенос длинных строк на новую строку +
            2.1 обрезание длинных строк +
            2.2 проверка не удалять элемент из пустого массива +
        3. Удлинять короткие слова +
        4. Применять стили к тексту
        """

        self.assertEqual(str(StyleText("123", "321")), "321")
        self.assertEqual(repr(StyleText("123", "321")), "123")

        """
        1. Выравнивание текста
        """

        self.assertEqual(list(style_t("123", len_word=10, agl="center").style_text),
                         [' ', ' ', ' ', '1', '2', '3', ' ', ' ', ' ', ' '])

        self.assertEqual(list(style_t("1234", len_word=10, agl="center").style_text),
                         [' ', ' ', ' ', '1', '2', '3', '4', ' ', ' ', ' '])

        self.assertEqual(list(style_t("1234", len_word=3, agl="center").style_text),
                         ['1', '.', '.'])

        """ 
         2.2 проверка не удалять элемент из пустого массива +
        """
        test_pop = style_t("", len_word=10)
        self.assertEqual(test_pop.style_text, "")
        self.assertEqual(test_pop.present_text, "")

        list_true = [
            [
                ['1', '2', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['1', '2', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' '],

                ['1', '2', '\n', '3', ' '],
                ['1', '2', '\n', '3', ' '],
                ['1', '2', '\n', '3', ' '],
                ['1', '2', '\n', '3', ' '],
                ['1', '2', '\n', '3', ' '],
                ['1', '2', '\n', '3', ' '],
            ],

            [
                ['1', '2', '3', '1', '2', '3', '\t', 'g', 'f', '\n', 'g', 'S', 'D', 'F', ' ', ' ', ' ', ' ', ' ', ' '],
                ['1', '2', '3', '1', '2', '3', '\t', 'g', 'f', '\n', 'g', 'S', 'D', 'F', ' ', ' ', ' ', ' ', ' ', ' '],

                ['1', '2', '\n', '3', '.'],
                ['1', '2', '\n', '3', '.'],

                ['1', '2', '\n', '3', '\n', '1', '2', '\n', '3', '\t', '\n', 'g', 'f', '\n', 'g', 'S', '\n', 'D', 'F'],
                ['1', '2', '\n', '3', '\n', '1', '.'],

                ['1', '2', '\n', '3', '\n', '1', '2', '\n', '3', '\t', '\n', 'g', 'f', '\n', 'g', 'S', '\n', 'D', 'F'],
                ['1', '2', '\n', '3', '\n', '1', '.'],
            ],
            [
                ['1', '2', '3', 'q', 'w', 'd', 'q', 'w', 'd', 'q', '\n', 'w', 'q', 'w', 'd', 'w', 'q', 'd', 'q', 's',
                 '.'],
                ['1', '2', '3', 'q', 'w', 'd', 'q', 'w', 'd', 'q', '\n', 'w', 'q', 'w', 'd', 'w', 'q', 'd', 'q', 's',
                 '.'],

                ['1', '2', '\n', '3', '.'],
                ['1', '2', '\n', '3', '.'],

                ['1', '2', '\n', '3', 'q', '\n', 'w', 'd', '\n', 'q', 'w', '\n', 'd', 'q', '\n', 'w', 'q', '\n', 'w',
                 'd', '\n', 'w', 'q', '\n', 'd', 'q', '\n', 's', '.'],

                ['1', '2', '\n', '3', 'q', '\n', 'w', '.'],

                ['1', '2', '\n', '3', 'q', '\n', 'w', 'd', '\n', 'q', 'w', '\n', 'd', 'q', '\n', 'w', 'q', '\n', 'w',
                 'd', '\n', 'w', 'q', '\n', 'd', 'q', '\n', 's', '.'],

                ['1', '2', '\n', '3', 'q', '\n', 'w', '.'],

            ],
        ]

        list_test = [
            "123",
            "123\n123\tgfgSDF",
            "123qwdqwdqwqwdwqdqsscqwergtrhtregrWASDFasD123gfgSDF",
        ]

        """
        2.1 обрезание длинных строк +
        3. Удлинять короткие слова +
        """
        for true_data, test_set in zip(list_true, list_test):
            self.assertEqual(list(style_t(test_set, len_word=10).style_text), true_data[0])
            self.assertEqual(list(style_t(test_set, len_word=10).present_text), true_data[1])

            self.assertEqual(list(style_t(test_set, len_word=2).style_text), true_data[2])
            self.assertEqual(list(style_t(test_set, len_word=2).present_text), true_data[3])

            self.assertEqual(list(style_t(test_set, len_word=2, height=10).present_text), true_data[4])
            self.assertEqual(list(style_t(test_set, len_word=2, height=3).present_text), true_data[5])

            self.assertEqual(list(style_t(test_set, len_word=2, height=10).style_text), true_data[6])
            self.assertEqual(list(style_t(test_set, len_word=2, height=3).style_text), true_data[7])

        """
        4. Применять стили к тексту
        """
        self.assertEqual(style_t("123", color="red", bg_color="bg_blue", attrs=["bold"]).style_text,
                         '\x1b[1m\x1b[44m\x1b[31m123\x1b[0m')

        cprint("123", color="red", bg_color="bg_blue", attrs=["bold"])


class TestTh_MgSendSocketData(unittest.TestCase):
    # @unittest.skip("0")
    def setUp(self):
        Debugger._all_instance = {}
        self.Debug = Debugger(**dDEBUG)
        self.Info = Debugger(**dINFO)

    # @unittest.skip("0")
    def test_send_port(self):
        global random_word
        Debugger.GlobalManager(typePrint="socket")

        for i in range(5):
            printD(self.Debug, str(i))
            printD(self.Info, str(i))

        print("end1")

        time.sleep(1)

        for i in range(5):
            printD(self.Debug, str(i))
            printD(self.Info, str(i))

        print("end2")


if __name__ == '__main__':
    unittest.main()
