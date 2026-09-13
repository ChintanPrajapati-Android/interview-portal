with open("modules_part1.py", "r") as f:
    c1 = f.read()
c1 = c1.replace('"Stops man-in-the-middle sniffing attacks completely."', '"Blocks man-in-the-middle packet sniffing attacks."')
with open("modules_part1.py", "w") as f:
    f.write(c1)

with open("modules_part2.py", "r") as f:
    c2 = f.read()
c2 = c2.replace('"Eliminates bad behavior battery warnings completely."', '"Eliminates bad behavior battery warnings on Play."')
with open("modules_part2.py", "w") as f:
    f.write(c2)

with open("modules_part3.py", "r") as f:
    c3 = f.read()
c3 = c3.replace('"Stops man-in-the-middle network attacks completely."', '"Blocks man-in-the-middle network proxy attacks."')
c3 = c3.replace('"Stops unauthorized inter-app communication attacks completely."', '"Blocks unauthorized inter-app IPC attacks."')
with open("modules_part3.py", "w") as f:
    f.write(c3)

print("Banned words replaced.")
