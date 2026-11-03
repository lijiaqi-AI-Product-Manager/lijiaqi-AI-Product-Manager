"""Build the profile's original, dependency-free SVG artwork."""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FONT = "'Segoe UI','Microsoft YaHei','PingFang SC',sans-serif"
MONO = "'Cascadia Code','Consolas',monospace"
THEMES = {
    "light": dict(bg="#f7f6f2", panel="#ffffff", text="#1d3434", muted="#607472", line="#d9e2da", mint="#237c68", warm="#b66638", soft="#e7f0e9"),
    "dark": dict(bg="#101c20", panel="#18292d", text="#ecf3ec", muted="#a3bab5", line="#30494b", mint="#9be4bc", warm="#f4b283", soft="#203a37"),
}


def text(x, y, value, size=20, color=None, weight=400, family=FONT, extra=""):
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{color}" {extra}>{escape(str(value))}</text>'


def rect(x, y, w, h, fill, radius=16, stroke=None, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}"' + (f' stroke="{stroke}"' if stroke else "") + f' {extra}/>'


def line(x1, y1, x2, y2, color, width=1, extra=""):
    return f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{color}" stroke-width="{width}" fill="none" {extra}/>'


def dot(x, y, r, color, extra=""):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" {extra}/>'


def wrap(name, theme, width, height, title, body):
    p = THEMES[theme]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">Original portfolio artwork for Li Jiaqi. Decorative interface sketches explain the product; they are not application screenshots.</desc>
