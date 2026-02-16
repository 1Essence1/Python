n = int(input())
a = list(map(int , input().split()))
b = list()
for i in a:
    if i in b:
        print("NO")
    else:
        print("YES")
        b.append(i)