# -*- coding: utf-8 -*-
import json
import html

from modules_6pts_part1 import m1, m2, m3
from modules_6pts_part2 import m4, m5, m6
from modules_6pts_part3 import m7, m8, m9
from module10_part1 import topics_1_to_25
from module10_part2 import topics_26_to_50
from make_m11 import m11_data

all_interview_modules = [m1, m2, m3, m4, m5, m6, m7, m8, m9]
all_topics = topics_1_to_25 + topics_26_to_50

print(f"Loaded {len(all_interview_modules)} Interview Modules (108 Qs)")
print(f"Loaded {len(all_topics)} Deep-Dive Topics for Module 10")
print(f"Loaded Module 11 with {len(m11_data['design_patterns'])} Design Patterns and 3 Deep Architecture blueprints")

badge_color_map = {
    "emerald": ("bg-emerald-50 dark:bg-emerald-950/50 text-emerald-700 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800", "text-emerald-600"),
    "cyan": ("bg-cyan-50 dark:bg-cyan-950/50 text-cyan-700 dark:text-cyan-300 border-cyan-200 dark:border-cyan-800", "text-cyan-600"),
    "indigo": ("bg-indigo-50 dark:bg-indigo-950/50 text-indigo-700 dark:text-indigo-300 border-indigo-200 dark:border-indigo-800", "text-indigo-600"),
    "amber": ("bg-amber-50 dark:bg-amber-950/50 text-amber-700 dark:text-amber-300 border-amber-200 dark:border-amber-800", "text-amber-600"),
    "purple": ("bg-purple-50 dark:bg-purple-950/50 text-purple-700 dark:text-purple-300 border-purple-200 dark:border-purple-800", "text-purple-600"),
    "rose": ("bg-rose-50 dark:bg-rose-950/50 text-rose-700 dark:text-rose-300 border-rose-200 dark:border-rose-800", "text-rose-600"),
    "teal": ("bg-teal-50 dark:bg-teal-950/50 text-teal-700 dark:text-teal-300 border-teal-200 dark:border-teal-800", "text-teal-600"),
    "blue": ("bg-blue-50 dark:bg-blue-950/50 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-800", "text-blue-600"),
    "violet": ("bg-purple-50 dark:bg-purple-950/50 text-purple-700 dark:text-purple-300 border-purple-200 dark:border-purple-800", "text-purple-600"),
    "orange": ("bg-orange-50 dark:bg-orange-950/50 text-orange-700 dark:text-orange-300 border-orange-200 dark:border-orange-800", "text-orange-600")
}

flashcards_json = json.dumps(all_interview_modules)
topics_json = json.dumps(all_topics)
m11_json = json.dumps(m11_data)

