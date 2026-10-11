# 2.1 Logische Operatoren

5 + 4 == 10
5 + 4 == 9
1 != 2
5 > 0
4 >= 3
-5 < 0
5.5 > 5.4
0.1 + 0.2 == 0.3
0.1 + 0.2 > 0.3
a = True
b = False
c = False
a and b
a or b
True ^ False
True ^ True
not a
# Präzedenz erläutern
not a and b
a or b and c
(a or b) and c


# 2.2 if-Anweisung
x = 5
if x < 5:
	print("X ist kleiner als 5")

x = 3
if x < 5:
	print("X ist kleiner als 5")

if True:
	print("Is True")

if x > 5:
	print("Ist größer als 5")
else:
	print("Ist kleiner als 5")

a = 2
if a == 0:
	print("A ist 0")
elif a == 1:
	print("A ist 1")
elif a == 2:
	print("A ist 2")
else:
	print("A ist was anderes")


# 2.2 match-Anweisung
a = 2
match a:
	case 0:
		print("A ist 0")
	case 1:
		print("A ist 1")
	case 2:
		print("A ist 2")
	case _:
		print("A ist was anderes")

# 2.3 while-Anweisung
x = 0
while x < 5:
	print(x)
	x = x + 1

x = 0
abort = False
while not abort:
	print(x)
	x = x + 1
	if x % 3 == 2:
		abort = True


# 2.4 continue / break
x = 0
while x < 10:
	if x == 5:
		x = x + 1
		continue
	print(x)
	x = x + 1

x = 0
while x < 10:
	if x == 5:
		x = x + 1
		break
	print(x)
	x = x + 1
print("Hallo")

while True:
	print("Hallo")

# 2.5 Listen
a = [1, 2, 3, 4, 5]
len(a)
a[2] = 4
a[-2] = 3

a = [1, 2, 3, 4, 5]
print(a)
i = 0
while i < len(a):
	print(a[i])
	a[i] = 0
	i = i + 1
print(a)

# 2.6 Slices / Strings
a = [1, 2, 3, 4, 5]
a[1:3]
a[:]
a[3:1:-1]

b = "12345"
b[1:3]
b[:]
b[3:1:-1]

c = [6, 7]
d = a + c
d
d.append(8)
d.pop()
a.reverse()
