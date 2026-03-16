import re
txt = input()
print(*re.findall('[0-9]', txt), sep=" ")