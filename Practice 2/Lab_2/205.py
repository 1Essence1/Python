n = int(input())
p = 0
b = 0
while 2**p <= n:
    if 2**p == n:
        b = 1
        print("YES")
    p+=1
if b== 0:
    print("NO")