n = input().split()
if(n[0] == "Manager"):
    print(f"Name: {n[1]}, Total: {(float(n[2]) + (float(n[2]) / 100 * float(n[3]))):.2f}")
elif(n[0] == "Developer"):
    print(f"Name: {n[1]}, Total: {(float(n[2]) + (float(n[3]) * 500)):.2f}")
else:
    print(f"Name: {n[1]}, Total: {float(n[2]):.2f}")