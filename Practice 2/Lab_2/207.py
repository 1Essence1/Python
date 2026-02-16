n = int(input())
a = list(map(int , input().split()))
mx = a[0]
pos = 0
for i in range(n):
    if a[i] > mx:
        pos = i
        mx = a[i]
print(pos + 1)
