n = int(input())
a = list(map(int, input().split()))
q = int(input())
for i in range(q):
    r = input().split()
    if r[0] == "abs":
        for j in range(n):
            a[j] = abs(a[j])
    elif r[0] == "add":
        for j in range(n):
            a[j] += int(r[1])
    elif r[0] == "multiply":
        for j in range(n):
            a[j] *= int(r[1])
    elif r[0] == "power":
        for j in range(n):
            a[j] **= int(r[1])
print(*a)