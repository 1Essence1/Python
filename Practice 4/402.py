def square(n):
    for i in range(n+1):
        if i % 2 == 0:
            yield i
n = int(input(""))
for i in square(n):
    if i != n and i != n-1:
        print(i , end=",")
    else:
        print(i)