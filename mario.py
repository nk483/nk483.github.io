from cs50 import get_int
while True:
    height = get_int("height: ")
    if height > 0:
        break
for i in range(height):
    for j in range(height - i - 1, 0, -1):
        print(" ", end="")
    for k in range(i+1):
        print("#", end="")
    print(" ", end="")
    for k in range(i+1):
        print("#", end="")
    for j in range(height - i, 0, -1):
        print(" ", end="")
    print("")
