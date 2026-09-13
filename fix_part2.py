with open("modules_part2.py", "r") as f:
    c = f.read()

c = c.replace('"AndroidView embeds legacy views like MapView inside Compose."', '"AndroidView embeds legacy views inside Compose."')

with open("modules_part2.py", "w") as f:
    f.write(c)

print("Part 2 fixed.")
