def square(a , n):
    for i in range(a , n+1):
        yield i ** 2
a , n = map(int , input("").split())
for i in square(a , n):
    print(i)