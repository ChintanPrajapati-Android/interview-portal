from modules_6pts_part1 import m1, m2, m3
from modules_6pts_part2 import m4, m5, m6
from modules_6pts_part3 import m7, m8, m9

all_modules = [m1, m2, m3, m4, m5, m6, m7, m8, m9]

banned_words = [
    "effectively", "gracefully", "completely", "robustly", "imperative",
    "seamlessly", "throttle redundant query emissions", "mitigate", "paradigm", "facilitate"
]

print(f"Total Modules: {len(all_modules)}")
total_questions = sum(len(m["questions"]) for m in all_modules)
print(f"Total Questions: {total_questions}")
total_bullets = sum(sum(len(q["solution"]) for q in m["questions"]) for m in all_modules)
print(f"Total Bullets: {total_bullets}")

errors = []

for mod_idx, mod in enumerate(all_modules, 1):
    qs = mod["questions"]
    if len(qs) != 12:
        errors.append(f"Module {mod_idx} has {len(qs)} questions (expected 12)")
    for q in qs:
        sol = q["solution"]
        if len(sol) != 6:
            errors.append(f"Question {q['id']} has {len(sol)} bullets (expected exactly 6)")
        for idx, (badge, text) in enumerate(sol):
            words = text.split()
            wc = len(words)
            if not (5 <= wc <= 7):
                errors.append(f"Question {q['id']} bullet {idx+1} has {wc} words: '{text}'")
            for bw in banned_words:
                if bw.lower() in text.lower():
                    errors.append(f"Question {q['id']} bullet {idx+1} contains banned word '{bw}': '{text}'")

if errors:
    print(f"FAILED with {len(errors)} issues:")
    for e in errors:
        print(" -", e)
else:
    print("SUCCESS: 9 modules, 108 questions, 648 bullets (exactly 6 bullets per question, 5-7 words each, 0 banned words) PASSED 100%!")
