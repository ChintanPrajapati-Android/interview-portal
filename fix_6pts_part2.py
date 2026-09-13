with open("modules_6pts_part2.py", "r") as f:
    c = f.read()

c = c.replace('"cachedIn viewModelScope caches the paging stream in memory."', '"cachedIn viewModelScope caches paging stream in memory."')
c = c.replace('"Automatically parses incoming deep links into typed models."', '"Parses incoming deep links into typed models."')
c = c.replace('"Parcelize data classes work with zero extra code."', '"Parcelize data classes work with zero boilerplate."')

with open("modules_6pts_part2.py", "w") as f:
    f.write(c)

print("Part 2 fixed.")
