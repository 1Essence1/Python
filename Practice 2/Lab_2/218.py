n = int(input())
ans = list()
a = list()
ch = list()
for i in range(n):
    m = input()
    if m in ch:
        continue
    else:
        ch.append(m)
        a.append((m , i + 1))
a.sort()
for i in range(len(a)):
    print(a[i][0] , a[i][1])