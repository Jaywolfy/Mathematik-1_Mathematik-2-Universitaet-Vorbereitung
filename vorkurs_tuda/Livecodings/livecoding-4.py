# 4.1 Rekursion
# Gestern haben wir bereits normale Funktionen und deren Aufrufe kennengelernt
# Man kann auch die Funktion selbst in der gerade definierten Funktion aufrufen

def fib(n):
	if n <= 1:
		return 1
	return fib(n-1) + fib(n-2)
print(fib(1))


def print_list(lst):
	for e in lst:
		if type(e) == list:
			print_list(e)
		else:
			print(e)

print_list([5, [3, 6, 2, [1, 4], 3], 7, 8, [10]])


# Praktischere Beispiele sind das Ausgeben von Ordnerstrukturen
# Könnt ihr natürlich auch nutzen, wenn ihr nicht mehr wisst, wo eure Python-Datei ist, kann aber ein bisschen dauern

import os

def tree(folder, depth):
	children = os.listdir(folder)
	for child in children:
		print(("| "*depth) + "+-", child)
		path = folder + "/" + child
		if os.path.isdir(path):
			tree(path, depth+1)
tree(".", 0)

# Anpassung, dass print() nur, wenn bestimmte Dateiendung
def tree(folder, ext):
	children = os.listdir(folder)
	for child in children:
		path = folder + "/" + child
		if path.endswith("." + ext):
			print(path)
		if os.path.isdir(path):
			tree(path)

# Ausführen in einem Ordner, wo es ewig dauert
tree(".", "py")


# 4.2 Rekursion - Stack Overflow
# Wichtig dabei ist, dass man die Funktion nicht zu häufig aufruft, z.B. Endlos:

def f():
	print(n)
	f(n)
f(20)

# Man braucht immer ein definiertes Ende, den Rekursionsanker

def f(n):
	print(n)
	if (n >= 0):
		f(n-1)
f(20)

def f(n):
	print(n)
	if (n >= 0):
		f(n-1)
f(20)

# Hilft natürlich auch nicht, wenn man zu häufig aufruft …
f(10000)
