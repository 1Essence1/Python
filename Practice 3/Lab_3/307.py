import math
x1, y1 = map(int, input().split())
new_x, new_y = map(int, input().split())
x2, y2 = map(int, input().split())
print(f"({x1}, {y1})")
x1, y1 = new_x, new_y
print(f"({x1}, {y1})")
distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
print(f"{distance:.2f}")
