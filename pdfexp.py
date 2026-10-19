"""Söhbəti PDF-ə çevirir (reportlab) və cavablardan LaTeX düsturlarını çıxarır."""
import os
import re
import html
import io

_HERE = os.path.dirname(os.path.abspath(__file__))
_FD = os.path.join(_HERE, "fonts")
_REG = False
BODY, BOLD, ITAL, BOLDI, MONO = "DVSans", "DVSans-Bold", "DVSans-Oblique", "DVSans-BoldOblique", "DVMono"


_WIN = r"C:\\Windows\\Fonts"
_DJV = "/usr/share/fonts/truetype/dejavu"
# rol -> namizəd fayllar (ilk tapılan götürülür). ə ı ş ğ üçün Arial və DejaVu uyğundur.
_CAND = {
    "reg": [os.path.join(_FD, "DejaVuSans.ttf"), os.path.join(_DJV, "DejaVuSans.ttf"), os.path.join(_WIN, "arial.ttf"),
            os.path.join(_WIN, "segoeui.ttf")],
    "bold": [os.path.join(_FD, "DejaVuSans-Bold.ttf"), os.path.join(_DJV, "DejaVuSans-Bold.ttf"), os.path.join(_WIN, "arialbd.ttf"),
             os.path.join(_WIN, "segoeuib.ttf")],
    "ital": [os.path.join(_FD, "DejaVuSans-Oblique.ttf"), os.path.join(_DJV, "DejaVuSans-Oblique.ttf"), os.path.join(_WIN, "ariali.ttf"),
             os.path.join(_WIN, "segoeuii.ttf")],
    "boldi": [os.path.join(_FD, "DejaVuSans-BoldOblique.ttf"), os.path.join(_DJV, "DejaVuSans-BoldOblique.ttf"),
              os.path.join(_WIN, "arialbi.ttf"), os.path.join(_WIN, "segoeuiz.ttf")],
    "mono": [os.path.join(_FD, "DejaVuSansMono.ttf"), os.path.join(_DJV, "DejaVuSansMono.ttf"), os.path.join(_WIN, "consola.ttf"),
             os.path.join(_WIN, "cour.ttf")],
}


def _fonts():
    """Unicode şriftləri tapıb qeydiyyatdan keçirir (ə, ı, ş, ğ üçün lazımdır). Heç biri yoxdursa Helvetica."""
    global _REG, BODY, BOLD, ITAL, BOLDI, MONO
    if _REG:
        return
    _REG = True
    try:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.fonts import addMapping
        found = {r: next((f for f in c if os.path.isfile(f)), None) for r, c in _CAND.items()}
        if not found["reg"]:
            raise FileNotFoundError("no unicode font")
        for role, name in (("reg", "DVSans"), ("bold", "DVSans-Bold"), ("ital", "DVSans-Oblique"),
                           ("boldi", "DVSans-BoldOblique"), ("mono", "DVMono")):
            pdfmetrics.registerFont(TTFont(name, found[role] or found["reg"]))
        addMapping("DVSans", 0, 0, "DVSans")
        addMapping("DVSans", 1, 0, "DVSans-Bold")
        addMapping("DVSans", 0, 1, "DVSans-Oblique")
        addMapping("DVSans", 1, 1, "DVSans-BoldOblique")
    except Exception:
        BODY, BOLD, ITAL, BOLDI, MONO = "Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Helvetica-BoldOblique", "Courier"


def _clean(s):
    """Emoji və digər BMP-xarici simvolları, idarəedici işarələri silir (şriftdə yoxdur, kvadrat çıxır)."""
    s = re.sub(r"[\U00010000-\U0010FFFF‍️]", "", s or "")
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", s)


_MATH = re.compile(r"\$\$(.+?)\$\$|\\\[(.+?)\\\]|\\\((.+?)\\\)|(?<![\\$\w])\$(?!\s)([^$\n]+?)(?<!\s)\$(?![\w$])", re.S)


def extract_latex(text):
    """Mətndəki düsturları (kod blokları xaric) təkrarsız siyahı kimi qaytarır."""
    text = re.sub(r"```.*?```", " ", text or "", flags=re.S)
    out = []
    for m in _MATH.finditer(text):
        f = next((g for g in m.groups() if g), "").strip()
        if f and f not in out:
            out.append(f)
    return out