<defs><pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{p['line']}" stroke-width=".65" opacity=".42"/></pattern>
<linearGradient id="wash" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{p['soft']}"/><stop offset="1" stop-color="{p['bg']}"/></linearGradient></defs>
{body}</svg>'''
    (ASSETS / f"{name}-{theme}.svg").write_text(svg + "\n", encoding="utf-8", newline="\n")


def hero(theme):
    p = THEMES[theme]
    b = rect(1, 1, 1278, 478, p["bg"], 28, p["line"])
    b += rect(710, 1, 569, 478, "url(#wash)", 28)
    b += rect(710, 1, 569, 478, "url(#grid)", 28)
    b += text(58, 67, "PRODUCT / AI / ENGINEERING", 15, p["mint"], 600, MONO, 'letter-spacing="2.2"')
    b += text(54, 182, "李佳奇", 88, p["text"], 700)
    b += text(58, 234, "Li Jiaqi / Gauss", 34, p["muted"], 400)
    b += text(58, 283, "把真实问题，做成好用的产品。", 27, p["text"], 500)
    b += text(58, 316, "Turning real problems into useful products.", 20, p["muted"])
    b += line(58, 344, 620, 344, p["line"])
    b += text(58, 379, "AI 产品经理 · AI Product Manager", 20, p["text"], 600)
    b += text(58, 413, "厦门大学 2029 届 · Xiamen University '29", 18, p["muted"])
    b += text(58, 449, "Research → Build → Verify → Iterate", 14, p["muted"], 400, MONO)
    # An original orbit diagram; no borrowed project logo or third-party asset.
    b += '<g transform="translate(988,235)">'
    b += f'<ellipse rx="178" ry="139" fill="none" stroke="{p["line"]}" stroke-dasharray="4 8"/>'
    b += f'<ellipse rx="114" ry="196" fill="none" stroke="{p["line"]}" transform="rotate(43)"/>'
    b += f'<ellipse rx="196" ry="87" fill="none" stroke="{p["mint"]}" opacity=".32" transform="rotate(-32)"/>'
    b += dot(0, 0, 73, p["soft"])
    b += f'<circle r="58" fill="none" stroke="{p["mint"]}" opacity=".55"/>'
    b += text(0, 13, "LJ", 42, p["text"], 600, MONO, 'text-anchor="middle"')
    for x, y, label, col in [(-139, -91, "INSIGHT", p["mint"]), (130, -66, "CRAFT", p["warm"]), (46, 145, "EVIDENCE", p["mint"])]:
        b += line(0, 0, x, y, p["line"])
        b += rect(x - 68, y - 20, 136, 40, p["panel"], 20, p["line"])
        b += dot(x - 47, y, 4, col)
        b += text(x + 6, y + 5, label, 13, p["text"], 500, MONO, 'text-anchor="middle"')
    b += dot(-31, -143, 6, p["warm"]) + dot(179, 19, 5, p["mint"]) + dot(-131, 85, 4, p["mint"])
    b += "</g>"
    b += text(1197, 434, "LET'S BUILD.", 13, p["muted"], 500, MONO, 'text-anchor="end" letter-spacing="1.2"')
    wrap("hero", theme, 1280, 480, "李佳奇 Li Jiaqi — AI 产品经理，厦门大学 2029 届", b)


def mobile_artwork(theme):
    p = THEMES[theme]
    b = rect(1, 1, 622, 498, p["bg"], 24, p["line"])
    b += text(35, 49, "PRODUCT / AI / ENGINEERING", 13, p["mint"], 600, MONO)
    b += text(31, 142, "李佳奇", 74, p["text"], 700)
    b += text(35, 187, "Li Jiaqi / Gauss", 28, p["muted"])
    b += text(35, 247, "把真实问题，做成好用的产品。", 27, p["text"], 500)
    b += text(35, 280, "Turning real problems into useful products.", 19, p["muted"])
    b += line(35, 309, 589, 309, p["line"])
    b += text(35, 350, "AI 产品经理", 25, p["text"], 600)
    b += text(35, 381, "AI Product Manager", 21, p["muted"])
    b += text(35, 420, "厦门大学 · 2029 届", 24, p["text"])
    b += text(35, 450, "Xiamen University · Class of 2029", 19, p["muted"])
    b += text(35, 481, "Research → Build → Verify → Iterate", 13, p["muted"], 400, MONO)
    b += f'<ellipse cx="492" cy="138" rx="67" ry="53" fill="none" stroke="{p["mint"]}" opacity=".4" transform="rotate(-28 492 138)"/>'
    b += dot(492, 138, 35, p["soft"]) + text(492, 148, "LJ", 29, p["text"], 500, MONO, 'text-anchor="middle"')
    b += dot(551, 112, 5, p["warm"])
    wrap("hero-mobile", theme, 624, 500, "李佳奇 Li Jiaqi — AI Product Manager, Xiamen University Class of 2029", b)
    b = rect(1, 1, 622, 388, p["bg"], 22, p["line"])
    for x, y, num, title, en, sub in [(30, 20, "01", "看见问题", "Understand the problem", "Research / competitive testing"), (337, 20, "02", "定义行为", "Define behavior", "PRDs / states / acceptance"), (30, 207, "03", "实现产品", "Build the product", "AI Coding / full-stack"), (337, 207, "04", "用证据迭代", "Verify and iterate", "Replay / regression / metrics")]:
        b += text(x, y + 25, num, 18, p["mint"], 500, MONO)
        b += text(x, y + 73, title, 30, p["text"], 600)
        b += text(x, y + 108, en, 18, p["muted"])
        b += text(x, y + 139, sub, 13, p["muted"])
    wrap("process-mobile", theme, 624, 390, "看见问题、定义行为、实现产品、用证据迭代 / Research, define, build, verify", b)


PROJECTS = [
    ("job-radar", "01", "DATA / OPPORTUNITY", "job_radar", "把招聘信息，变成本地可查询的数据。", "Public job data, ready for local search.", "Python · SQLite · CLI / MCP", "mint"),
    ("qgauss", "02", "CREATIVE / WORKSPACE", "QGauss AI", "对话、图像、视频与声音，一个工作台。", "Chat, images, video and voice in one workspace.", "Vue · NestJS · Prisma", "warm"),
    ("agent-compare", "03", "AGENTS / DECISIONS", "AgentCompare", "同一需求，两版真跑，盲选再揭晓。", "Two live builds. Choose first, reveal later.", "TypeScript · Git worktree · DSH", "mint"),
    ("bug-gps", "04", "AGENTS / VERIFICATION", "BugGPS", "录下问题，按原预期复核修复。", "Record the bug. Replay the original expectation.", "JavaScript · Playwright · DSH", "warm"),
    ("skill-healthcheck", "05", "AGENTS / OBSERVABILITY", "skill-healthcheck", "技能还在，为什么助手不再调用？", "Find skills that silently stopped working.", "TypeScript · Git · Local evidence", "mint"),
    ("unremember", "06", "AGENTS / PRIVACY", "unremember", "让本地 Agent 的遗忘可验证、可回滚。", "Verifiable, reversible forgetting for local agents.", "TypeScript · JSONL / Zstd · SHA-256", "warm"),
]


def window(p, x=34, y=161, w=556, h=132):
    b = rect(x, y, w, h, p["panel"], 12, p["line"])
    for i in range(3):
        b += dot(x + 17 + i * 13, y + 16, 3, p["muted"], 'opacity=".55"')
    return b + line(x, y + 31, x + w, y + 31, p["line"])


def card(slug, num, label, name, desc, en, stack, accent, theme):
    p = THEMES[theme]
    col = p[accent]
    b = rect(1, 1, 622, 382, p["bg"], 22, p["line"])
    b += text(34, 36, label, 12, col, 600, MONO, 'letter-spacing="1.6"')
    b += text(590, 36, num, 14, p["muted"], 400, MONO, 'text-anchor="end"')
    title_size = 34 if len(name) > 14 else 39
    b += text(32, 88, name, title_size, p["text"], 650)
    b += text(34, 126, desc, 21, p["muted"])
    b += text(34, 153, en, 16, p["muted"])
    b += '<g transform="translate(0,22)">'
    if slug == "job-radar":
        b += window(p)
        b += text(88, 182, "LOCAL DATA / ORIGINAL SOURCES", 11, p["muted"], 400, MONO)
        for yy, company, role, badge in [(219, "Company / city", "Jobs & JD", "Source"), (249, "Year / type", "Filters & evidence", "Date"), (279, "Calendar / changes", "Local SQLite", "State")]:
            b += dot(52, yy - 5, 3, col)
            b += text(65, yy, company, 13, p["text"])
            b += text(239, yy, role, 13, p["muted"])
            b += rect(515, yy - 17, 50, 22, p["soft"], 6)
            b += text(540, yy - 2, badge, 11, col, 500, extra='text-anchor="middle"')
    elif slug == "qgauss":
        b += window(p)
        b += text(88, 182, "YOUR MULTIMODAL STUDIO", 11, p["muted"], 400, MONO)
        for x, mark, caption in [(52, "Aa", "Chat"), (184, "◇", "Image"), (316, "▷", "Video"), (448, "≈", "Voice")]:
            b += rect(x, 207, 124, 68, p["soft"], 10)
            b += text(x + 20, 244, mark, 29, col, 500, MONO)
            b += text(x + 72, 245, caption, 13, p["text"])
    elif slug == "agent-compare":
        for x, letter, offset in [(34, "A", 0), (324, "B", 17)]:
            b += rect(x, 161, 266, 132, p["panel"], 12, p["line"])
            b += text(x + 15, 185, letter, 15, col, 600, MONO)
            b += rect(x + 17, 203, 232, 13, p["soft"], 4)
            b += rect(x + 17, 228, 100 + offset, 46, p["soft"], 7)
            b += rect(x + 128 + offset, 228, 121 - offset, 46, p["soft"], 7)
            b += dot(x + 236, 182, 3, col)
        b += rect(270, 215, 84, 34, col, 17)
        b += text(312, 237, "A | B", 15, p["bg"], 600, MONO, 'text-anchor="middle"')
    elif slug == "bug-gps":
        b += window(p)
        b += text(88, 182, "RECORD → LOCK → VERIFY", 11, p["muted"], 400, MONO)
        b += line(106, 235, 518, 235, p["line"], 3)
        for x, yy, lbl, tag, color in [(106, 235, "Record", "EXPECTATION", p["warm"]), (312, 235, "Lock", "SAME FAILURE", p["muted"]), (518, 235, "Verify", "VERIFIED", p["mint"])]:
            b += dot(x, yy, 17, p["soft"]) + dot(x, yy, 6, color)
            b += text(x, 213, lbl, 13, p["text"], 500, extra='text-anchor="middle"')
            b += text(x, 275, tag, 10, color, 500, MONO, 'text-anchor="middle"')
    elif slug == "skill-healthcheck":
        b += window(p)
        b += text(88, 182, "$ skill-healthcheck", 11, p["muted"], 400, MONO)
        for yy, symbol, label2, status, color in [(220, "✓", "Host loading rules", "CHECK", p["mint"]), (248, "!", "Upstream description", "CHANGED", p["warm"]), (276, "↳", "Session timeline", "WHY", p["mint"])]:
            b += text(51, yy, symbol, 15, color, 600, MONO)
            b += text(78, yy, label2, 14, p["text"])
            b += text(567, yy, status, 11, color, 400, MONO, 'text-anchor="end"')
    elif slug == "unremember":
        b += window(p)
        b += text(88, 182, "PLAN / APPLY / VERIFY / ROLLBACK", 11, p["muted"], 400, MONO)
        b += text(53, 221, "session", 12, p["muted"], 400, MONO)
        b += rect(158, 208, 277, 15, p["line"], 4)
        b += text(53, 252, "memory", 12, p["muted"], 400, MONO)
        for x in range(158, 430, 23):
            b += rect(x, 238, 15, 17, p["soft"], 3)
        b += text(53, 280, "fork", 12, p["muted"], 400, MONO)
        b += text(158, 280, "verify against the local copies", 12, col, 500, MONO)
        b += text(553, 248, "↶", 37, col, 400, extra='text-anchor="middle"')
    b += line(34, 312, 590, 312, p["line"])
    b += text(34, 339, stack, 12, p["muted"], 400, MONO)
    b += text(589, 339, "↗", 22, col, 400, extra='text-anchor="end"')
    b += "</g>"
    wrap(slug, theme, 624, 384, f"{name} — {desc} {en} {stack}", b)


def process(theme):
    p = THEMES[theme]
    b = rect(1, 1, 1278, 242, p["bg"], 22, p["line"])
    steps = [("01", "看见问题", "Understand the problem", "Research / competitive testing"), ("02", "定义行为", "Define behavior", "PRDs / states / acceptance"), ("03", "实现产品", "Build the product", "AI Coding / full-stack"), ("04", "用证据迭代", "Verify and iterate", "Replay / regression / metrics")]
    for i, (num, title, en, sub) in enumerate(steps):
        x = 35 + 317 * i
        b += text(x, 49, num, 17, p["mint"], 500, MONO)
        b += text(x, 99, title, 28, p["text"], 600)
        b += text(x, 136, en, 17, p["muted"])
        b += text(x, 169, sub, 13, p["muted"])
        b += rect(x, 198, 240, 4, p["soft"], 2)
        b += rect(x, 198, 50 + 48 * i, 4, p["mint"], 2)
        if i < 3:
            b += text(x + 270, 103, "→", 24, p["muted"])
    wrap("process", theme, 1280, 244, "工作方式 / How I work: research, define, build, verify", b)


def footer(theme):
    p = THEMES[theme]
    b = rect(1, 1, 1278, 158, p["bg"], 22, p["line"])
    b += text(38, 53, "LET'S MAKE SOMETHING USEFUL.", 25, p["text"], 600, MONO)
    b += text(38, 92, "AI 产品 · 开源工具 · 真实业务 · 欢迎交流与合作", 19, p["muted"])
    b += text(38, 126, "AI products · Open source · Real-world operations · Let's connect", 16, p["muted"])
    b += dot(1206, 67, 17, p["soft"]) + text(1206, 75, "↗", 24, p["mint"], 500, extra='text-anchor="middle"')
    wrap("footer", theme, 1280, 160, "欢迎交流 / Let's connect: AI products, open-source tools and real-world operations", b)


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    for theme in THEMES:
        hero(theme)
        mobile_artwork(theme)
        for project in PROJECTS:
            card(*project, theme)
        process(theme)
        footer(theme)
    print(f"Built {len(list(ASSETS.glob('*.svg')))} original SVG assets")


if __name__ == "__main__":
    main()
