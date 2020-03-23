import random
def print_line(m):
    print("-" * 12 * (m+1))
max_num = 220
min_num = 120
k = 4
while True:
    m = input("m (integer):")
    if m.isnumeric():
        print("OK")
        m = int(m)
        break
    else:
        print("m must be integer")

print_line(m)
print("| " + '{:<10}'.format(""), end="")
for i in range(1, m+1):
    print("| " + '{:<10}'.format("yi" + str(i)), end="")
print("|")
print_line(m)

y = []

for j in range(1, k+1):
    y.append([])
    print("| " + '{:<10}'.format(j), end="")
    for i in range(1, m+1):
        r = round(random.random() * (max_num - min_num) + min_num)
        y[j-1].append(r)
        print("| " + '{:<10}'.format(r), end="")
    print("|")
    print_line(m)