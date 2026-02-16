n = int(input())
sum = 0
a = list(map(int , input().split()))
for i in range(n):
    if a[i] > 0:
        sum+=1
print(sum)