import random
import math
import numpy
import copy
from scipy.stats import t
from scipy.stats import f

def cochran(f1, f2, q):
    fish = f.isf(q/f2, f1, (f2 - 1)*f1)
    result = fish/(fish + f2 - 1)
    return result

def print_line(m):
    print("-" * 12 * (m+1))

def part2(yi, x):
    global b
    k = len(x[0])
    mx = []
    len_x = len(x)
    for i in range(len_x):
        mx.append(round(sum(x[i])/k, 3))
    my = round(sum(yi)/k, 3)
    a0 = []
    for i in range(len_x):
        a0.append(round(sum([x[i][j] * yi[j] for j in range(k)])/k, 3))
    a = []
    for i in range(len_x):
        a.append([])
        for j in range(len_x):
            a[i].append(round(sum([x[i][l] * x[j][l] for l in range(k)])/k, 3))

#    delta = numpy.array()
    base = [[1, mx[0], mx[1], mx[2]],
          [mx[0], a[0][0], a[0][1], a[0][2]],
          [mx[1], a[1][0], a[1][1], a[1][2]],
          [mx[2], a[2][0], a[2][1], a[2][2]]]

    delta = round(numpy.linalg.det(base), 3)

    b = [copy.deepcopy(base) for i in range(k+1)]
    for i in range(len_x+1):
        b[i][0][i] = my
        for j in range(len_x):
            b[i][j+1][i] = a0[j]
        b[i] = round(numpy.linalg.det(b[i])/delta, 3)

        print("b" + str(i) + ": " + str(b[i]))


max_num = 231.667
min_num = 196.667
x = [[-30, -30, 0, 0],
     [10, 60, 10, 60],
     [10, 35, 35, 10]]
k = len(x[0])
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
        r = round(random.random() * (max_num - min_num) + min_num, 3)
        y[j-1].append(r)
        print("| " + '{:<10}'.format(r), end="")
    print("|")
    print_line(m)

yi = []
sigma2 = []
for i in range(k):
    yi.append(round(1/m * sum(y[i]), 3))

print("y (середні): " + str(yi))

part2(yi, x)

x = [[1, 1, 1, 1],
     [-1, -1, 1, 1],
     [-1, 1, -1, 1],
     [-1, 1, 1, -1]]

print("y: " + str(y))
print("yi: " + str(yi))

S2 = []
for i in range(len(y)):
    S2.append(sum([(y[i][j] - yi[i])**2 for j in range(len(y[i]))]))
    S2[i] = round(S2[i]/len(y[i]), 3)
print("S2: " + str(S2))

Gp = round(max(S2)/sum(S2), 3)
print("Gp: " + str(Gp))

f1 = m - 1
f2 = k

print("f1:" + str(f1))
print("f2:" + str(f2))

Gcr = round(cochran(f1, f2, 0.05), 4)
print("Gcr: " + str(Gcr))
if Gp < Gcr:
    print("Cochran's C: OK")
else:
    print("Cochran's C: :(")
    exit(0)

S2v = sum(S2)/4

S2b = round(S2v/(4 * m), 3)
Sb = round(math.sqrt(S2b), 3)

f3 = f1 * f2
print("f3: " + str(f3))
t = round(t.ppf(1-0.05 / 2, df=f3), 3)
print("t: " + str(t))
bs = []
ts = []
d = 0
for i in range(4):
    bs.append(round(sum([yi[j] * x[i][j] for j in range(4)])/4, 3))
    ts.append(round(bs[i]/Sb, 3))
    if ts[i] > t:
        ts[i] = True
        d += 1
    else:
        ts[i] = False

print("Чи значимі b: " + str(ts))

f4 = k - d
print("f4: " + str(f4))
x = [[-30, -30, 0, 0],
     [10, 60, 10, 60],
     [10, 35, 35, 10]]
yj = []
for i in range(4):
    yj.append(0)
    for j in range(4):
        if ts[j]:
            if j == 0:
                yj[i] += b[0]
            else:
                yj[i] += b[j] * x[j-1][i]
print("yj: " + str(yj))

S2ad = round(m * sum([(yj[i] - yi[i])**2 for i in range(4)])/f4, 3)

Fp = round(S2ad/S2v, 3)
print("Fp: " + str(Fp))
Fcr = round(f.ppf(1 - 0.05, f4, f3), 1)
print("Fcr: " + str(Fcr))
if Fp < Fcr:
    print("F-criteria: OK")
else:
    print("F-criteria: :(")