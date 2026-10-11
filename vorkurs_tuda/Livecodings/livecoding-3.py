# 3.1 Dictionaries
d = dict()
d[2] = 5
d
d = {2: 5}
print(d[3])
print(d.get(3, 0))
d['name'] = 'Tim'
d['age'] = 28
d[True] = 7.4
d[(2, 3)] = 'no'
print(d[(2, 3)])
print(d)
for key, value in d.items():
	print(f'Für Schlüssel "{key}" ist der Wert "{value}" gespeichert')

# 3.2 for-Schleife
for i in range(10):
	print(i)

a = [6, 9, 1, 2]
for i in range(len(a)):
	print(f'Element an Index {i} ist {a[i]}')

for k, e in enumerate(a):
	print(f'Element an Index {k} ist {e}')

for i in range(2, 10, 3):
	print(i)

for i in range(10, 2, -3):
	print(i)

b = [1, 3, 2, 4]
for i, j in zip(a, b):
	print(i + j)


# 3.3 Dateioperationen
f = open("hallo.txt") # Pfad muss richtig sein!
for k, line in enumerate(f.readlines()):
	print(f'Zeile {k}: {line}')
f.close()

f = open("welt.txt", "w")
f.write("Hallo\n") # Zeilenumbruch muss explizit gegeben werden im Gegensatz zu print()
f.write("Welt\n")
f.close()

with open("welt.txt", "a") as f:
	f.write("Schnupsi\n")
	f.write("Dubsi\n")
	f.close()

# 3.4 Funktionen
# Wir kennen bereits:
int("4")
print("Hallo")
# etc.

# Wir können auch eigene Funktionen definieren …
def fun(name, n):
	msg = "Hallo, " + name
	for i in range(n):
		print(f'{msg}')

# … und aufrufen
fun("Thorsten", 2)
fun("Anna", 4)

# Diese können wir auch wiederum in anderen Funktionen referenzieren:
def hi():
	name = input("Name: ")
	n = input("Anzahl: ")
	fun(name, int(n))

hi()
