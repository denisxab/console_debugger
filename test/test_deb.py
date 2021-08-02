import os
import threading
import unittest

from coloring_text import *
from debugger import Debugger
from templates import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        Debugger.AllCountActiveInstance = []
        Debugger.AllCountSleepInstance = []
        Debugger.AllUseFileName = {}
        self.Debug1 = Debugger(title_id="[DEBUG]",

                               fileConfig=dopen(file="debug.log",
                                                mode="a",
                                                encoding="utf-8"),

                               style_text=dstyle(bg_color="bg_blue",
                                                 len_word=15)

                               )

    def test___addFileName_in_AllUseFileName(self):
        with self.assertRaises(FileExistsError):
            Debug2 = Debugger(title_id="Test",
                              fileConfig=dopen(file="debug.log",
                                               mode="w"),
                              )

    def test_changePrivateData(self):
        testD = Debugger(title_id="Test", active=False)

        # Проверка защиты атрибута Debugger от внешних изменений
        self.assertEqual(self.Debug1.fileConfig,
                         {'file': 'debug.log', 'mode': 'a', 'buffering': 8192, 'encoding': 'utf-8', 'errors': None,
                          'newline': None, 'closefd': True})

        self.assertEqual(self.Debug1.AllCountActiveInstance, ['[DEBUG]'])
        self.assertEqual(self.Debug1.AllCountSleepInstance, ['Test'])
        self.assertEqual(self.Debug1.AllUseFileName,
                         {'C:/Users/denis/PycharmProjects/console_debugger/test/debug.log': '[DEBUG]'})

        with self.assertRaises(AttributeError):
            self.Debug1.fileConfig = None
        with self.assertRaises(AttributeError):
            self.Debug1.AllCountActiveInstance = None
        with self.assertRaises(AttributeError):
            self.Debug1.AllCountSleepInstance = None
        with self.assertRaises(AttributeError):
            self.Debug1.AllUseFileName = None

    def test__str__repr__(self):
        self.assertEqual(str(self.Debug1), "'[DEBUG]'")
        self.assertEqual(self.Debug1.title, "[DEBUG]")
        self.assertEqual(len(repr(self.Debug1)), 719)

    def test___call__(self):
        self.Debug1("Test Message")

    def test_style_t(self):
        test_text_style_shotLen = style_t("test", color="red", bg_color="bg_blue", attrs=["bold"], len_word=3)
        self.assertEqual(repr(test_text_style_shotLen), 't..')
        self.assertEqual(str(test_text_style_shotLen), '\x1b[1m\x1b[44m\x1b[31mt..\x1b[0m')

        test_text_style_LongLen = style_t("test", color="red", bg_color="bg_blue", attrs=["bold"], len_word=10)
        self.assertEqual(repr(test_text_style_LongLen), 'test      ')
        self.assertEqual(str(test_text_style_LongLen), '\x1b[1m\x1b[44m\x1b[31mtest      \x1b[0m')

    def test_cprint(self):
        cprint("test", color="red", bg_color="bg_blue", attrs=["bold"], len_word=3)

    def test_GlobalManager(self):
        testWarning = Debugger("[WARNING]", style_text=dstyle(len_word=25))
        Debugger.GlobalManager()
        self.assertEqual(Debugger.GlobalLenRows, [('[DEBUG]', 15), ('[WARNING]', 25)])
        self.assertEqual(Debugger.GlobalRowBoard, '+---------------+-------------------------+')
        self.Debug1("12313H\nello wor\tld ")
        self.setUp()

        testWarning = Debugger("[WARNING]", style_text=dstyle(len_word=25))
        Debugger.GlobalManager(typePrint=None)
        self.assertEqual(Debugger.GlobalLenRows, [])
        self.assertEqual(Debugger.GlobalRowBoard, '')
        self.Debug1("12313Hello wor\tld ")
        testWarning("Hello wor\tld ")

        self.assertEqual(Debugger.AllCountSleepInstance, [])
        self.assertEqual(Debugger.AllCountActiveInstance, ['[DEBUG]', '[WARNING]'])

        saveFun = Debugger.__call__

        Debugger.GlobalManager(global_disable=True)

        self.assertEqual(Debugger.AllCountSleepInstance, ["GLOBAL_DISABLE"])
        self.assertEqual(Debugger.AllCountActiveInstance, ["GLOBAL_DISABLE"])

        Debugger.__call__ = saveFun

    def test_StyleText_strip(self):
        a = " 3132  "
        a1 = "3132  "
        a2 = " 3132"

        self.assertEqual(StyleText(a, "").strip(), "3132")
        self.assertEqual(StyleText(a1, "").strip(), "3132")
        self.assertEqual(StyleText(a2, "").strip(), "3132")

    def test_treadPrint(self):

        Debug = Debugger(title_id="[DEBUG]",

                         fileConfig=dopen(file="debug1.log",
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

        def testPrintThread1():
            nonlocal Debug
            for i in range(10):
                # print(f"Deb \t{str(i)}")
                Debug(f"Deb \t{str(i)}")

        def testPrintThread2():
            nonlocal Warning
            for i in range(10):
                # print(f"Warning \t{str(i)}")
                Warning(f"Warning \t{str(i)}")

        threadList = []
        #
        for th in range(2):
            tmp = threading.Thread(target=testPrintThread1 if th % 2 else testPrintThread2)
            threadList.append(tmp)
            tmp.start()
        #
        for th in threadList:
            th.join()

    def test_templates(self):

        cprint("1312", **dDEBUG)
        cprint("1312", **dINFO)
        cprint("1312", **dWARNING)
        cprint("1312", **dEXCEPTION)

        self.assertEqual(style_t("1312", **dDEBUG).style_text, '1312                     ')
        self.assertEqual(style_t("1312", **dINFO).style_text, '\x1b[34m1312                     \x1b[0m')
        self.assertEqual(style_t("1312", **dWARNING).style_text,
                         '\x1b[1m\x1b[33m1312                           \x1b[0m')
        self.assertEqual(style_t("1312", **dEXCEPTION).style_text,
                         '\x1b[1m\x1b[31m1312                           \x1b[0m')

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
