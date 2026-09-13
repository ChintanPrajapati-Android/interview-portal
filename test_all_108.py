from modules_part1 import m1, m2, m3
from modules_part2 import m4, m5, m6
from modules_part3 import m7, m8, m9

all_modules = [m1, m2, m3, m4, m5, m6, m7, m8, m9]

banned_words = [
    "effectively", "gracefully", "completely", "robustly", "imperative",
    "seamlessly", "throttle redundant query emissions", "mitigate", "paradigm", "facilitate"
]

print(f"Total Modules: {len(all_modules)}")
total_questions = sum(len(m["questions"]) for m in all_modules)
print(f"Total Questions: {total_questions}")

errors = []

for mod_idx, mod in enumerate(all_modules, 1):
    qs = mod["questions"]
    if len(qs) != 12:
        errors.append(f"Module {mod_idx} has {len(qs)} questions (expected 12)")
    for q in qs:
        sol = q["solution"]
        if not (3 <= len(sol) <= 4):
            errors.append(f"Question {q['id']} has {len(sol)} bullets (expected 3-4)")
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
    print("SUCCESS: All 9 modules, all 108 questions, all bullets (5-7 words, 3-4 bullets, 0 banned words) PASSED 100%!")
