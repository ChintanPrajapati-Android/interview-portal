with open("modules_part1.py", "r") as f:
    c = f.read()

c = c.replace('"I bundle state into one immutable data class."', '"I bundle state into one immutable class."')
c = c.replace('"I drop processing from 30 to 10 FPS."', '"I drop frame rate to 10 FPS."')
c = c.replace('"I encrypt binary bytes before transmitting over BLE."', '"I encrypt data bytes before BLE transmission."')

with open("modules_part1.py", "w") as f:
    f.write(c)

print("Part 1 fixed.")
