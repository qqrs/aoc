
# f = open('example.txt')
f = open('input.txt')

x = 0
y = 0

for line in f.readlines():
    (cmd, n) = line.split()
    n = int(n)

    if cmd == 'forward':
        x += n
    elif cmd == 'down':
        y += n
    elif cmd == 'up':
        y -= n


print((x,y))
print(x * y)
