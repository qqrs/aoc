
#f = open('example.txt')
f = open('input.txt')

x = 0
y = 0
aim = 0

for line in f.readlines():
    (cmd, n) = line.split()
    n = int(n)

    if cmd == 'forward':
        x += n
        y += aim * n
    elif cmd == 'down':
        aim += n
    elif cmd == 'up':
        aim -= n


print((x,y))
print(x * y)
