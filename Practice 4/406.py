def square(n):
    a = list(map(int, range(n + 1)))
    for i in range(n):
        if i == 0:
            a[i] = 0
        elif i == 1:        
            a[i] = 1
        else:
            a[i] = a[i-1] + a[i-2]
    for i in a:
        yield i
n = int(input(""))
cnt = 0
if n != 0:
    for i in square(n):
        cnt+=1
        if cnt != n:
            print(i , end=",")
        else:
            print(i)
            break