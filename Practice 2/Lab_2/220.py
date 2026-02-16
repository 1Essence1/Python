n = int(input())
a = {}
for i in range(n):
    parts = input().split()
    if parts[0] == "set":
        a[parts[1]] = parts[2]
    else:
        if parts[1] in a:
            print(a[parts[1]])
        else:
            print(f"KE: no key {parts[1]} found in the document")