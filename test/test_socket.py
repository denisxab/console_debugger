import random
import string
import time

from console_debugger.logic.debugger import printD, Debugger, dINFO, dDEBUG

# Сгенерировать случайное слово
random_word = lambda: "".join(random.choice(string.ascii_letters) for j in range(random.randint(30, 100)))

if __name__ == '__main__':
	Debugger._all_instance = {}
	Debug = Debugger(**dDEBUG)
	Info = Debugger(**dINFO)

	Debugger.GlobalManager(typePrint="socket")

	for i in range(5):
		printD(Debug, str(i))
		printD(Info, str(i))

	print("end1")

	time.sleep(1)

	for i in range(5):
		printD(Debug, str(i))
		printD(Info, str(i))

	print("end2")