def _inline(s):
    """Bir sətir markdown -> reportlab işarələməsi. Kod/düstur ilkin çıxarılır ki, ulduz və s. pozmasın."""
    keep = []

    def stash(m):
        body = next((g for g in m.groups() if g is not None), "")
        keep.append(body)
        return f"\x01{len(keep) - 1}\x02"

    s = re.sub(r"`([^`]+)`", stash, s)
    s = _MATH.sub(stash, s)
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)([^*]+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r"\1", s)
    return re.sub(r"\x01(\d+)\x02",
                  lambda m: f'<font name="{MONO}" size="9">{html.escape(keep[int(m.group(1))], quote=False)}</font>', s)


def chat_pdf(chat, title, who_user="Sual", who_ai="Cavab"):
    """chat: {"messages": [{"role","content"}]}. PDF baytlarını qaytarır."""
    _fonts()
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, KeepTogether

    base = ParagraphStyle("b", fontName=BODY, fontSize=10.5, leading=15, spaceAfter=4)
    h_ttl = ParagraphStyle("t", parent=base, fontName=BOLD, fontSize=18, leading=22, spaceAfter=10)
    h_who = ParagraphStyle("w", parent=base, fontName=BOLD, fontSize=11, leading=14, spaceBefore=10,
                           textColor=colors.HexColor("#0f766e"))
    h_md = ParagraphStyle("h", parent=base, fontName=BOLD, fontSize=12.5, leading=16, spaceBefore=6)
    bullet = ParagraphStyle("li", parent=base, leftIndent=14, bulletIndent=3)
    code = ParagraphStyle("c", fontName=MONO, fontSize=8.5, leading=11, backColor=colors.HexColor("#f1f5f9"),
                          borderPadding=4, spaceBefore=3, spaceAfter=6)

    def para(txt, style):
        try:
            return Paragraph(_inline(_clean(txt)), style)
        except Exception:
            return Paragraph(html.escape(_clean(txt), quote=False), style)

    def wrap(line, n=95):
        return "\n".join(line[i:i + n] for i in range(0, len(line), n)) if len(line) > n else line

    story = [para(title or "Tutor", h_ttl)]
    for m in (chat or {}).get("messages", []):
        story.append(para(who_user if m.get("role") == "user" else who_ai, h_who))
        in_code, buf = False, []
        for raw in str(m.get("content", "")).replace("\r", "").split("\n"):
            if raw.strip().startswith("```"):
                if in_code and buf:
                    story.append(Preformatted(_clean("\n".join(wrap(x) for x in buf)), code))
                in_code, buf = not in_code, []
                continue
            if in_code:
                buf.append(raw.replace("\t", "    "))
                continue
            line = raw.rstrip()
            if not line.strip():
                story.append(Spacer(1, 3))
            elif re.match(r"^\s*\|", line):
                if not re.match(r"^\s*\|[\s:|-]+\|?\s*$", line):
                    story.append(Preformatted(_clean(wrap(line.strip())), code))
            elif re.match(r"^#{1,6}\s", line):
                story.append(para(re.sub(r"^#+\s*", "", line), h_md))
            elif re.match(r"^\s*([-*•]|\d+[.)])\s+", line):
                mark = re.match(r"^\s*([-*•]|\d+[.)])\s+", line).group(1)
                story.append(para(re.sub(r"^\s*([-*•]|\d+[.)])\s+", "", line), ParagraphStyle(
                    "l", parent=bullet, bulletFontName=BODY)))
                story[-1].bulletText = "•" if mark in "-*•" else mark
            else:
                story.append(para(line, base))
        if in_code and buf:
            story.append(Preformatted(_clean("\n".join(wrap(x) for x in buf)), code))
    buf_io = io.BytesIO()
    doc = SimpleDocTemplate(buf_io, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=16 * mm, bottomMargin=16 * mm, title=_clean(title or "Tutor")[:100])
    doc.build(story)
    return buf_io.getvalue()