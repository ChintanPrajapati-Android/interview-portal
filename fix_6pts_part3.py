with open("modules_6pts_part3.py", "r") as f:
    c = f.read()

c = c.replace('"Full mode inlines code and removes dead branches."', '"Full mode eliminates dead code and inlines."')

with open("modules_6pts_part3.py", "w") as f:
    f.write(c)

print("Part 3 fixed.")
