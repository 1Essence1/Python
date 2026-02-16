n = int(input())
a = list(map(int , input().split()))
mx = 0
mn = 0
for i in a:
    cnt = 0
    for j in a:
        if i == j:
            cnt+=1
    if cnt > mx:
        mx = cnt
        mn = i
    elif cnt == mx:
        if i < mn:
            mn = i
print(mn)