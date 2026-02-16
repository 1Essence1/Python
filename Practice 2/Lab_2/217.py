n = int(input())
a = list()
ans = set()
for i in range(n):
    s = input()
    a.append(s)
for i in a:
    cnt = 0
    for j in a:
        if j== i:
            cnt+=1
    if cnt == 3:
        ans.add(i)
print(len(ans))