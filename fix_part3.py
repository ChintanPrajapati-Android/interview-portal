with open("modules_part3.py", "r") as f:
    c = f.read()

c = c.replace('"Stops man-in-the-middle network attacks."', '"Stops man-in-the-middle network attacks completely."')
c = c.replace('"Stops unauthorized inter-app communication."', '"Stops unauthorized inter-app communication attacks completely."')
c = c.replace('"BIOMETRIC_STRONG enforces hardware-backed fingerprint."', '"BIOMETRIC_STRONG enforces hardware-backed biometric security."')

with open("modules_part3.py", "w") as f:
    f.write(c)

print("Part 3 fixed.")
