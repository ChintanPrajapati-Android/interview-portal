with open("modules_6pts_part2.py", "r") as f:
    c2 = f.read()
c2 = c2.replace('"App works completely without active internet connection."', '"App works fully without active internet connection."')
c2 = c2.replace('"Eliminates string route typo bugs completely."', '"Eliminates string route typo bugs for good."')
with open("modules_6pts_part2.py", "w") as f:
    f.write(c2)

with open("modules_6pts_part3.py", "r") as f:
    c3 = f.read()
c3 = c3.replace('"Action: Removed all Thread.sleep calls completely."', '"Action: Removed all Thread.sleep calls from tests."')
with open("modules_6pts_part3.py", "w") as f:
    f.write(c3)

print("Part 2 & 3 banned words fixed.")
