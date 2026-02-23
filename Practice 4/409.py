def pow(n):
    for i in range(n + 1):
        yield 2 ** i
n = int(input(""))
a = list(pow(n))
print(*a)