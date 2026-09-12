import json
import html

from generate_all_modules import get_all_modules
from generate_modules_3_to_9 import get_modules_3_to_9
from assemble_master_portal import m4
from generate_modules_5_to_9 import get_modules_5_to_9
from generate_modules_6_to_9 import get_modules_6_to_9
from generate_modules_7_to_9 import get_modules_7_to_9

# Combine all 9 modules
all_modules = []
all_modules.extend(get_all_modules()) # m1, m2
all_modules.extend(get_modules_3_to_9()) # m3
all_modules.append(m4) # m4
all_modules.extend(get_modules_5_to_9()) # m5
all_modules.extend(get_modules_6_to_9()) # m6
all_modules.extend(get_modules_7_to_9()) # m7, m8, m9

print(f"Total Modules: {len(all_modules)}")
total_questions = sum(len(m["questions"]) for m in all_modules)
print(f"Total Questions: {total_questions}")

for i, m in enumerate(all_modules, 1):
    print(f"Module {i}: {m['title']} -> {len(m['questions'])} questions")

# Now let's generate the complete standalone HTML
badge_color_map = {
    "emerald": ("bg-emerald-50 text-emerald-700 border-emerald-200", "text-emerald-600"),
    "cyan": ("bg-cyan-50 text-cyan-700 border-cyan-200", "text-cyan-600"),
    "indigo": ("bg-indigo-50 text-indigo-700 border-indigo-200", "text-indigo-600"),
    "amber": ("bg-amber-50 text-amber-700 border-amber-200", "text-amber-600"),
    "purple": ("bg-purple-50 text-purple-700 border-purple-200", "text-purple-600"),
    "rose": ("bg-rose-50 text-rose-700 border-rose-200", "text-rose-600"),
    "teal": ("bg-teal-50 text-teal-700 border-teal-200", "text-teal-600"),
    "blue": ("bg-blue-50 text-blue-700 border-blue-200", "text-blue-600"),
    "violet": ("bg-purple-50 text-purple-700 border-purple-200", "text-purple-600")
}

# Serialize data for flashcards
flashcards_json = json.dumps(all_modules)

html_content = f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Staff Android Architect Interview Mastery Portal (108 Questions)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['"Plus Jakarta Sans"', 'sans-serif'],
                        mono: ['"JetBrains Mono"', 'monospace']
                    }}
                }}
            }}
        }}
    </script>
    <style>
        .custom-scrollbar::-webkit-scrollbar {{
            height: 6px;
            width: 6px;
        }}
        .custom-scrollbar::-webkit-scrollbar-track {{
            background: #f1f5f9;
            border-radius: 9999px;
        }}
        .custom-scrollbar::-webkit-scrollbar-thumb {{
            background: #cbd5e1;
            border-radius: 9999px;
        }}
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {{
            background: #94a3b8;
        }}
        .keyword-focus .bullet-text {{
            opacity: 0.35;
            transition: opacity 0.2s ease;
        }}
        .keyword-focus .keyword-tag {{
            transform: scale(1.05);
            box-shadow: 0 0 0 2px #f59e0b;
        }}
    </style>
</head>
<body class="bg-slate-50 text-slate-900 font-sans antialiased min-h-screen selection:bg-amber-100 selection:text-amber-900">

    <!-- Top Header -->
    <header class="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 flex items-center justify-center text-white shadow-md shadow-emerald-600/20 flex-shrink-0">
                    <svg class="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M17.523 15.3414c-.5511 0-.9993-.4486-.9993-.9997s.4482-.9993.9993-.9993c.551 0 .9993.4482.9993.9993.0001.5511-.4483.9997-.9993.9997m-11.046 0c-.5511 0-.9993-.4486-.9993-.9997s.4482-.9993.9993-.9993c.5511 0 .9993.4482.9993.9993 0 .5511-.4482.9997-.9993.9997m11.4045-6.02l1.9973-3.4592a.416.416 0 00-.1521-.5676.416.416 0 00-.5676.1521l-2.0223 3.503C15.5902 8.4111 13.8533 8 12 8s-3.5902.4111-5.1367.9497L4.841 5.4467a.4161.4161 0 00-.5677-.1521.4157.4157 0 00-.152 5676l1.9972 3.4592C2.6889 11.1867.3432 14.6589 0 18.8h24c-.3432-4.1411-2.6889-7.6133-6.1185-9.4786"/>
                    </svg>
                </div>
                <div>
                    <h1 class="text-lg font-bold text-slate-900 tracking-tight flex items-center gap-2">
                        Staff Android Architect
                        <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 border border-slate-200">9+ Years</span>
                        <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-300">108 Questions</span>
                    </h1>
                    <p class="text-xs text-slate-500">Executive Interview Cadence & Architectural Mastery Portal</p>
                </div>
            </div>

            <!-- Global Actions -->
            <div class="flex items-center gap-2 flex-wrap">
                <button onclick="toggleKeywordFocus()" id="keywordFocusBtn" class="px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition border border-slate-200 flex items-center gap-1.5">
                    <span class="w-2 h-2 rounded-full bg-amber-500"></span>
                    <span>Keyword Focus</span>
                </button>
                <button onclick="openSpeedDrill()" class="px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm transition flex items-center gap-1.5">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                    <span>Speed Drill (Space)</span>
                </button>
                <button onclick="resetAllProgress()" class="px-2.5 py-1.5 text-xs font-medium rounded-lg bg-slate-100 hover:bg-red-50 hover:text-red-600 text-slate-600 transition border border-slate-200">
                    Reset
                </button>
            </div>
        </div>

        <!-- Horizontal Mobile Navigation Slider -->
        <div class="border-t border-slate-200 bg-slate-50/80">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2 overflow-x-auto custom-scrollbar flex items-center gap-2 whitespace-nowrap">
                <span class="text-xs font-bold uppercase tracking-wider text-slate-400 mr-1 flex-shrink-0">Modules:</span>
