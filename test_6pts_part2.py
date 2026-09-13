from modules_6pts_part2 import m4, m5, m6

all_m = [m4, m5, m6]
errors = []

for mod in all_m:
    for q in mod["questions"]:
        sol = q["solution"]
        if len(sol) != 6:
            errors.append(f"Question {q['id']} has {len(sol)} bullets (expected 6)")
        for idx, (badge, text) in enumerate(sol):
            wc = len(text.split())
            if not (5 <= wc <= 7):
                errors.append(f"Question {q['id']} bullet {idx+1} has {wc} words: '{text}'")

if errors:
    print(f"FAILED with {len(errors)} errors:")
    for e in errors:
        print(" -", e)
else:
    print("ALL bullets in Part 2 (6 points) strictly passed 5-7 word count check!")
