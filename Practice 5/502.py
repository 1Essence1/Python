import re

txt = input()
s = input()
if re.search(s , txt):
    print("Yes")
else:
    print("No")