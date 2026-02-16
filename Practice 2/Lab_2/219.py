n = int(input())
a = list()
ch = list()
for i in range(n):
    name , epi = input().split()
    epi = int(epi)
    name = str(name)
    if name in ch:
        for j in range(len(a)):
            if a[j][0] == name:
                a[j] = (a[j][0], a[j][1] + epi)
                break
    else:
        a.append((name , epi))
        ch.append(name)
a.sort()
for i in range(len(a)):
    print(a[i][0] , a[i][1])