html_content = f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Staff Android Architect Master Portal (108 Questions + 50 Deep Dive Topics + Architecture & Patterns)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {{
            darkMode: 'class',
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
        .dark .custom-scrollbar::-webkit-scrollbar-track {{
            background: #1e293b;
        }}
        .custom-scrollbar::-webkit-scrollbar-thumb {{
            background: #cbd5e1;
            border-radius: 9999px;
        }}
        .dark .custom-scrollbar::-webkit-scrollbar-thumb {{
            background: #475569;
        }}
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {{
            background: #94a3b8;
        }}
        .keyword-focus .bullet-text {{
            opacity: 0.25;
            transition: opacity 0.2s ease;
        }}
        .keyword-focus .keyword-tag {{
            transform: scale(1.05);
            box-shadow: 0 0 0 2px #f59e0b;
        }}
        .ascii-box {{
            font-family: 'JetBrains Mono', monospace;
            line-height: 1.25;
            letter-spacing: -0.01em;
        }}
    </style>
</head>
<body class="bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 font-sans antialiased min-h-screen selection:bg-indigo-100 dark:selection:bg-indigo-900/40 selection:text-indigo-900 dark:selection:text-indigo-200 transition-colors duration-200">

    <!-- Top Sticky Header -->
    <header class="sticky top-0 z-40 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 shadow-sm transition-colors duration-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-500 flex items-center justify-center text-white shadow-md shadow-indigo-600/20 flex-shrink-0">
                    <svg class="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                    </svg>
                </div>
                <div>
                    <h1 class="text-lg font-bold text-slate-900 dark:text-white tracking-tight flex items-center gap-2 flex-wrap">
                        Staff Android Architect
                        <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700">9+ Years</span>
                        <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800">108 Qs</span>
                        <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-orange-100 dark:bg-orange-950 text-orange-800 dark:text-orange-300 border border-orange-300 dark:border-orange-800">50 Topics</span>
                        <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-indigo-100 dark:bg-indigo-950 text-indigo-800 dark:text-indigo-300 border border-indigo-300 dark:border-indigo-800">Arch & 12 Patterns</span>
                    </h1>
                    <p class="text-xs text-slate-500 dark:text-slate-400">Executive 6-Point Cadence • Kotlin Deep Dive • MVVM + Clean • MVI • Multi-Module • 12 Design Patterns</p>
                </div>
            </div>

            <!-- Global Actions & Tools -->
            <div class="flex items-center gap-2 flex-wrap">
                <button onclick="toggleDarkMode()" id="darkModeBtn" class="p-2 text-xs font-medium rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 transition border border-slate-200 dark:border-slate-700" title="Toggle Theme">
                    <svg id="sunIcon" class="w-4 h-4 hidden dark:block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
                    <svg id="moonIcon" class="w-4 h-4 block dark:hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/></svg>
                </button>
                <button onclick="toggleKeywordFocus()" id="keywordFocusBtn" class="px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 transition border border-slate-200 dark:border-slate-700 flex items-center gap-1.5">
                    <span class="w-2 h-2 rounded-full bg-amber-500"></span>
                    <span>Keyword Focus</span>
                </button>
                <button onclick="openSpeedDrill()" class="px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm transition flex items-center gap-1.5">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                    <span>Speed Drill (Space)</span>
                </button>
                <button onclick="resetAllProgress()" class="px-2.5 py-1.5 text-xs font-medium rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-red-50 dark:hover:bg-red-950/50 hover:text-red-600 dark:hover:text-red-400 text-slate-600 dark:text-slate-400 transition border border-slate-200 dark:border-slate-700">
                    Reset
                </button>
            </div>
        </div>

        <!-- Horizontal Swipeable Mobile Module Navigation -->
        <div class="border-t border-slate-200 dark:border-slate-800 bg-slate-50/80 dark:bg-slate-900/80">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2 overflow-x-auto custom-scrollbar flex items-center gap-2 whitespace-nowrap">
                <span class="text-xs font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 mr-1 flex-shrink-0">Jump To:</span>
"""

# Render interview module buttons
for i, m in enumerate(all_interview_modules, 1):
    html_content += f"""
                <a href="#{m['id']}" class="px-3 py-1 text-xs font-semibold rounded-full bg-white dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 shadow-2xs transition flex-shrink-0 flex items-center gap-1.5">
                    <span class="w-2 h-2 rounded-full {badge_color_map[m['color']][0].split()[0]}"></span>
                    <span>M{i}: {m['title'].split(':')[1].split('&')[0].strip()}</span>
                    <span class="text-slate-400 dark:text-slate-500 text-[10px]">12</span>
                </a>"""

# Add Module 10 Deep Dive Topic Navigation Pill
html_content += f"""
                <a href="#module-10" class="px-3.5 py-1 text-xs font-bold rounded-full bg-orange-500 hover:bg-orange-600 text-white shadow-sm transition flex-shrink-0 flex items-center gap-1.5">
                    <span class="w-2 h-2 rounded-full bg-white"></span>
                    <span>M10: Kotlin Deep Dive</span>
                    <span class="bg-orange-600 text-white px-1.5 py-0.2 rounded-full text-[10px]">50 Topics</span>
                </a>"""

# Add Module 11 Architecture Navigation Pill
html_content += f"""
                <a href="#module-11" class="px-3.5 py-1 text-xs font-bold rounded-full bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm transition flex-shrink-0 flex items-center gap-1.5">
                    <span class="w-2 h-2 rounded-full bg-white animate-pulse"></span>
                    <span>M11: Architecture & Patterns</span>
                    <span class="bg-indigo-700 text-white px-1.5 py-0.2 rounded-full text-[10px]">MVVM • MVI • Modular • 12 DP</span>
                </a>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        <!-- Search and Mastery Stats Bar -->
        <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-5 shadow-sm mb-8 flex flex-col md:flex-row items-center justify-between gap-4 transition-colors duration-200">
            <div class="relative w-full md:w-96">
                <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
                </div>
                <input type="text" id="searchInput" oninput="filterAllContent()" placeholder="Search 108 questions, 50 topics & patterns..." class="w-full pl-10 pr-4 py-2 text-sm bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white rounded-xl border border-slate-200 dark:border-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition">
            </div>

            <div class="flex items-center gap-6 w-full md:w-auto justify-between md:justify-end">
                <div>
                    <div class="text-xs text-slate-500 dark:text-slate-400 font-medium">Interview Questions Mastery</div>
                    <div class="text-base font-bold text-slate-900 dark:text-white"><span id="masteredCount">0</span> / 108 <span class="text-xs text-emerald-600 dark:text-emerald-400 font-semibold">(<span id="masteredPercent">0</span>%)</span></div>
                </div>
                <div class="w-32 bg-slate-100 dark:bg-slate-800 rounded-full h-2.5 overflow-hidden border border-slate-200 dark:border-slate-700">
                    <div id="masteryProgressBar" class="bg-emerald-500 h-full rounded-full transition-all duration-300" style="width: 0%"></div>
                </div>
            </div>
        </div>

        <!-- Section 1: 9 Interview Modules (108 Questions) -->
        <div class="space-y-12">
"""

for mod_idx, mod in enumerate(all_interview_modules, 1):
    badge_style = badge_color_map[mod['color']][0]
    
    html_content += f"""
            <!-- Module {mod_idx} -->
            <section id="{mod['id']}" class="scroll-mt-28">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800 mb-6 gap-2">
                    <div>
                        <div class="flex items-center gap-2 mb-1">
                            <span class="text-xs font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full border {badge_style}">
                                {mod['badge']} Pillar
                            </span>
                            <span class="text-xs font-semibold text-slate-500 dark:text-slate-400">12 Questions • 6 Points Each</span>
                        </div>
                        <h2 class="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight">{mod['title']}</h2>
                        <p class="text-sm text-slate-600 dark:text-slate-400 mt-0.5">{mod['summary']}</p>
                    </div>
                </div>

                <div class="grid grid-cols-1 gap-6">
    """
    
    for q in mod['questions']:
        code_block = ""
        if q.get('code'):
            escaped_code = html.escape(q['code'])
            code_block = f"""
                        <div class="mt-4 rounded-xl overflow-hidden border border-slate-200 dark:border-slate-800 bg-slate-900 dark:bg-black shadow-inner">
                            <div class="px-4 py-2 bg-slate-800/80 dark:bg-slate-900/80 border-b border-slate-700/60 flex items-center justify-between">
                                <span class="text-xs font-mono text-slate-400">Production Kotlin/NDK Snippet</span>
                                <button onclick="copyCode(this)" data-code="{escaped_code}" class="text-[11px] font-mono text-slate-400 hover:text-white transition flex items-center gap-1">
                                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
                                    <span>Copy</span>
                                </button>
                            </div>
                            <pre class="p-4 text-xs font-mono text-emerald-300 overflow-x-auto custom-scrollbar leading-relaxed"><code>{escaped_code}</code></pre>
                        </div>
            """
        
        bullets_html = ""
        tts_text_parts = []
        for badge, text in q['solution']:
            tts_text_parts.append(f"{badge}. {text}")
            bullets_html += f"""
                                <li class="flex items-start gap-3">
                                    <span class="keyword-tag inline-block mt-0.5 px-2 py-0.5 rounded text-[11px] font-extrabold tracking-wide uppercase bg-amber-100 dark:bg-amber-950 text-amber-900 dark:text-amber-200 border border-amber-300 dark:border-amber-700/60 flex-shrink-0 transition-transform">
                                        {badge}
                                    </span>
                                    <span class="bullet-text text-base text-slate-700 dark:text-slate-200 leading-snug font-medium">{text}</span>
                                </li>
            """
        
        full_tts_escaped = html.escape(" ".join(tts_text_parts))
        
        metric_html = ""
        if q.get('metric'):
            metric_html = f"""
                        <div class="mt-4 px-3.5 py-2.5 rounded-xl bg-slate-100 dark:bg-slate-800/70 border border-slate-200 dark:border-slate-700/60 flex items-center gap-2 text-xs font-semibold text-slate-700 dark:text-slate-300">
                            <span class="text-emerald-600 dark:text-emerald-400 font-bold">PROVEN IMPACT:</span>
                            <span>{q['metric']}</span>
                        </div>
            """

        html_content += f"""
                    <!-- Question Card {q['id']} -->
                    <article id="card-{q['id']}" class="searchable-card bg-white dark:bg-slate-900 rounded-2xl border border-slate-200/90 dark:border-slate-800 p-6 shadow-sm hover:shadow-md transition-all">
                        <div class="flex items-start justify-between gap-4">
                            <div class="flex-1">
                                <h3 class="text-lg sm:text-xl font-bold text-slate-900 dark:text-white tracking-tight leading-snug">{q['title']}</h3>
                                <p class="text-xs font-medium text-red-600 dark:text-red-400 mt-1 flex items-center gap-1.5">
                                    <svg class="w-3.5 h-3.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
                                    <span>Problem: {q['problem']}</span>
                                </p>
                            </div>

                            <div class="flex items-center gap-2 flex-shrink-0">
                                <label class="flex items-center gap-1.5 cursor-pointer text-xs font-semibold text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200 select-none">
                                    <input type="checkbox" id="check-{q['id']}" onchange="toggleMastery('{q['id']}')" class="w-4 h-4 rounded border-slate-300 dark:border-slate-700 text-emerald-600 focus:ring-emerald-500 cursor-pointer">
                                    <span class="hidden sm:inline">Mastered</span>
                                </label>
                            </div>
                        </div>

                        <!-- Exactly 6 Bullets, Strictly 5-7 Words Plain Spoken Structure -->
                        <div class="mt-5">
                            <div class="text-xs font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-2">Executive 6-Point Cadence:</div>
                            <ul class="space-y-2.5">
                                {bullets_html}
                            </ul>
                        </div>

                        {code_block}
                        {metric_html}

                        <!-- Action Toolbar -->
                        <div class="mt-5 pt-4 border-t border-slate-100 dark:border-slate-800 flex flex-wrap items-center justify-between gap-2">
                            <div class="flex items-center gap-2">
                                <button onclick="startBreathTimer(this)" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 transition flex items-center gap-1.5 border border-slate-200 dark:border-slate-700">
                                    <svg class="w-3.5 h-3.5 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                                    <span class="timer-label">3s Breath Chime</span>
                                </button>
                                <button onclick="readAloud(this, '{full_tts_escaped}')" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 transition flex items-center gap-1.5 border border-slate-200 dark:border-slate-700">
                                    <svg class="w-3.5 h-3.5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/></svg>
                                    <span>TTS Cadence</span>
                                </button>
                            </div>

                            <span class="text-[11px] font-mono text-slate-400 dark:text-slate-500">{mod['badge']} • {q['id'].upper()}</span>
                        </div>
                    </article>
        """

    html_content += """
                </div>
            </section>
    """

# SECTION 2: MODULE 10 - 50 DEEP DIVE KOTLIN & ANDROID TOPICS
html_content += """
            <!-- MODULE 10: 50 DEEP DIVE TOPICS -->
            <section id="module-10" class="scroll-mt-28 pt-8 border-t-2 border-orange-500/30">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800 mb-8 gap-2">
                    <div>
                        <div class="flex items-center gap-2 mb-1">
                            <span class="text-xs font-bold uppercase tracking-wider px-3 py-1 rounded-full bg-orange-50 dark:bg-orange-950/50 text-orange-700 dark:text-orange-300 border border-orange-200 dark:border-orange-800">
                                Master Engineering Pillar • Reference Guide
                            </span>
                            <span class="text-xs font-semibold text-slate-500 dark:text-slate-400">50 Comprehensive Topics</span>
                        </div>
                        <h2 class="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">Module 10: Kotlin & Android Deep Dive Reference</h2>
                        <p class="text-sm text-slate-600 dark:text-slate-400 mt-1">Exhaustive architectural reference covering Kotlin language internals, Coroutines, Flow, Compose runtime, and Android framework systems with production examples.</p>
                    </div>
                </div>

                <div class="grid grid-cols-1 gap-8">
"""

# Render all 50 deep dive topics
for t in all_topics:
    escaped_code = html.escape(t['code'])
    html_content += f"""
                    <!-- Deep Dive Topic {t['number']}: {t['id']} -->
                    <article id="topic-{t['id']}" class="searchable-card bg-white dark:bg-slate-900 rounded-3xl border border-slate-200/90 dark:border-slate-800 p-6 sm:p-8 shadow-sm hover:shadow-md transition-all">
                        
                        <!-- Header -->
                        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-4 border-b border-slate-100 dark:border-slate-800">
                            <div class="flex items-center gap-2">
                                <span class="px-2.5 py-0.5 rounded-md text-xs font-mono font-bold bg-orange-100 dark:bg-orange-950 text-orange-800 dark:text-orange-300 border border-orange-300 dark:border-orange-800">
                                    TOPIC #{t['number']}
                                </span>
                                <span class="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">{t['category']}</span>
                            </div>
                            <button onclick="copyCode(this)" data-code="{escaped_code}" class="self-start sm:self-auto text-xs font-mono text-slate-500 hover:text-slate-900 dark:hover:text-white transition flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
                                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
                                <span>Copy Snippet</span>
                            </button>
                        </div>

                        <!-- Title -->
                        <h3 class="text-xl sm:text-2xl font-bold text-slate-900 dark:text-white mt-4 tracking-tight leading-snug">
                            {t['title']}
                        </h3>

                        <!-- Why & How Deep Dive Grid -->
                        <div class="mt-5 grid grid-cols-1 md:grid-cols-2 gap-5">
                            
                            <!-- Why (Problem & Value) -->
                            <div class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/60">
                                <div class="text-xs font-extrabold uppercase tracking-wider text-amber-600 dark:text-amber-400 flex items-center gap-1.5 mb-2">
                                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
                                    <span>Why It Matters (The Core Rationale)</span>
                                </div>
                                <p class="text-sm text-slate-700 dark:text-slate-300 leading-relaxed font-normal">
                                    {t['why']}
                                </p>
                            </div>

                            <!-- How (Deep Dive Mechanism) -->
                            <div class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/60">
                                <div class="text-xs font-extrabold uppercase tracking-wider text-indigo-600 dark:text-indigo-400 flex items-center gap-1.5 mb-2">
                                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"/></svg>
                                    <span>How It Works (Under The Hood)</span>
                                </div>
                                <p class="text-sm text-slate-700 dark:text-slate-300 leading-relaxed font-normal">
                                    {t['how']}
                                </p>
                            </div>
                        </div>

                        <!-- Code Example -->
                        <div class="mt-5 rounded-2xl overflow-hidden border border-slate-200 dark:border-slate-800 bg-slate-900 dark:bg-black shadow-inner">
                            <div class="px-4 py-2 bg-slate-800/80 dark:bg-slate-900/80 border-b border-slate-700/60 flex items-center justify-between">
                                <span class="text-xs font-mono text-slate-400">Production Kotlin Implementation</span>
                                <span class="text-[11px] font-mono text-emerald-400">Tested Pattern</span>
                            </div>
                            <pre class="p-4 text-xs font-mono text-emerald-300 overflow-x-auto custom-scrollbar leading-relaxed"><code>{escaped_code}</code></pre>
                        </div>

                        <!-- Golden Takeaway Banner -->
                        <div class="mt-4 px-4 py-3 rounded-2xl bg-orange-50 dark:bg-orange-950/40 border border-orange-200 dark:border-orange-800/60 flex items-start gap-2.5">
                            <div class="text-orange-600 dark:text-orange-400 mt-0.5 flex-shrink-0">
                                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
                            </div>
                            <div class="text-xs font-semibold text-orange-950 dark:text-orange-200 leading-snug">
                                <span class="font-bold uppercase tracking-wider text-orange-700 dark:text-orange-400">Architect Rule:</span> {t['takeaway']}
                            </div>
                        </div>

                    </article>
    """

html_content += """
                </div>
            </section>
"""

# =========================================================================
# SECTION 3: MODULE 11 - ARCHITECTURE & DESIGN PATTERNS MASTERCLASS
# =========================================================================
m11_mvvm = m11_data['mvvm_clean']
m11_mvi = m11_data['mvi_udf']
m11_mod = m11_data['modular_architecture']
m11_patterns = m11_data['design_patterns']

html_content += f"""
            <!-- MODULE 11: ARCHITECTURE & DESIGN PATTERNS MASTERCLASS -->
            <section id="module-11" class="scroll-mt-28 pt-8 border-t-2 border-indigo-500/30">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800 mb-8 gap-2">
                    <div>
                        <div class="flex items-center gap-2 mb-1">
                            <span class="text-xs font-bold uppercase tracking-wider px-3 py-1 rounded-full bg-indigo-50 dark:bg-indigo-950/50 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800">
                                Enterprise Architectural Pillar
                            </span>
                            <span class="text-xs font-semibold text-slate-500 dark:text-slate-400">MVVM • MVI • Modularization • 12 Design Patterns</span>
                        </div>
                        <h2 class="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">{m11_data['title']}</h2>
                        <p class="text-sm text-slate-600 dark:text-slate-400 mt-1">{m11_data['summary']}</p>
                    </div>
                </div>

                <!-- Sub-Navigation Shortcuts for Module 11 -->
                <div class="mb-8 flex flex-wrap gap-2.5">
                    <a href="#m11-mvvm-clean" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 hover:bg-indigo-50 dark:hover:bg-indigo-950 text-slate-800 dark:text-slate-200 transition">
                        1. MVVM + Clean Architecture
                    </a>
                    <a href="#m11-mvi-udf" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 hover:bg-indigo-50 dark:hover:bg-indigo-950 text-slate-800 dark:text-slate-200 transition">
                        2. MVI & UDF Architecture
                    </a>
                    <a href="#m11-modular-arch" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 hover:bg-indigo-50 dark:hover:bg-indigo-950 text-slate-800 dark:text-slate-200 transition">
                        3. Modular Multi-Module Architecture
                    </a>
                    <a href="#m11-design-patterns" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 hover:bg-indigo-50 dark:hover:bg-indigo-950 text-slate-800 dark:text-slate-200 transition">
                        4. 12 Production Android Design Patterns
                    </a>
                </div>

                <div class="space-y-12">

                    <!-- ==================================================== -->
                    <!-- 11.1 MVVM + CLEAN ARCHITECTURE -->
                    <!-- ==================================================== -->
                    <article id="m11-mvvm-clean" class="searchable-card bg-white dark:bg-slate-900 rounded-3xl border border-slate-200/90 dark:border-slate-800 p-6 sm:p-8 shadow-sm hover:shadow-md transition-all">
                        <div class="flex items-center gap-2 pb-3 border-b border-slate-100 dark:border-slate-800">
                            <span class="px-2.5 py-0.5 rounded-md text-xs font-mono font-bold bg-indigo-100 dark:bg-indigo-950 text-indigo-800 dark:text-indigo-300 border border-indigo-300 dark:border-indigo-800">
                                ARCHITECTURE 01
                            </span>
                            <span class="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Layered Separation of Concerns</span>
                        </div>

                        <h3 class="text-2xl font-bold text-slate-900 dark:text-white mt-4 tracking-tight">
                            {m11_mvvm['title']}
                        </h3>
                        <p class="text-sm font-medium text-slate-500 dark:text-slate-400 mt-1">{m11_mvvm['subtitle']}</p>

                        <!-- Why It Matters Banner -->
                        <div class="mt-5 p-4 rounded-2xl bg-indigo-50/60 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-800/60">
                            <div class="text-xs font-extrabold uppercase tracking-wider text-indigo-700 dark:text-indigo-300 flex items-center gap-1.5 mb-1.5">
                                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
                                <span>Why Clean Architecture Matters in Android</span>
                            </div>
                            <p class="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
                                {m11_mvvm['why_it_matters']}
                            </p>
                        </div>

                        <!-- System Architecture Diagram -->
                        <div class="mt-6">
                            <div class="flex items-center justify-between mb-2">
                                <span class="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">System Architecture Flow Diagram:</span>
                                <span class="text-[11px] font-mono text-slate-400">Inward Dependency Rule</span>
                            </div>
                            <div class="rounded-2xl overflow-hidden border border-slate-800 bg-slate-950 p-4 text-emerald-400 text-xs overflow-x-auto custom-scrollbar ascii-box">
                                <pre><code>{html.escape(m11_mvvm['diagram'])}</code></pre>
                            </div>
                        </div>

                        <!-- Layer Breakdown & Why Each Class Is Used -->
                        <div class="mt-8 space-y-6">
                            <h4 class="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
                                <span>Layer Breakdown & Why Each Class Is Used</span>
                            </h4>
"""

for lb in m11_mvvm['layer_breakdown']:
    badge_style = badge_color_map.get(lb['color'], badge_color_map['indigo'])[0]
    html_content += f"""
                            <div class="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/60">
                                <div class="flex items-center gap-2 mb-2">
                                    <span class="text-xs font-extrabold uppercase tracking-wider px-2.5 py-0.5 rounded-full border {badge_style}">
                                        {lb['layer']}
                                    </span>
                                </div>
                                <p class="text-xs text-slate-600 dark:text-slate-400 mb-4">{lb['description']}</p>
                                
                                <div class="space-y-3">
    """
    for cls in lb['classes']:
        html_content += f"""
                                    <div class="p-3.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
                                        <div class="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
                                            <span class="w-2 h-2 rounded-full bg-indigo-500"></span>
                                            <span>{cls['name']}</span>
                                        </div>
                                        <div class="mt-2 text-xs text-slate-700 dark:text-slate-300 space-y-1">
                                            <p><span class="font-bold text-amber-700 dark:text-amber-400">Why this class is used:</span> {cls['why_used']}</p>
                                            <p><span class="font-bold text-indigo-700 dark:text-indigo-400">Class Responsibility:</span> {cls['responsibility']}</p>
                                        </div>
                                    </div>
        """
    html_content += """
                                </div>
                            </div>
    """

html_content += f"""
                        </div>

                        <!-- Full Production Kotlin Example -->
                        <div class="mt-8 rounded-2xl overflow-hidden border border-slate-200 dark:border-slate-800 bg-slate-900 dark:bg-black shadow-inner">
                            <div class="px-4 py-2.5 bg-slate-800/80 dark:bg-slate-900/80 border-b border-slate-700/60 flex items-center justify-between">
                                <span class="text-xs font-mono text-slate-400">End-to-End MVVM + Clean Architecture Implementation</span>
                                <button onclick="copyCode(this)" data-code="{html.escape(m11_mvvm['code'])}" class="text-xs font-mono text-slate-400 hover:text-white transition flex items-center gap-1.5 px-2.5 py-1 rounded bg-slate-800 border border-slate-700">
                                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
                                    <span>Copy Complete Architecture</span>
                                </button>
                            </div>
                            <pre class="p-4 text-xs font-mono text-emerald-300 overflow-x-auto custom-scrollbar leading-relaxed"><code>{html.escape(m11_mvvm['code'])}</code></pre>
                        </div>
                    </article>

                    <!-- ==================================================== -->
                    <!-- 11.2 MVI (MODEL-VIEW-INTENT & UDF) -->
                    <!-- ==================================================== -->
                    <article id="m11-mvi-udf" class="searchable-card bg-white dark:bg-slate-900 rounded-3xl border border-slate-200/90 dark:border-slate-800 p-6 sm:p-8 shadow-sm hover:shadow-md transition-all">
                        <div class="flex items-center gap-2 pb-3 border-b border-slate-100 dark:border-slate-800">
                            <span class="px-2.5 py-0.5 rounded-md text-xs font-mono font-bold bg-purple-100 dark:bg-purple-950 text-purple-800 dark:text-purple-300 border border-purple-300 dark:border-purple-800">
                                ARCHITECTURE 02
                            </span>
                            <span class="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Unidirectional Data Flow (UDF)</span>
                        </div>

                        <h3 class="text-2xl font-bold text-slate-900 dark:text-white mt-4 tracking-tight">
                            {m11_mvi['title']}
                        </h3>
                        <p class="text-sm font-medium text-slate-500 dark:text-slate-400 mt-1">{m11_mvi['subtitle']}</p>

                        <!-- Why It Matters Banner -->
                        <div class="mt-5 p-4 rounded-2xl bg-purple-50/60 dark:bg-purple-950/40 border border-purple-200 dark:border-purple-800/60">
                            <div class="text-xs font-extrabold uppercase tracking-wider text-purple-700 dark:text-purple-300 flex items-center gap-1.5 mb-1.5">
                                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
                                <span>Why MVI & UDF Matter (Zero Impossible States)</span>
                            </div>
                            <p class="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
                                {m11_mvi['why_it_matters']}
                            </p>
                        </div>

                        <!-- UDF Cycle Diagram -->
                        <div class="mt-6">
                            <div class="flex items-center justify-between mb-2">
                                <span class="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Unidirectional Data Flow (UDF) Loop Diagram:</span>
                                <span class="text-[11px] font-mono text-slate-400">UI = f(State)</span>
                            </div>
                            <div class="rounded-2xl overflow-hidden border border-slate-800 bg-slate-950 p-4 text-emerald-400 text-xs overflow-x-auto custom-scrollbar ascii-box">
                                <pre><code>{html.escape(m11_mvi['diagram'])}</code></pre>
                            </div>
                        </div>

                        <!-- MVI Component Breakdown & Why Used -->
                        <div class="mt-8 space-y-4">
                            <h4 class="text-lg font-bold text-slate-900 dark:text-white">MVI Component Breakdown & Why Used</h4>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
"""

for c in m11_mvi['class_breakdown']:
    html_content += f"""
                                <div class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/60">
                                    <div class="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
                                        <span class="w-2.5 h-2.5 rounded-full bg-purple-500"></span>
                                        <span>{c['name']}</span>
                                    </div>
                                    <p class="text-xs text-amber-700 dark:text-amber-400 mt-2 font-semibold">Why this class is used: <span class="text-slate-700 dark:text-slate-300 font-normal">{c['why_used']}</span></p>
                                    <p class="text-xs text-indigo-700 dark:text-indigo-400 mt-1 font-semibold">Under the hood: <span class="text-slate-700 dark:text-slate-300 font-normal">{c['description']}</span></p>
                                </div>
    """

html_content += f"""
                            </div>
                        </div>

                        <!-- Production MVI Code -->
                        <div class="mt-8 rounded-2xl overflow-hidden border border-slate-200 dark:border-slate-800 bg-slate-900 dark:bg-black shadow-inner">
                            <div class="px-4 py-2.5 bg-slate-800/80 dark:bg-slate-900/80 border-b border-slate-700/60 flex items-center justify-between">
                                <span class="text-xs font-mono text-slate-400">Complete Production MVI Kotlin + Compose Implementation</span>
                                <button onclick="copyCode(this)" data-code="{html.escape(m11_mvi['code'])}" class="text-xs font-mono text-slate-400 hover:text-white transition flex items-center gap-1.5 px-2.5 py-1 rounded bg-slate-800 border border-slate-700">
                                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
                                    <span>Copy MVI Architecture</span>
                                </button>
                            </div>
                            <pre class="p-4 text-xs font-mono text-emerald-300 overflow-x-auto custom-scrollbar leading-relaxed"><code>{html.escape(m11_mvi['code'])}</code></pre>
                        </div>
                    </article>

                    <!-- ==================================================== -->
                    <!-- 11.3 MODULAR MULTI-MODULE ARCHITECTURE -->
                    <!-- ==================================================== -->
                    <article id="m11-modular-arch" class="searchable-card bg-white dark:bg-slate-900 rounded-3xl border border-slate-200/90 dark:border-slate-800 p-6 sm:p-8 shadow-sm hover:shadow-md transition-all">
                        <div class="flex items-center gap-2 pb-3 border-b border-slate-100 dark:border-slate-800">
                            <span class="px-2.5 py-0.5 rounded-md text-xs font-mono font-bold bg-teal-100 dark:bg-teal-950 text-teal-800 dark:text-teal-300 border border-teal-300 dark:border-teal-800">
                                ARCHITECTURE 03
                            </span>
                            <span class="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Multi-Module Scalability & Build Performance</span>
                        </div>

                        <h3 class="text-2xl font-bold text-slate-900 dark:text-white mt-4 tracking-tight">
                            {m11_mod['title']}
                        </h3>
                        <p class="text-sm font-medium text-slate-500 dark:text-slate-400 mt-1">{m11_mod['subtitle']}</p>

                        <!-- Why It Matters Banner -->
                        <div class="mt-5 p-4 rounded-2xl bg-teal-50/60 dark:bg-teal-950/40 border border-teal-200 dark:border-teal-800/60">
                            <div class="text-xs font-extrabold uppercase tracking-wider text-teal-700 dark:text-teal-300 flex items-center gap-1.5 mb-1.5">
                                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
                                <span>Why Multi-Module Architecture Matters</span>
                            </div>
                            <p class="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
                                {m11_mod['why_it_matters']}
                            </p>
                        </div>

                        <!-- Dependency Graph Diagram -->
                        <div class="mt-6">
                            <div class="flex items-center justify-between mb-2">
                                <span class="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Enterprise Multi-Module Dependency Graph:</span>
                                <span class="text-[11px] font-mono text-slate-400">Parallel Build Optimization</span>
                            </div>
                            <div class="rounded-2xl overflow-hidden border border-slate-800 bg-slate-950 p-4 text-emerald-400 text-xs overflow-x-auto custom-scrollbar ascii-box">
                                <pre><code>{html.escape(m11_mod['diagram'])}</code></pre>
                            </div>
                        </div>

                        <!-- Module Taxonomy Grid -->
                        <div class="mt-8 space-y-4">
                            <h4 class="text-lg font-bold text-slate-900 dark:text-white">Module Taxonomy & Responsibilities</h4>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
"""

for mt in m11_mod['module_taxonomy']:
    html_content += f"""
                                <div class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/60">
                                    <div class="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
                                        <span class="w-2.5 h-2.5 rounded-full bg-teal-500"></span>
                                        <span>{mt['module_type']}</span>
                                    </div>
                                    <p class="text-xs text-amber-700 dark:text-amber-400 mt-2 font-semibold">Why this module is used: <span class="text-slate-700 dark:text-slate-300 font-normal">{mt['why_used']}</span></p>
                                    <p class="text-xs text-indigo-700 dark:text-indigo-400 mt-1 font-semibold">Module Contents: <span class="text-slate-700 dark:text-slate-300 font-normal">{mt['description']}</span></p>
                                </div>
    """

html_content += f"""
                            </div>
                        </div>

                        <!-- Golden Architectural Rules -->
                        <div class="mt-6 p-4 rounded-2xl bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800/60">
                            <div class="text-xs font-extrabold uppercase tracking-wider text-amber-800 dark:text-amber-300 mb-2">4 Golden Rules of Multi-Module Architecture:</div>
                            <ul class="space-y-1.5 text-xs font-medium text-slate-800 dark:text-slate-200">
"""
for r in m11_mod['golden_rules']:
    html_content += f"""                                <li class="flex items-start gap-2"><span class="text-amber-500 font-bold">•</span><span>{r}</span></li>\n"""

html_content += f"""
                            </ul>
                        </div>

                        <!-- Gradle & Feature Contract Code -->
                        <div class="mt-8 rounded-2xl overflow-hidden border border-slate-200 dark:border-slate-800 bg-slate-900 dark:bg-black shadow-inner">
                            <div class="px-4 py-2.5 bg-slate-800/80 dark:bg-slate-900/80 border-b border-slate-700/60 flex items-center justify-between">
                                <span class="text-xs font-mono text-slate-400">Gradle Kotlin DSL & Navigation Contract Pattern</span>
                                <button onclick="copyCode(this)" data-code="{html.escape(m11_mod['code'])}" class="text-xs font-mono text-slate-400 hover:text-white transition flex items-center gap-1.5 px-2.5 py-1 rounded bg-slate-800 border border-slate-700">
                                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
                                    <span>Copy Multi-Module Code</span>
                                </button>
                            </div>
                            <pre class="p-4 text-xs font-mono text-emerald-300 overflow-x-auto custom-scrollbar leading-relaxed"><code>{html.escape(m11_mod['code'])}</code></pre>
                        </div>
                    </article>

                    <!-- ==================================================== -->
                    <!-- 11.4 12 PRODUCTION ANDROID DESIGN PATTERNS -->
                    <!-- ==================================================== -->
                    <div id="m11-design-patterns" class="pt-6">
                        <div class="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-slate-800 mb-6">
                            <div>
                                <h3 class="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight">12 Production Android Design Patterns (Deep Dive)</h3>
                                <p class="text-sm text-slate-600 dark:text-slate-400">Creational, Structural, and Behavioral patterns with real Android SDK & Jetpack production examples.</p>
                            </div>
                        </div>

                        <div class="grid grid-cols-1 gap-8">
"""

# Render 12 Design Patterns
for dp in m11_patterns:
    escaped_dp_code = html.escape(dp['code'])
    cat_badge = {
        "Creational": "bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 border-emerald-300 dark:border-emerald-800",
        "Structural": "bg-blue-100 dark:bg-blue-950 text-blue-800 dark:text-blue-300 border-blue-300 dark:border-blue-800",
        "Behavioral": "bg-purple-100 dark:bg-purple-950 text-purple-800 dark:text-purple-300 border-purple-300 dark:border-purple-800"
    }.get(dp['category'], "bg-slate-100 text-slate-800 border-slate-300")

    html_content += f"""
                            <!-- Design Pattern #{dp['number']}: {dp['id']} -->
                            <article id="{dp['id']}" class="searchable-card bg-white dark:bg-slate-900 rounded-3xl border border-slate-200/90 dark:border-slate-800 p-6 sm:p-8 shadow-sm hover:shadow-md transition-all">
                                
                                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-4 border-b border-slate-100 dark:border-slate-800">
                                    <div class="flex items-center gap-2">
                                        <span class="px-2.5 py-0.5 rounded-md text-xs font-mono font-bold {cat_badge} border">
                                            PATTERN #{dp['number']} • {dp['category'].upper()}
                                        </span>
                                    </div>
                                    <button onclick="copyCode(this)" data-code="{escaped_dp_code}" class="self-start sm:self-auto text-xs font-mono text-slate-500 hover:text-slate-900 dark:hover:text-white transition flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
                                        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
                                        <span>Copy Pattern Snippet</span>
                                    </button>
                                </div>

                                <h4 class="text-xl sm:text-2xl font-bold text-slate-900 dark:text-white mt-4 tracking-tight">
                                    {dp['name']}
                                </h4>

                                <!-- Deep Dive 3-Column Info -->
                                <div class="mt-5 grid grid-cols-1 md:grid-cols-3 gap-4">
                                    
                                    <!-- When to Use -->
                                    <div class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/60">
                                        <div class="text-xs font-extrabold uppercase tracking-wider text-emerald-600 dark:text-emerald-400 mb-1.5">
                                            🎯 When To Use
                                        </div>
                                        <p class="text-xs text-slate-700 dark:text-slate-300 leading-relaxed font-normal">
                                            {dp['when_to_use']}
                                        </p>
                                    </div>

                                    <!-- Why Used -->
                                    <div class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/60">
                                        <div class="text-xs font-extrabold uppercase tracking-wider text-amber-600 dark:text-amber-400 mb-1.5">
                                            💡 Why It Matters
                                        </div>
                                        <p class="text-xs text-slate-700 dark:text-slate-300 leading-relaxed font-normal">
                                            {dp['why_used']}
                                        </p>
                                    </div>

                                    <!-- How In Android -->
                                    <div class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/60">
                                        <div class="text-xs font-extrabold uppercase tracking-wider text-indigo-600 dark:text-indigo-400 mb-1.5">
                                            📱 In Android Framework
                                        </div>
                                        <p class="text-xs text-slate-700 dark:text-slate-300 leading-relaxed font-normal">
                                            {dp['how_in_android']}
                                        </p>
                                    </div>

                                </div>

                                <!-- Code Snippet -->
                                <div class="mt-5 rounded-2xl overflow-hidden border border-slate-200 dark:border-slate-800 bg-slate-900 dark:bg-black shadow-inner">
                                    <div class="px-4 py-2 bg-slate-800/80 dark:bg-slate-900/80 border-b border-slate-700/60 flex items-center justify-between">
                                        <span class="text-xs font-mono text-slate-400">Real Android Production Example</span>
                                        <span class="text-[11px] font-mono text-emerald-400">Kotlin Tested</span>
                                    </div>
                                    <pre class="p-4 text-xs font-mono text-emerald-300 overflow-x-auto custom-scrollbar leading-relaxed"><code>{escaped_dp_code}</code></pre>
                                </div>

                            </article>
    """

html_content += """
                        </div>
                    </div>

                </div>
            </section>
        </div>
    </main>

    <!-- Speed Drill Flashcard Modal -->
    <div id="flashcardModal" class="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm hidden flex items-center justify-center p-4">
        <div class="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-2xl max-w-2xl w-full p-6 sm:p-8 flex flex-col relative max-h-[90vh]">
            <button onclick="closeSpeedDrill()" class="absolute top-4 right-4 p-2 rounded-full text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>

            <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
                <span id="cardModuleBadge" class="text-xs font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-indigo-50 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800">Module 1</span>
                <span class="text-xs font-semibold text-slate-400 dark:text-slate-500">Card <span id="cardCurrentIndex">1</span> of 108</span>
            </div>

            <!-- Card Content -->
            <div id="flashcardBody" onclick="flipSpeedCard()" class="my-6 p-6 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 cursor-pointer min-h-[220px] flex flex-col justify-center transition-all hover:bg-slate-100/70 dark:hover:bg-slate-800 select-none">
                <div id="flashcardSidePrompt" class="text-[11px] font-bold uppercase tracking-widest text-slate-400 dark:text-slate-500 mb-2">QUESTION (TAP / SPACE TO REVEAL 6-POINT ANSWER)</div>
                <div id="flashcardContent" class="text-xl font-bold text-slate-900 dark:text-white leading-snug">Loading question...</div>
            </div>

            <!-- Navigation Controls -->
            <div class="flex items-center justify-between pt-2">
                <button onclick="prevSpeedCard()" class="px-4 py-2 text-xs font-bold rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 transition">
                    ← Previous (Left)
                </button>
                <button onclick="flipSpeedCard()" class="px-5 py-2 text-xs font-bold rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white shadow transition">
                    Flip (Space)
                </button>
                <button onclick="nextSpeedCard()" class="px-4 py-2 text-xs font-bold rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 transition">
                    Next (Right) →
                </button>
            </div>
        </div>
    </div>

    <!-- Floating Back to Top Button -->
    <button onclick="window.scrollTo({ top: 0, behavior: 'smooth' })" class="fixed bottom-6 right-6 w-11 h-11 rounded-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white shadow-lg flex items-center justify-center transition hover:scale-105 z-30">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/></svg>
    </button>

    <!-- Interactive Scripts -->
    <script>
        const portalData = """ + flashcards_json + """;
        const topicData = """ + topics_json + """;
        const m11Data = """ + m11_json + """;

        let flatQuestions = [];
        portalData.forEach(m => {
            m.questions.forEach(q => {
                flatQuestions.push({ ...q, moduleTitle: m.title, moduleBadge: m.badge });
            });
        });

        let currentCardIndex = 0;
        let isCardFlipped = false;

        // Dark Mode Toggle
        function toggleDarkMode() {
            document.documentElement.classList.toggle('dark');
            const isDark = document.documentElement.classList.contains('dark');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        }

        // Check Dark Mode preference
        if (localStorage.getItem('theme') === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }

        // Sound Synthesizer Chime
        function playChime() {
            try {
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(587.33, audioCtx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(880, audioCtx.currentTime + 0.15);
                gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.6);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.6);
            } catch(e) {
                console.log(e);
            }
        }

        function startBreathTimer(btn) {
            const label = btn.querySelector('.timer-label');
            let timeLeft = 3;
            btn.classList.add('bg-amber-100', 'text-amber-800', 'border-amber-300', 'dark:bg-amber-950', 'dark:text-amber-200');
            label.innerText = `Inhale... ${timeLeft}s`;
            
            const interval = setInterval(() => {
                timeLeft--;
                if (timeLeft > 0) {
                    label.innerText = `Steady... ${timeLeft}s`;
                } else {
                    clearInterval(interval);
                    playChime();
                    label.innerText = `Speak with conviction!`;
                    setTimeout(() => {
                        btn.classList.remove('bg-amber-100', 'text-amber-800', 'border-amber-300', 'dark:bg-amber-950', 'dark:text-amber-200');
                        label.innerText = `3s Breath Chime`;
                    }, 2000);
                }
            }, 1000);
        }

        function readAloud(btn, text) {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 0.95;
                utterance.pitch = 1.0;
                window.speechSynthesis.speak(utterance);
            } else {
                alert("Speech synthesis is not supported on your browser.");
            }
        }

        function copyCode(btn) {
            const code = btn.getAttribute('data-code');
            navigator.clipboard.writeText(code).then(() => {
                const span = btn.querySelector('span');
                const orig = span ? span.innerText : 'Copy';
                if (span) span.innerText = 'Copied!';
                setTimeout(() => { if (span) span.innerText = orig; }, 1500);
            });
        }

        function toggleKeywordFocus() {
            document.body.classList.toggle('keyword-focus');
            const btn = document.getElementById('keywordFocusBtn');
            btn.classList.toggle('bg-amber-100');
            btn.classList.toggle('text-amber-900');
            btn.classList.toggle('border-amber-300');
        }

        // Speed Drill Flashcards
        function openSpeedDrill() {
            document.getElementById('flashcardModal').classList.remove('hidden');
            currentCardIndex = 0;
            isCardFlipped = false;
            updateSpeedCard();
        }

        function closeSpeedDrill() {
            document.getElementById('flashcardModal').classList.add('hidden');
        }

        function updateSpeedCard() {
            const card = flatQuestions[currentCardIndex];
            document.getElementById('cardModuleBadge').innerText = `${card.moduleBadge} • ${card.moduleTitle.split(':')[1] || ''}`;
            document.getElementById('cardCurrentIndex').innerText = currentCardIndex + 1;
            const content = document.getElementById('flashcardContent');
            const prompt = document.getElementById('flashcardSidePrompt');
            
            if (!isCardFlipped) {
                prompt.innerText = "QUESTION (TAP / SPACE TO REVEAL 6-POINT ANSWER)";
                content.innerHTML = `<div class="text-xl font-bold text-slate-900 dark:text-white">${card.title}</div><div class="text-xs font-medium text-red-600 dark:text-red-400 mt-2">Problem: ${card.problem}</div>`;
            } else {
                prompt.innerText = "EXECUTIVE 6-POINT ANSWER";
                let bullets = card.solution.map(s => `<li class="flex items-start gap-2 mb-1.5"><span class="px-1.5 py-0.5 rounded text-[10px] font-extrabold uppercase bg-amber-100 dark:bg-amber-950 text-amber-900 dark:text-amber-200 border border-amber-300 dark:border-amber-700/60">${s[0]}</span><span class="text-sm font-medium text-slate-800 dark:text-slate-200">${s[1]}</span></li>`).join('');
                content.innerHTML = `<ul class="text-left space-y-1">${bullets}</ul>`;
            }
        }

        function flipSpeedCard() {
            isCardFlipped = !isCardFlipped;
            updateSpeedCard();
        }

        function nextSpeedCard() {
            if (currentCardIndex < flatQuestions.length - 1) {
                currentCardIndex++;
                isCardFlipped = false;
                updateSpeedCard();
            }
        }

        function prevSpeedCard() {
            if (currentCardIndex > 0) {
                currentCardIndex--;
                isCardFlipped = false;
                updateSpeedCard();
            }
        }

        window.addEventListener('keydown', (e) => {
            const modal = document.getElementById('flashcardModal');
            if (!modal.classList.contains('hidden')) {
                if (e.code === 'Space') {
                    e.preventDefault();
                    flipSpeedCard();
                } else if (e.code === 'ArrowRight') {
                    nextSpeedCard();
                } else if (e.code === 'ArrowLeft') {
                    prevSpeedCard();
                } else if (e.code === 'Escape') {
                    closeSpeedDrill();
                }
            }
        });

        // Mastery Checkbox & Persistence
        function toggleMastery(qid) {
            const cb = document.getElementById(`check-${qid}`);
            localStorage.setItem(`mastery_${qid}`, cb.checked ? 'true' : 'false');
            updateMasteryStats();
        }

        function updateMasteryStats() {
            let count = 0;
            flatQuestions.forEach(q => {
                if (localStorage.getItem(`mastery_${q.id}`) === 'true') {
                    count++;
                    const cb = document.getElementById(`check-${q.id}`);
                    if (cb) cb.checked = true;
                }
            });
            document.getElementById('masteredCount').innerText = count;
            const pct = Math.round((count / flatQuestions.length) * 100);
            document.getElementById('masteredPercent').innerText = pct;
            document.getElementById('masteryProgressBar').style.width = `${pct}%`;
        }

        function resetAllProgress() {
            if (confirm("Reset all mastered question checkboxes?")) {
                flatQuestions.forEach(q => {
                    localStorage.removeItem(`mastery_${q.id}`);
                    const cb = document.getElementById(`check-${q.id}`);
                    if (cb) cb.checked = false;
                });
                updateMasteryStats();
            }
        }

        // Universal Search Across 108 Qs, 50 Deep-Dive Topics, and Module 11 Architecture & Design Patterns
        function filterAllContent() {
            const query = document.getElementById('searchInput').value.toLowerCase().trim();
            
            // Filter 108 Questions
            flatQuestions.forEach(q => {
                const card = document.getElementById(`card-${q.id}`);
                if (!card) return;
                const match = q.title.toLowerCase().includes(query) ||
                              q.problem.toLowerCase().includes(query) ||
                              q.solution.some(s => s[0].toLowerCase().includes(query) || s[1].toLowerCase().includes(query));
                card.style.display = match ? 'block' : 'none';
            });

            // Filter 50 Deep-Dive Topics
            topicData.forEach(t => {
                const card = document.getElementById(`topic-${t.id}`);
                if (!card) return;
                const match = t.title.toLowerCase().includes(query) ||
                              t.category.toLowerCase().includes(query) ||
                              t.why.toLowerCase().includes(query) ||
                              t.how.toLowerCase().includes(query) ||
                              t.takeaway.toLowerCase().includes(query);
                card.style.display = match ? 'block' : 'none';
            });

            // Filter Module 11 (MVVM, MVI, Modularization)
            const mvvmCard = document.getElementById('m11-mvvm-clean');
            if (mvvmCard) {
                const match = query === '' || "mvvm clean architecture usecase repository viewmodel".includes(query) || mvvmCard.innerText.toLowerCase().includes(query);
                mvvmCard.style.display = match ? 'block' : 'none';
            }

            const mviCard = document.getElementById('m11-mvi-udf');
            if (mviCard) {
                const match = query === '' || "mvi unidirectional data flow intent state reducer effect".includes(query) || mviCard.innerText.toLowerCase().includes(query);
                mviCard.style.display = match ? 'block' : 'none';
            }

            const modCard = document.getElementById('m11-modular-arch');
            if (modCard) {
                const match = query === '' || "modular multi-module feature api impl gradle".includes(query) || modCard.innerText.toLowerCase().includes(query);
                modCard.style.display = match ? 'block' : 'none';
            }

            // Filter 12 Design Patterns
            m11Data.design_patterns.forEach(dp => {
                const card = document.getElementById(dp.id);
                if (!card) return;
                const match = dp.name.toLowerCase().includes(query) ||
                              dp.category.toLowerCase().includes(query) ||
                              dp.when_to_use.toLowerCase().includes(query) ||
                              dp.why_used.toLowerCase().includes(query) ||
                              dp.how_in_android.toLowerCase().includes(query);
                card.style.display = match ? 'block' : 'none';
            });
        }

        // Init
        document.addEventListener('DOMContentLoaded', () => {
            updateMasteryStats();
        });
    </script>
</body>
</html>
"""

output_path = "/Users/prajapatichintankumar/.gemini/antigravity/scratch/interview-portal/index.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully compiled MASTER Portal {output_path} with:")
print(f" - 108 Interview Questions (6 points each)")
print(f" - 50 Kotlin & Android Deep Dive Topics")
print(f" - Module 11: MVVM + Clean, MVI, Modularization, 12 Design Patterns!")
