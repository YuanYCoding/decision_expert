"""Build the original README SVGs; --render exports PNGs using Playwright.

Run from any directory. No dependencies for SVG; PNG requires playwright and
its Chromium browser. System CJK fonts are used, without network requests.
"""
from __future__ import annotations

import argparse
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "images"
W = 1440
INK = "#142D38"
MUTED = "#526671"
PAPER = "#F4F7F5"
LINE = "#D7E2DE"
TEAL = "#087F6F"
MINT = "#94E3C8"
CORAL = "#E79A7C"
BLUE = "#87BDEA"
DARK = "#102B35"


def text(x, y, value, size=28, color=INK, weight=400, width=None, mono=False):
    limit = f' data-max-width="{width}"' if width else ""
    family = "Consolas, monospace" if mono else "'Microsoft YaHei', 'Noto Sans CJK SC', 'Noto Sans SC', sans-serif"
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" font-family="{family}"{limit}>{escape(value)}</text>'


def rect(x, y, w, h, fill="white", stroke="none", r=16):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'


def line(x1, y1, x2, y2, color=LINE, width=2, arrow=False):
    end = ' marker-end="url(#arrow)"' if arrow else ""
    return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="{width}"{end}/>'


def dot(x, y, color=TEAL, r=6):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'


def document(slug, title, desc, body, h=800, bg=PAPER):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-labelledby="{slug}-title {slug}-desc">
<title id="{slug}-title">{escape(title)}</title>
<desc id="{slug}-desc">{escape(desc)}</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10" fill="none" stroke="{MUTED}" stroke-width="1.5"/></marker></defs>
{rect(0, 0, W, h, bg, r=0)}
{body}
</svg>'''


def header(number, eyebrow, title, sub, dark=False):
    c = "#F1F6F4" if dark else INK
    m = "#BCD0D6" if dark else MUTED
    return (text(72, 60, f"DECISION EXPERT / {number}", 20, MINT if dark else TEAL, 600, mono=True)
            + text(1368, 60, "", 20)
            + text(72, 132, title, 48, c, 700, 1296)
            + text(72, 184, sub, 26, m, width=1296))


def footer(label, h=800, dark=False):
    return (line(72, h - 70, 1368, h - 70, "#31505A" if dark else LINE)
            + text(72, h - 32, "decision_expert", 20, "#BCD0D6" if dark else MUTED, mono=True)
            + text(390, h - 32, label, 20, "#BCD0D6" if dark else MUTED, width=978))


def build():
    items = []
    # Cover: deliberately wide whitespace and a compact three-role diagram.
    b = text(72, 74, "DECISION EXPERT", 23, MINT, 600, mono=True)
    b += text(72, 144, "重大决策前的 AI 压力测试", 28, "#BCD0D6", width=750)
    b += text(72, 270, "先拆穿你的选择。", 72, "#F1F6F4", 700, 790)
    b += text(72, 374, "再决定是否值得。", 72, MINT, 700, 790)
    b += text(76, 452, "拒绝迎合 · 拒绝硬凑五五开 · 允许结论反转", 29, "#BCD0D6", width=800)
    for i, (n, title, subtitle, color) in enumerate([
        ("01", "反对者", "拆假设，找盲区", CORAL),
        ("02", "支持者", "建立最强理由", BLUE),
        ("03", "裁决者", "按证据给出建议", MINT),
    ]):
        y = 174 + i * 128
        b += rect(948, y, 420, 108, "#193B47", "#31505A", 12)
        b += text(972, y + 44, n, 24, color, 600, mono=True)
        b += text(1040, y + 44, title, 32, "#F1F6F4", 700, 294)
        b += text(1040, y + 80, subtitle, 23, "#BCD0D6", width=294)
    b += line(72, 564, 1368, 564, "#31505A")
    for x, a, c in [(72, "可核查的理由", "不是情绪化唱反调"), (520, "明确的倾向", "不是优缺点堆砌"), (968, "可执行的下一步", "不是一句谨慎考虑")]:
        b += text(x, 626, a, 31, "#F1F6F4", 600, 400)
        b += text(x, 668, c, 24, "#BCD0D6", width=400)
    items.append(("01-hero", "重大决策前，先让 AI 全力唱反调", "先全力反驳，再建立最强支持，最后按证据裁决并给出下一步。", b, 740, DARK))

    b = header("02", "PROCESS", "让三个视角依次发言", "顺序固定，结论开放。先检查，再判断。")
    labels = [("00", "界定决策", ["目标与底线", "替代与期限"], "#E7EEEB"),
              ("01", "全力反驳", ["遗漏与假设", "损失与偏差"], "#F7E7DE"),
              ("02", "最强支持", ["真实的优势", "成立的条件"], "#E1EDF8"),
              ("03", "证据裁决", ["哪边占优势", "最大未知项"], "#DBF0E7"),
              ("04", "行动与反转", ["最小的验证", "止损与复盘"], "#E7EEEB")]
    for i in range(4):
        b += line(72 + i * 264 + 228, 360, 72 + (i + 1) * 264 - 12, 360, MUTED, arrow=True)
    for i, (n, title, rows, fill) in enumerate(labels):
        x = 72 + i * 264
        b += rect(x, 260, 228, 248, fill, r=12)
        b += text(x + 24, 304, n, 25, TEAL, 600, mono=True)
        b += text(x + 24, 362, title, 29, INK, 700, 186)
        b += text(x + 24, 422, rows[0], 25, MUTED, width=184)
        b += text(x + 24, 464, rows[1], 25, MUTED, width=184)
    b += text(72, 600, "先反驳，不代表最后必须反对。", 37, TEAL, 700, 1250)
    b += text(72, 656, "新证据出现时，更新判断；不维护旧结论。", 28, MUTED, width=1250)
    b += footer("中性界定可以在前；背书和最终建议必须在证据审查之后。")
    items.append(("02-workflow", "五步决策审查流程", "中性界定后，依次反驳、支持、证据裁决，最后给出行动和反转条件。", b, 800, PAPER))

    b = header("03", "BLIND SPOTS", "决定之前，照亮六类盲区", "把反对意见落到事实、损失路径与可验证的信号。")
    data = [("01", "遗漏信息", "什么未知会改变判断？"), ("02", "乐观假设", "哪些前提还没有被证实？"), ("03", "不可逆成本", "哪些投入很难再拿回来？"), ("04", "机会成本", "最好的可行替代是什么？"), ("05", "最坏可信风险", "怎样失败，会损失到哪里？"), ("06", "情绪与偏差", "有证据，还是怕错过？")]
    for i, (n, title, sub) in enumerate(data):
        x, y = 72 + (i % 3) * 440, 244 + (i // 3) * 190
        b += rect(x, y, 416, 166, "white", LINE, 12)
        b += text(x + 24, y + 46, n, 23, TEAL, 600, mono=True)
        b += text(x + 78, y + 48, title, 30, INK, 700, 308)
        b += text(x + 24, y + 113, sub, 25, MUTED, width=368)
    b += rect(72, 628, 1296, 64, "#DBF0E7", r=8)
    b += text(96, 670, "再补两问：执行依赖可靠吗？一直不行动会失去什么？", 27, TEAL, 600, 1248)
    b += footer("质疑推理，不评判人格；关注可信风险，不编造灾难。")
    items.append(("03-blindspots", "重大决策的六类盲区", "检查遗漏、乐观假设、不可逆成本、机会成本、最坏风险和偏差，并补查执行与不行动代价。", b, 800, PAPER))

    b = header("04", "EVIDENCE", "一项硬约束，可能胜过五条弱理由", "按证据分量裁决。观点多，不等于证据强。")
    b += rect(72, 248, 576, 326, "#F7E7DE", r=12)
    b += text(104, 304, "关键反对证据", 32, INK, 700, 510)
    b += text(104, 372, "将突破用户明确的损失底线", 29, INK, 600, 510)
    b += text(104, 428, "直接相关 · 能核查 · 后果重大", 25, MUTED, width=510)
    b += rect(104, 478, 180, 50, "#E8B39B", r=8)
    b += text(125, 513, "高决策权重", 25, INK, 600, 140)
    b += text(688, 428, "vs", 34, MUTED, 500, mono=True)
    b += rect(776, 248, 592, 326, "#E1EDF8", r=12)
    b += text(808, 304, "多条支持观点", 32, INK, 700, 528)
    for i, v in enumerate(["朋友很看好", "网上有成功故事", "自己非常想做"]):
        b += dot(816, 360 + i * 49, "#6093BE", 5)
        b += text(840, 370 + i * 49, v, 28, MUTED, width=480)
    b += text(808, 539, "这些还不能证明收益能够兑现", 25, MUTED, width=528)
    b += text(72, 639, "裁决：先守住底线，再验证收益。", 38, TEAL, 700, 1296)
    b += text(72, 688, "示意案例，不是通用评分公式；事实变化时结论也要变化。", 25, MUTED, width=1296)
    b += footer("硬约束不能靠平均分抵消；没有数据，不编成功概率。", 820)
    items.append(("04-evidence", "证据权重优于观点计数", "在示意案例中，突破明确损失底线的事实比多条尚未验证的支持观点更能决定结论。", b, 820, PAPER))

    b = header("05", "REVERSAL", "提前说清楚：什么会让我改主意", "把“看情况”写成可观察的条件。", dark=True)
    b += rect(72, 282, 340, 238, "#193B47", "#31505A", 12)
    b += text(104, 334, "当前判断", 25, "#BCD0D6", width=272)
    b += text(104, 393, "先小规模验证", 34, "#F1F6F4", 700, 276)
    b += text(104, 451, "保留资金与退出选择", 24, "#BCD0D6", width=276)
    b += line(412, 400, 484, 400, "#BCD0D6", arrow=True)
    b += rect(504, 314, 294, 174, "#244D59", r=12)
    b += text(532, 363, "收到新证据", 30, "#F1F6F4", 700, 238)
    b += text(532, 408, "与预先标准比较", 26, "#BCD0D6", width=238)
    b += text(532, 452, "标准需有依据", 23, "#BCD0D6", width=238)
    # A single explicit branching junction with separated outgoing routes.
    b += '<path d="M798,400 H854 M854,278 V550 M854,278 H908 M854,414 H908 M854,550 H908" fill="none" stroke="#BCD0D6" stroke-width="2"/>'
    b += dot(854, 400, MINT, 5)
    for y, title, sub, color in [(234, "支持条件得到验证", "可考虑推进下一阶段", MINT), (370, "证据仍不能区分", "只做能改判的补充验证", BLUE), (506, "触发底线或止损", "暂停、缩小或退出", CORAL)]:
        b += rect(912, y, 456, 104, "#193B47", "#31505A", 10)
        b += rect(912, y, 6, 104, color, r=0)
        b += text(942, y + 43, title, 29, color, 700, 392)
        b += text(942, y + 81, sub, 24, "#BCD0D6", width=392)
    b += text(72, 680, "目标变了，也要重开评估。", 31, MINT, 600, 1200)
    b += footer("条件 → 可观察标准 → 结论变化 → 对应行动", dark=True)
    items.append(("05-reversal", "双向结论反转条件", "把新证据与预先说明的标准比较，分别触发推进、必要验证或暂停退出。", b, 800, DARK))

    b = header("06", "EXAMPLE", "有限的试行，也值得先唱反调", "虚构案例 / 两人 · 两周 · 费用上限 500 元 · 可退出")
    rows = [("01  反驳", "离线样本不等于实际流程", "复核、返工和维护，可能吃掉节省的时间。", "#F7E7DE"),
            ("02  支持", "有限投入能换来关键的信息", "有方向性证据，费用和期限清楚，也能退出。", "#E1EDF8"),
            ("03  裁决", "支持附条件试行", "测人工净耗时和质量；暂不据此全面推广。", "#DBF0E7")]
    for i, (tag, title, sub, fill) in enumerate(rows):
        y = 240 + i * 148
        b += rect(72, y, 1296, 124, fill, r=12)
        b += text(100, y + 52, tag, 28, TEAL, 700, 225)
        b += text(354, y + 48, title, 32, INK, 700, 974)
        b += text(354, y + 93, sub, 26, MUTED, width=974)
    b += footer("第一阶段挑问题；最终建议仍然可以是“做”。")
    items.append(("06-example", "内部工具试行的虚构示例", "反驳样本外推，支持有限试验的学习价值，最后有条件推进并测量净人时和质量。", b, 800, PAPER))

    b = header("07", "DECISION CARD", "带走一张能执行的决策卡", "从“分析过了”，走到“知道下一步做什么”。")
    b += rect(72, 242, 1296, 402, "white", LINE, 12)
    for i, (a, v) in enumerate([
        ("当前建议", "哪一边占优，选择哪个方案"),
        ("决定性证据", "真正决定结论的 1–3 项依据"),
        ("信心与未知", "为什么有把握，什么仍可能改判"),
        ("反转条件", "观察到什么，就转向推进或退出"),
        ("行动边界", "验证什么，投入多少，何时复盘"),
        ("现在的下一步", "今天就能执行的一个具体动作"),
    ]):
        y = 290 + i * 62
        b += text(104, y, a, 27, TEAL, 600, 266)
        b += text(398, y, v, 28, INK, width=920)
        if i < 5:
            b += line(104, y + 22, 1336, y + 22, LINE, 1)
    b += text(72, 698, "不保证结果，帮助你把决定做得更清楚。", 31, TEAL, 600, 1296)
    b += footer("保留理由，跟踪变化；复盘时区分决策过程与最终结果。", 830)
    items.append(("07-decision-card", "可执行的决策卡", "记录当前建议、关键证据、信心与未知、双向反转条件、投入边界和下一步。", b, 830, PAPER))
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, title, desc, body, h, bg in items:
        (OUT / f"{slug}.svg").write_text(document(slug, title, desc, body, h, bg), encoding="utf-8")
    return items


def render(items):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": W, "height": 900}, device_scale_factor=1)
        page.route("http://**/*", lambda route: route.abort())
        page.route("https://**/*", lambda route: route.abort())
        for slug, _, _, _, h, _ in items:
            svg = (OUT / f"{slug}.svg").read_text(encoding="utf-8")
            page.set_viewport_size({"width": W, "height": h})
            page.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>body{{margin:0}}svg{{display:block}}</style></head><body>{svg}</body></html>')
            page.evaluate("document.fonts.ready")
            errors = page.evaluate('''() => [...document.querySelectorAll('text')].flatMap(t => {
                const b = t.getBBox(); const limit = Number(t.dataset.maxWidth || 99999);
                const s = document.querySelector('svg').viewBox.baseVal;
                return b.width > limit + 1 || b.x < 0 || b.y < 0 || b.x+b.width > s.width || b.y+b.height > s.height
                    ? [{text:t.textContent, width:b.width, limit, x:b.x, y:b.y}] : [];
            })''')
            if errors:
                raise ValueError(f"Text overflow in {slug}: {errors}")
            page.locator("svg").screenshot(path=str(OUT / f"{slug}.png"))
            print(f"Rendered {slug}.png ({W} x {h}); no text overflow")
        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args()
    diagrams = build()
    print(f"Built {len(diagrams)} editable SVGs")
    if args.render:
        render(diagrams)