"""

# Add horizontal module buttons
for i, m in enumerate(all_modules, 1):
    html_content += f"""
                <a href="#{m['id']}" class="px-3 py-1 text-xs font-semibold rounded-full bg-white hover:bg-slate-200 text-slate-700 border border-slate-200 shadow-2xs transition flex-shrink-0 flex items-center gap-1.5">
                    <span class="w-2 h-2 rounded-full {badge_color_map[m['color']][0].split()[0]}"></span>
                    <span>M{i}: {m['title'].split(':')[1].split('&')[0].strip()}</span>
                    <span class="text-slate-400 text-[10px]">12</span>
                </a>"""

html_content += f"""
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        <!-- Search and Global Stats Bar -->
        <div class="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm mb-8 flex flex-col md:flex-row items-center justify-between gap-4">
            <div class="relative w-full md:w-96">
                <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
                </div>
                <input type="text" id="searchInput" oninput="filterQuestions()" placeholder="Search 108 questions, keywords, APIs..." class="w-full pl-10 pr-4 py-2 text-sm bg-slate-50 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition">
            </div>

            <div class="flex items-center gap-6 w-full md:w-auto justify-between md:justify-end">
                <div>
                    <div class="text-xs text-slate-500 font-medium">Mastery Progress</div>
                    <div class="text-base font-bold text-slate-900"><span id="masteredCount">0</span> / 108 <span class="text-xs text-emerald-600 font-semibold">(<span id="masteredPercent">0</span>%)</span></div>
                </div>
                <div class="w-32 bg-slate-100 rounded-full h-2.5 overflow-hidden border border-slate-200">
                    <div id="masteryProgressBar" class="bg-emerald-500 h-full rounded-full transition-all duration-300" style="width: 0%"></div>
                </div>
            </div>
        </div>

        <!-- Question Modules -->
        <div class="space-y-12">
