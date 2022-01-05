
# f = open('example.txt')
f = open('input.txt')

# count = 0
# prev = None
# for line in f.readlines():
    # v = int(line)
    # if prev is not None and v > prev:
        # count += 1
    # prev = v

# print(count)


count = 0
vals = [int(v) for v in f.readlines()]

prev = None
for i in range(2, len(vals)):
    v = sum((vals[i-2], vals[i-1], vals[i]))
    if prev is not None and v > prev:
        count += 1
    prev = v

print(count)
