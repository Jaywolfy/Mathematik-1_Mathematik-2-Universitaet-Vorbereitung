# 1.1 Demo Interpreter
> python
> python
> Strg+D
> python
> exit

print('Hallo, Welt!')
4
3.5
1e6
5 + 3

# 1.2 Operatoren
7 + 3
4 * 2
7 / 2
7 // 2
7 / 0
7 % 0
3 + 2 * 4
(3 + 2) * 4
23 % 6
24 % 6
0.1 + 0.2
0.1 + 0.2 == 0.3


# 1.3 Variablen
x = 5
x
print(x)
y = 3
x + y

x = y * 12
x

x = y == 24
x

y < 24
y >= 24

# 1.4 Strings
"Hallo"
x = 5
x + 1
x + "Hallo"
"Hallo" + " Welt"
x = "Hallo"
y = "Welt"
x + " " + y
"H" + 1
# Sonderzeichen können problematisch sein
print("Name: "Thomas"")
print('Name: "Thomas"')
print("Name: \"Thomas\"")
print("Zeilenumbrüche sind mit \n markiert")
print("Zeilenumbrüche sind mit \\n markiert")


# 1.5 Konvertierung
type('x')
x = 5
type(x)
type(1 + 2.0)

x = "3"
x + 2
x
int(x)
int(x) + 2
int("abc")
int("abc", base=16)

4 + "3"
str(4) + "3"
float("4.5")
int("4.5")
int(float("4.5"))
str(3 == 3)

# Extrakram / Exkurs
ord("a")
chr(48)
chr(ord("a") + 1)

# 1.6 I/O
print("Lorem ipsum")
x = input("Gib etwas ein: ")
x
type(x)
x = input("Zahl: ")
x + 5
y = float(x)
y + 5
print("Y hat den Wert " + str(y) + "!")
print(f'Y hat den Wert {y}!')
print(f'Y+5 hat den Wert {y+5}!')
# Man kann auch mehrere Werte auf einmal ausgeben (ohne explizite Formatierung)
print(5, '-', 2, '=', 3)

# Im Interpreter etwas nutzlos, wichtig nur: kein Zeilenumbruch
print('Hallo')
print('Hallo', end='')
print(' Welt')
