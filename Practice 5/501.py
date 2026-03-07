import re

txt = input()

if re.match(r'^Hello$', txt):
    print("Yes")
else:
    print("No")