#!/usr/bin/env python3
"""
build.py — Creative Communicator index.md → index.html

index.md를 수정한 뒤 이 스크립트를 실행하면 _template.html에 데이터를 채워
index.html을 새로 만든다. 표준 라이브러리만 사용.

Usage:
    cd ~/Desktop/creative-communicator
    python3 build.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "index.md"
TEMPLATE = ROOT / "_template.html"
OUT = ROOT / "index.html"


# ---------- Markdown → HTML (limited inline) ----------

def md_inline(text: str) -> str:
    """**bold**, [text](url) 만 변환. 나머지 인라인 HTML(<em>, <br/>)은 보존."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(
        r'\[([^\]]+)\]\(([^)]+)\)',
        r'<a href="\2" target="_blank" rel="noopener">\1</a>',
        text,
    )
    return text


def md_paragraphs(body: str) -> str:
    """빈 줄로 분리된 단락을 <p>...</p>로 감싼다."""
    parts = re.split(r'\n\s*\n', body.strip())
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        out.append(f"<p>{md_inline(p)}</p>")
    return "\n        ".join(out)


# ---------- Parser ----------

def parse_frontmatter(text: str):
    """--- 사이의 키:값 frontmatter 파싱."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm_block = parts[1].strip()
    body = parts[2].strip()
    meta = {}
    for line in fm_block.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip()
    return meta, body


def split_sections(body: str):
    """`# 제목` 단위로 본문을 섹션 dict로 분리."""
    sections = {}
    current = None
    buf = []
    for line in body.splitlines():
        m = re.match(r'^# (.+)$', line)
        if m:
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = m.group(1).strip()
            buf = []
        else:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return sections


def split_subsections(text: str):
    """`## 제목` 단위. 순서 유지를 위해 list[(heading, body)] 반환."""
    subs = []
    current = None
    buf = []
    for line in text.splitlines():
        m = re.match(r'^## (.+)$', line)
        if m:
            if current is not None:
                subs.append((current, "\n".join(buf).strip()))
            current = m.group(1).strip()
            buf = []
        else:
            buf.append(line)
    if current is not None:
        subs.append((current, "\n".join(buf).strip()))
    return subs


def parse_meta_lines(text: str):
    """본문 시작부의 `- key: value` 라인을 메타 dict로. 첫 빈 줄에서 종료."""
    meta = {}
    lines = text.splitlines()
    i = 0
    started = False
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped:
            if started:
                i += 1
                break
            i += 1
            continue
        m = re.match(r'^- ([\w\s.·]+?):\s*(.+)$', stripped)
        if m:
            meta[m.group(1).strip()] = m.group(2).strip()
            started = True
            i += 1
        else:
            break
    body = "\n".join(lines[i:]).strip()
    return meta, body


def get_subsection_body(section: str, sub_heading: str) -> str:
    for h, t in split_subsections(section):
        if h == sub_heading:
            return t.strip()
    return ""


# ---------- Renderers ----------

def render_about_cards(section: str) -> str:
    cards = []
    for heading, text in split_subsections(section):
        if not heading.startswith("Card"):
            continue
        meta, body = parse_meta_lines(text)
        title = meta.get("title", "")
        punch = meta.get("punch", "")
        body_html = md_paragraphs(body)
        cards.append(
            f'      <div class="about-card">\n'
            f'        <h3>{title}</h3>\n'
            f'        <div class="punch">{punch}</div>\n'
            f'        {body_html}\n'
            f'      </div>'
        )
    return "\n".join(cards)


def render_principles_cards(section: str) -> str:
    cards = []
    color_cls = {"accent": "", "teal": " c-tl", "purple": " c-pp"}
    n = 0
    for heading, text in split_subsections(section):
        if not heading.startswith("Card"):
            continue
        n += 1
        meta, body = parse_meta_lines(text)
        title = meta.get("title", "")
        cls = color_cls.get(meta.get("color", "accent"), "")
        body_html = md_paragraphs(body)
        cards.append(
            f'      <div class="principle-card{cls}">\n'
            f'        <div class="num">PRINCIPLE {n:02d}</div>\n'
            f'        <h4>{title}</h4>\n'
            f'        {body_html}\n'
            f'      </div>'
        )
    return "\n".join(cards)


def render_report_cards(section: str) -> str:
    color_cls = {
        "yellow": "c-yel", "pink": "c-pk", "teal": "c-tl", "purple": "c-pp",
        "blue": "c-bl", "green": "c-gr", "red": "c-rd",
        "accent": "c-ac", "dark": "c-dk",
    }
    cards = []
    for heading, text in split_subsections(section):
        if not heading.startswith("Part"):
            continue
        part_no = heading.strip()
        meta, body = parse_meta_lines(text)
        cls = color_cls.get(meta.get("color", "accent"), "c-ac")
        date = meta.get("date", "")
        file = meta.get("file", "#")
        title = meta.get("title", "")
        sub = meta.get("sub", "")
        meta_str = meta.get("meta", "")
        star = " ★" if meta.get("star", "").lower() == "true" else ""
        punch_html = md_inline(body.strip())
        cards.append(
            f'      <article class="report-card {cls}">\n'
            f'        <a href="{file}">\n'
            f'          <div class="meta-top">\n'
            f'            <span class="part-no">{part_no.upper()}{star}</span>\n'
            f'            <span class="pub-date">{date}</span>\n'
            f'          </div>\n'
            f'          <h3>{title}</h3>\n'
            f'          <div class="sub-en">{sub}</div>\n'
            f'          <p class="punch">{punch_html}</p>\n'
            f'          <div class="meta-bottom"><span>{meta_str}</span><span class="open">OPEN →</span></div>\n'
            f'        </a>\n'
            f'      </article>'
        )
    return "\n".join(cards)


def render_threads(section: str) -> str:
    items = []
    for heading, text in split_subsections(section):
        if not heading.startswith("Thread"):
            continue
        meta, body = parse_meta_lines(text)
        name = meta.get("name", "")
        parts = meta.get("parts", "")
        body_html = md_inline(body.strip())
        items.append(
            f'        <li>\n'
            f'          <span class="t-name">{name}</span>\n'
            f'          <div class="t-body">\n'
            f'            {body_html}\n'
            f'            <span class="t-parts">{parts}</span>\n'
            f'          </div>\n'
            f'        </li>'
        )
    return "\n".join(items)


def render_colophon_rows(section: str) -> str:
    rows = []
    for heading, text in split_subsections(section):
        if not heading.startswith("Row"):
            continue
        meta, body = parse_meta_lines(text)
        label = meta.get("label", "")
        body_html = md_inline(body.strip())
        rows.append(
            f'      <div class="col-row">\n'
            f'        <div class="col-label">{label}</div>\n'
            f'        <div class="col-content">{body_html}</div>\n'
            f'      </div>'
        )
    return "\n".join(rows)


def render_list_lines(section: str, sub_heading: str) -> str:
    """`- item` 형식 마크다운 리스트를 <li> 시퀀스로."""
    body = get_subsection_body(section, sub_heading)
    items = []
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("- "):
            items.append(f"        <li>{md_inline(line[2:])}</li>")
    return "\n".join(items)


# ---------- Main ----------

def main():
    if not SRC.exists():
        print(f"✗ {SRC} not found")
        return 1
    if not TEMPLATE.exists():
        print(f"✗ {TEMPLATE} not found")
        return 1

    text = SRC.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    sections = split_sections(body)

    HERO = sections.get("HERO", "")
    ABOUT = sections.get("ABOUT", "")
    PRINCIPLES = sections.get("PRINCIPLES", "")
    REPORTS = sections.get("REPORTS", "")
    THREADS = sections.get("THREADS", "")
    COLOPHON = sections.get("COLOPHON", "")
    FOOTER = sections.get("FOOTER", "")

    subs = {
        "TITLE": fm.get("title", "Creative Communicator"),
        "HERO_KICKER": fm.get("hero_kicker", ""),
        "HERO_H1": get_subsection_body(HERO, "H1"),
        "HERO_TAGLINE": fm.get("hero_tagline", ""),
        "HERO_LEAD": md_inline(get_subsection_body(HERO, "Lead")),
        "META_DURATION": fm.get("meta_duration", ""),
        "META_SPAN": fm.get("meta_span", ""),
        "META_FORMAT": fm.get("meta_format", ""),
        "META_AUTHOR": fm.get("meta_author", ""),
        "ABOUT_H2": get_subsection_body(ABOUT, "H2"),
        "ABOUT_LEAD": md_inline(get_subsection_body(ABOUT, "Lead")),
        "ABOUT_CARDS": render_about_cards(ABOUT),
        "PRINCIPLES_H2": get_subsection_body(PRINCIPLES, "H2"),
        "PRINCIPLES_LEAD": md_inline(get_subsection_body(PRINCIPLES, "Lead")),
        "PRINCIPLES_CARDS": render_principles_cards(PRINCIPLES),
        "REPORTS_SUB": get_subsection_body(REPORTS, "Sub"),
        "REPORTS_H2": get_subsection_body(REPORTS, "H2"),
        "REPORTS_LEAD": md_inline(get_subsection_body(REPORTS, "Lead")),
        "REPORT_CARDS": render_report_cards(REPORTS),
        "THREADS_H2": get_subsection_body(THREADS, "H2"),
        "THREADS_LEAD": md_inline(get_subsection_body(THREADS, "Lead")),
        "THREADS_LIST": render_threads(THREADS),
        "COLOPHON_H2": get_subsection_body(COLOPHON, "H2"),
        "COLOPHON_LEAD": md_inline(get_subsection_body(COLOPHON, "Lead")),
        "COLOPHON_ROWS": render_colophon_rows(COLOPHON),
        "COMMIT_BODY": md_inline(get_subsection_body(COLOPHON, "Commit")),
        "FOOTER_LEFT": md_inline(get_subsection_body(FOOTER, "Left")),
        "FOOTER_CONTACT": render_list_lines(FOOTER, "Contact"),
        "FOOTER_STACK": render_list_lines(FOOTER, "Stack"),
        "FOOTER_COPY": fm.get("footer_copy", ""),
        "FOOTER_VERSION": fm.get("footer_version", ""),
    }

    template = TEMPLATE.read_text(encoding="utf-8")
    for key, val in subs.items():
        template = template.replace("{{" + key + "}}", val)

    # 채우지 못한 placeholder 경고
    leftovers = re.findall(r'\{\{(\w+)\}\}', template)
    if leftovers:
        print(f"⚠ unfilled placeholders: {sorted(set(leftovers))}")

    OUT.write_text(template, encoding="utf-8")
    n_reports = sum(1 for h, _ in split_subsections(REPORTS) if h.startswith("Part"))
    print(f"✓ Built {OUT.name} ({len(template):,} bytes · {n_reports} reports)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
