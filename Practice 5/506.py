import re

txt = input()

if re.search(r'[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+', txt):
    print(re.search(r'[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+', txt).group())

else:
    print("No email")