"""

# Render all 9 modules and 108 questions
for mod_idx, mod in enumerate(all_modules, 1):
    badge_style = badge_color_map[mod['color']][0]
    text_color = badge_color_map[mod['color']][1]
    
    html_content += f"""
            <!-- Module {mod_idx} -->
            <section id="{mod['id']}" class="scroll-mt-28">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200 mb-6 gap-2">
                    <div>
                        <div class="flex items-center gap-2 mb-1">
                            <span class="text-xs font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full border {badge_style}">
                                {mod['badge']} Pillar
                            </span>
                            <span class="text-xs font-semibold text-slate-500">12 Architectural Scenarios</span>
                        </div>
                        <h2 class="text-2xl font-extrabold text-slate-900 tracking-tight">{mod['title']}</h2>
                        <p class="text-sm text-slate-600 mt-0.5">{mod['summary']}</p>
                    </div>
                </div>

                <div class="grid grid-cols-1 gap-6">
    """
    
    for q in mod['questions']:
        code_block = ""
        if q.get('code'):
            escaped_code = html.escape(q['code'])
            code_block = f"""
                        <div class="mt-4 rounded-xl overflow-hidden border border-slate-200 bg-slate-900 shadow-inner">
                            <div class="px-4 py-2 bg-slate-800/80 border-b border-slate-700/60 flex items-center justify-between">
                                <span class="text-xs font-mono text-slate-400">Production Implementation</span>
                                <button onclick="copyCode(this)" data-code="{escaped_code}" class="text-[11px] font-mono text-slate-400 hover:text-white transition flex items-center gap-1">
                                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
                                    <span>Copy</span>
                                </button>
                            </div>
                            <pre class="p-4 text-xs font-mono text-emerald-300 overflow-x-auto custom-scrollbar leading-relaxed"><code>{escaped_code}</code></pre>
                        </div>
            """
        
        # Build solution bullets
        bullets_html = ""
        tts_text_parts = []
        for badge, text in q['solution']:
            tts_text_parts.append(f"{badge}. {text}")
            bullets_html += f"""
                                <li class="flex items-start gap-3">
                                    <span class="keyword-tag inline-block mt-0.5 px-2 py-0.5 rounded text-[11px] font-extrabold tracking-wide uppercase bg-amber-100 text-amber-900 border border-amber-300/80 flex-shrink-0 transition-transform">
                                        {badge}
                                    </span>
                                    <span class="bullet-text text-base text-slate-700 leading-snug">{text}</span>
                                </li>
            """
        
        full_tts_escaped = html.escape(" ".join(tts_text_parts))
        
        metric_html = ""
        if q.get('metric'):
            metric_html = f"""
                        <div class="mt-4 px-3.5 py-2.5 rounded-xl bg-slate-100 border border-slate-200 flex items-center gap-2 text-xs font-semibold text-slate-700">
                            <span class="text-emerald-600 font-bold">PROVEN IMPACT:</span>
                            <span>{q['metric']}</span>
                        </div>
            """

        html_content += f"""
                    <!-- Question Card {q['id']} -->
                    <article id="card-{q['id']}" class="question-card bg-white rounded-2xl border border-slate-200/90 p-6 shadow-sm hover:shadow-md transition-all">
                        <div class="flex items-start justify-between gap-4">
                            <div class="flex-1">
                                <h3 class="text-lg sm:text-xl font-bold text-slate-900 tracking-tight leading-snug">{q['title']}</h3>
                                <p class="text-xs font-medium text-red-600 mt-1 flex items-center gap-1.5">
                                    <svg class="w-3.5 h-3.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
                                    <span>Problem: {q['problem']}</span>
                                </p>
                            </div>

                            <div class="flex items-center gap-2 flex-shrink-0">
                                <!-- Master Checkbox -->
                                <label class="flex items-center gap-1.5 cursor-pointer text-xs font-semibold text-slate-500 hover:text-slate-800 select-none">
                                    <input type="checkbox" id="check-{q['id']}" onchange="toggleMastery('{q['id']}')" class="w-4 h-4 rounded border-slate-300 text-emerald-600 focus:ring-emerald-500 cursor-pointer">
                                    <span class="hidden sm:inline">Mastered</span>
                                </label>
                            </div>
                        </div>

                        <!-- 5-7 Word Structured Bullet Cadence -->
                        <div class="mt-5">
                            <div class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Executive Architectural Answer:</div>
                            <ul class="space-y-2.5">
                                {bullets_html}
                            </ul>
                        </div>

                        {code_block}
                        {metric_html}

                        <!-- Action Toolbar -->
                        <div class="mt-5 pt-4 border-t border-slate-100 flex flex-wrap items-center justify-between gap-2">
                            <div class="flex items-center gap-2">
                                <button onclick="startBreathTimer(this)" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition flex items-center gap-1.5 border border-slate-200">
                                    <svg class="w-3.5 h-3.5 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                                    <span class="timer-label">3s Breath Chime</span>
                                </button>
                                <button onclick="readAloud(this, '{full_tts_escaped}')" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition flex items-center gap-1.5 border border-slate-200">
                                    <svg class="w-3.5 h-3.5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/></svg>
                                    <span>TTS Cadence</span>
                                </button>
                            </div>

                            <span class="text-[11px] font-mono text-slate-400">{mod['badge']} • {q['id'].upper()}</span>
                        </div>
                    </article>
        """

    html_content += """
                </div>
            </section>
    """

html_content += f"""
        </div>
    </main>

    <!-- Speed Drill Flashcard Modal -->
    <div id="flashcardModal" class="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm hidden flex items-center justify-center p-4">
        <div class="bg-white rounded-3xl border border-slate-200 shadow-2xl max-w-2xl w-full p-6 sm:p-8 flex flex-col relative max-h-[90vh]">
            <button onclick="closeSpeedDrill()" class="absolute top-4 right-4 p-2 rounded-full text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>

            <div class="flex items-center justify-between pb-3 border-b border-slate-100">
                <span id="cardModuleBadge" class="text-xs font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200">Module 1</span>
                <span class="text-xs font-semibold text-slate-400">Card <span id="cardCurrentIndex">1</span> of 108</span>
            </div>

            <!-- Card Content (Click to flip) -->
            <div id="flashcardBody" onclick="flipSpeedCard()" class="my-6 p-6 rounded-2xl bg-slate-50 border border-slate-200 cursor-pointer min-h-[220px] flex flex-col justify-center transition-all hover:bg-slate-100/70 select-none">
                <div id="flashcardSidePrompt" class="text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-2">QUESTION (TAP / SPACE TO REVEAL ANSWER)</div>
                <div id="flashcardContent" class="text-xl font-bold text-slate-900 leading-snug">Loading question...</div>
            </div>

            <!-- Navigation Controls -->
            <div class="flex items-center justify-between pt-2">
                <button onclick="prevSpeedCard()" class="px-4 py-2 text-xs font-bold rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 transition">
                    ← Previous (Left)
                </button>
                <button onclick="flipSpeedCard()" class="px-5 py-2 text-xs font-bold rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white shadow transition">
                    Flip (Space)
                </button>
                <button onclick="nextSpeedCard()" class="px-4 py-2 text-xs font-bold rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 transition">
                    Next (Right) →
                </button>
            </div>
        </div>
    </div>

    <!-- Floating Back to Top Button -->
    <button onclick="window.scrollTo({{ top: 0, behavior: 'smooth' }})" class="fixed bottom-6 right-6 w-11 h-11 rounded-full bg-white border border-slate-200 text-slate-600 hover:text-slate-900 shadow-lg flex items-center justify-center transition hover:scale-105 z-30">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/></svg>
    </button>

    <!-- Interactive Scripts -->
    <script>
        const portalData = {flashcards_json};
        let flatQuestions = [];
        portalData.forEach(m => {{
            m.questions.forEach(q => {{
                flatQuestions.push({{ ...q, moduleTitle: m.title, moduleBadge: m.badge }});
            }});
        }});

        let currentCardIndex = 0;
        let isCardFlipped = false;

        // Sound Synthesizer Chime
        function playChime() {{
            try {{
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(587.33, audioCtx.currentTime); // D5 note
                osc.frequency.exponentialRampToValueAtTime(880, audioCtx.currentTime + 0.15); // A5 note
                gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.6);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.6);
            }} catch(e) {{
                console.log(e);
            }}
        }}

        function startBreathTimer(btn) {{
            const label = btn.querySelector('.timer-label');
            let timeLeft = 3;
            btn.classList.add('bg-amber-100', 'text-amber-800', 'border-amber-300');
            label.innerText = `Inhale... ${{timeLeft}}s`;
            
            const interval = setInterval(() => {{
                timeLeft--;
                if (timeLeft > 0) {{
                    label.innerText = `Steady... ${{timeLeft}}s`;
                }} else {{
                    clearInterval(interval);
                    playChime();
                    label.innerText = `Speak with conviction!`;
                    setTimeout(() => {{
                        btn.classList.remove('bg-amber-100', 'text-amber-800', 'border-amber-300');
                        label.innerText = `3s Breath Chime`;
                    }}, 2000);
                }}
            }}, 1000);
        }}

        function readAloud(btn, text) {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 0.95; // Executive interview speaking cadence
                utterance.pitch = 1.0;
                window.speechSynthesis.speak(utterance);
            }} else {{
                alert("Speech synthesis is not supported on your browser.");
            }}
        }}

        function copyCode(btn) {{
            const code = btn.getAttribute('data-code');
            navigator.clipboard.writeText(code).then(() => {{
                const span = btn.querySelector('span');
                const orig = span.innerText;
                span.innerText = 'Copied!';
                setTimeout(() => span.innerText = orig, 1500);
            }});
        }}

        function toggleKeywordFocus() {{
            document.body.classList.toggle('keyword-focus');
            const btn = document.getElementById('keywordFocusBtn');
            btn.classList.toggle('bg-amber-100');
            btn.classList.toggle('text-amber-900');
            btn.classList.toggle('border-amber-300');
        }}

        // Speed Drill Flashcards
        function openSpeedDrill() {{
            document.getElementById('flashcardModal').classList.remove('hidden');
            currentCardIndex = 0;
            isCardFlipped = false;
            updateSpeedCard();
        }}

        function closeSpeedDrill() {{
            document.getElementById('flashcardModal').classList.add('hidden');
        }}

        function updateSpeedCard() {{
            const card = flatQuestions[currentCardIndex];
            document.getElementById('cardModuleBadge').innerText = `${{card.moduleBadge}} • ${{card.moduleTitle.split(':')[1] || ''}}`;
            document.getElementById('cardCurrentIndex').innerText = currentCardIndex + 1;
            const content = document.getElementById('flashcardContent');
            const prompt = document.getElementById('flashcardSidePrompt');
            
            if (!isCardFlipped) {{
                prompt.innerText = "QUESTION (TAP / SPACE TO REVEAL ANSWER)";
                content.innerHTML = `<div class="text-xl font-bold text-slate-900">${{card.title}}</div><div class="text-xs font-medium text-red-600 mt-2">Problem: ${{card.problem}}</div>`;
            }} else {{
                prompt.innerText = "5-7 WORD EXECUTIVE ANSWER";
                let bullets = card.solution.map(s => `<li class="flex items-start gap-2 mb-1.5"><span class="px-1.5 py-0.5 rounded text-[10px] font-extrabold uppercase bg-amber-100 text-amber-900 border border-amber-300">${{s[0]}}</span><span class="text-sm font-medium text-slate-800">${{s[1]}}</span></li>`).join('');
                content.innerHTML = `<ul class="text-left space-y-1">${{bullets}}</ul>`;
            }}
        }}

        function flipSpeedCard() {{
            isCardFlipped = !isCardFlipped;
            updateSpeedCard();
        }}

        function nextSpeedCard() {{
            if (currentCardIndex < flatQuestions.length - 1) {{
                currentCardIndex++;
                isCardFlipped = false;
                updateSpeedCard();
            }}
        }}

        function prevSpeedCard() {{
            if (currentCardIndex > 0) {{
                currentCardIndex--;
                isCardFlipped = false;
                updateSpeedCard();
            }}
        }}

        window.addEventListener('keydown', (e) => {{
            const modal = document.getElementById('flashcardModal');
            if (!modal.classList.contains('hidden')) {{
                if (e.code === 'Space') {{
                    e.preventDefault();
                    flipSpeedCard();
                }} else if (e.code === 'ArrowRight') {{
                    nextSpeedCard();
                }} else if (e.code === 'ArrowLeft') {{
                    prevSpeedCard();
                }} else if (e.code === 'Escape') {{
                    closeSpeedDrill();
                }}
            }}
        }});

        // Mastery Checkbox & Persistence
        function toggleMastery(qid) {{
            const cb = document.getElementById(`check-${{qid}}`);
            localStorage.setItem(`mastery_${{qid}}`, cb.checked ? 'true' : 'false');
            updateMasteryStats();
        }}

        function updateMasteryStats() {{
            let count = 0;
            flatQuestions.forEach(q => {{
                if (localStorage.getItem(`mastery_${{q.id}}`) === 'true') {{
                    count++;
                    const cb = document.getElementById(`check-${{q.id}}`);
                    if (cb) cb.checked = true;
                }}
            }});
            document.getElementById('masteredCount').innerText = count;
            const pct = Math.round((count / flatQuestions.length) * 100);
            document.getElementById('masteredPercent').innerText = pct;
            document.getElementById('masteryProgressBar').style.width = `${{pct}}%`;
        }}

        function resetAllProgress() {{
            if (confirm("Reset all mastered question checkboxes?")) {{
                flatQuestions.forEach(q => {{
                    localStorage.removeItem(`mastery_${{q.id}}`);
                    const cb = document.getElementById(`check-${{q.id}}`);
                    if (cb) cb.checked = false;
                }});
                updateMasteryStats();
            }}
        }}

        function filterQuestions() {{
            const query = document.getElementById('searchInput').value.toLowerCase().trim();
            flatQuestions.forEach(q => {{
                const card = document.getElementById(`card-${{q.id}}`);
                if (!card) return;
                const match = q.title.toLowerCase().includes(query) ||
                              q.problem.toLowerCase().includes(query) ||
                              q.solution.some(s => s[0].toLowerCase().includes(query) || s[1].toLowerCase().includes(query));
                card.style.display = match ? 'block' : 'none';
            }});
        }}

        // Init
        document.addEventListener('DOMContentLoaded', () => {{
            updateMasteryStats();
        }});
    </script>
</body>
</html>
"""

output_path = "/Users/prajapatichintankumar/.gemini/antigravity/scratch/android-interview-portal/index.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully compiled {output_path} with {total_questions} questions!")
