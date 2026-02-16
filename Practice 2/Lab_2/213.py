from math import sqrt


n = int(input())
b = 0

for i in range(2 ,int(sqrt(n)) + 1):
    if n % i == 0:
        b = 1
        break
if b == 1:
    print("No")
else:
    print("Yes")