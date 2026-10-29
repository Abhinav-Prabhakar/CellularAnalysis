"""Minimal typesetting engine that reproduces the assignment report template.

Geometry measured from the reference document:
  A4 595.44 x 841.92 pt, page border rect (24, 24) - (571.68, 817.68), stroke 0.48 pt
  text column x = 90 .. 550 (460 pt), first line top y = 71, last line bottom y = 768
  footer page number centred on 297.7, baseline 793.2, Calibri (Carlito) 11 pt

Inline markup:  **bold**  *italic*  ***bold italic***  ~subscript~  ^superscript^
"""
import os
import re

import pymupdf
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(os.path.dirname(HERE), "report_assets")
TNR_DIR = "/System/Library/Fonts/Supplemental"

PAGE_W, PAGE_H = 595.44, 841.92
BORDER = pymupdf.Rect(24, 24, 571.68, 817.68)
LEFT, RIGHT = 90.0, 550.0
WIDTH = RIGHT - LEFT
TOP, BOTTOM = 71.0, 768.0
PAGENO_BASELINE = 793.2
BLACK = (0, 0, 0)


def _font(path):
    return pymupdf.Font(fontfile=path)


def _coverage(path):
    return set(TTFont(path).getBestCmap().keys())


ALIASES = str.maketrans({"₀": "~0~", "₁": "~1~", "₂": "~2~", "₃": "~3~", "₄": "~4~",
                         "⁰": "^0^", "¹": "^1^", "²": "^2^", "³": "^3^", "⁴": "^4^",
                         "⁻": "^-^", "⁵": "^5^", "⁶": "^6^", "⁷": "^7^", "⁸": "^8^",
                         "⁹": "^9^"})


class Engine:
    def __init__(self):
        self.regular = _font(os.path.join(FONT_DIR, "Caladea-Regular.ttf"))
        self.bold = _font(os.path.join(FONT_DIR, "Caladea-Bold.ttf"))
        self.italic = _font(os.path.join(FONT_DIR, "Caladea-Italic.ttf"))
        self.bolditalic = _font(os.path.join(FONT_DIR, "Caladea-BoldItalic.ttf"))
        self.fallback = {
            0: _font(os.path.join(TNR_DIR, "Times New Roman.ttf")),
            1: _font(os.path.join(TNR_DIR, "Times New Roman Bold.ttf")),
            2: _font(os.path.join(TNR_DIR, "Times New Roman Italic.ttf")),
            3: _font(os.path.join(TNR_DIR, "Times New Roman Bold Italic.ttf")),
        }
        self.mono = pymupdf.Font("cour")
        self.cov = _coverage(os.path.join(FONT_DIR, "Caladea-Regular.ttf"))
        self.doc = pymupdf.open()
        self.page = None
        self.tw = None
        self.y = TOP
        self.page_no = 0
        self.seq = 0

    # ---------------------------------------------------------------- pages
    def new_page(self):
        if self.page is not None:
            self.end_page()
        self.page = self.doc.new_page(width=PAGE_W, height=PAGE_H)
        self.page.draw_rect(BORDER, color=BLACK, width=0.48)
        self.tw = pymupdf.TextWriter(pymupdf.Rect(0, 0, PAGE_W, PAGE_H))
        self.page_no += 1
        self.y = TOP

    def end_page(self):
        if self.page is None:
            return
        self.tw.write_text(self.page, color=BLACK)
        label = str(self.page_no)
        w = self._carlito_len(label)
        self.page.insert_text((297.7 - w / 2, PAGENO_BASELINE), label, fontsize=11,
                              fontname="carl",
                              fontfile=os.path.join(FONT_DIR, "Carlito-Regular.ttf"))
        self.page = None
        self.tw = None

    def _carlito_len(self, s):
        return _font(os.path.join(FONT_DIR, "Carlito-Regular.ttf")).text_length(s, 11)

    def save(self, path):
        self.end_page()
        try:
            self.doc.subset_fonts(verbose=False)
        except Exception:
            pass
        self.doc.save(path, garbage=3, deflate=True)
        self.doc.close()

    # -------------------------------------------------------- rich parsing
    @staticmethod
    def parse(text):
        """Return words, each a list of (chunk, style, script) pieces."""
        text = text.translate(ALIASES)
        segments = []
        pattern = re.compile(r"(\*\*\*.+?\*\*\*|\*\*.+?\*\*|\*.+?\*|~[^~]+?~|\^[^\^]+?\^)")
        pos = 0
        for m in pattern.finditer(text):
            if m.start() > pos:
                segments.append((text[pos:m.start()], 0, 0))
            core = m.group(1)
            if core.startswith("***"):
                segments.append((core[3:-3], 3, 0))
            elif core.startswith("**"):
                segments.append((core[2:-2], 1, 0))
            elif core.startswith("*"):
                segments.append((core[1:-1], 2, 0))
            elif core.startswith("~"):
                segments.append((core[1:-1], 0, -1))
            else:
                segments.append((core[1:-1], 0, 1))
            pos = m.end()
        if pos < len(text):
            segments.append((text[pos:], 0, 0))

        words, cur = [], []
        for seg, style, script in segments:
            for chunk in re.split(r"(\s+)", seg):
                if not chunk:
                    continue
                if chunk.isspace():
                    if cur:
                        words.append(cur)
                        cur = []
                else:
                    cur.append((chunk, style, script))
        if cur:
            words.append(cur)
        return words

    def _face(self, style):
        return {0: self.regular, 1: self.bold, 2: self.italic, 3: self.bolditalic}[style]

    def _segments(self, piece, size):
        """Split a piece into drawable runs with per-character font fallback."""
        text, style, script = piece
        scale = 1.0 if script == 0 else 0.63
        fs = size * scale
        face = self._face(style)
        fb = self.fallback[style]
        runs, cur, cur_face = [], "", face
        for ch in text:
            f = face if ord(ch) in self.cov else fb
            if f is not cur_face and cur:
                runs.append((cur, cur_face, fs))
                cur = ""
            cur_face = f
            cur += ch
        if cur:
            runs.append((cur, cur_face, fs))
        return runs

    def piece_width(self, piece, size):
        return sum(f.text_length(t, fs) for t, f, fs in self._segments(piece, size))

    def word_width(self, word, size):
        return sum(self.piece_width(p, size) for p in word)

    def line_width(self, line, size):
        space = self.regular.text_length(" ", size)
        return sum(self.word_width(w, size) for w in line) + space * (len(line) - 1)

    def draw_word(self, word, x, baseline, size):
        for piece in word:
            text, style, script = piece
            dy = {0: 0.0, 1: -0.30 * size, -1: 0.16 * size}[script]
            for run, face, fs in self._segments(piece, size):
                self.tw.append((x, baseline + dy), run, font=face, fontsize=fs)
                x += face.text_length(run, fs)
        return x

    def draw_line(self, line, baseline, size, align="left", x0=LEFT, width=WIDTH):
        space = self.regular.text_length(" ", size)
        total = self.line_width(line, size)
        if align == "center":
            x, gap = x0 + (width - total) / 2, space
        elif align == "right":
            x, gap = x0 + width - total, space
        elif align == "justify" and len(line) > 1:
            x, gap = x0, space + (width - total) / (len(line) - 1)
        else:
            x, gap = x0, space
        for word in line:
            x = self.draw_word(word, x, baseline, size)
            x += gap

    # ------------------------------------------------------------- blocks
    def wrap(self, words, size, width, indent_first=0.0, indent_rest=0.0):
        lines, cur, cur_w = [], [], 0.0
        limit = width - indent_first
        space = self.regular.text_length(" ", size)
        for w in words:
            ww = self.word_width(w, size)
            add = ww if not cur else space + ww
            if cur and cur_w + add > limit + 0.01:
                lines.append(cur)
                cur, cur_w = [w], ww
                limit = width - indent_rest
            else:
                cur.append(w)
                cur_w += add
        if cur:
            lines.append(cur)
        return lines

    def para(self, text, size=12.57, leading=21.1, align="justify", x0=LEFT,
             width=WIDTH, indent_first=0.0, indent_rest=0.0, space_before=0.0,
             space_after=0.0, keep_together=False, last_left=True):
        self.y += space_before
        words = self.parse(text)
        if not words:
            self.y += space_after
            return
        lines = self.wrap(words, size, width, indent_first, indent_rest)
        if keep_together and self.y + leading * len(lines) > BOTTOM:
            self.new_page()
        asc = self.regular.ascender * size
        for i, line in enumerate(lines):
            ind = indent_first if i == 0 else indent_rest
            if self.y + leading > BOTTOM + 1:
                self.new_page()
            baseline = self.y + asc
            last = i == len(lines) - 1
            self.draw_line(line, baseline, size,
                           align="left" if (last and last_left) else align,
                           x0=x0 + ind, width=width - ind)
            self.y += leading
        self.y += space_after

    def code_line(self, text, size=10.2, leading=16.0, centre=(LEFT + RIGHT) / 2,
                  space_before=4.0, space_after=10.0, x0=None):
        """Monospaced line, centred by default or left-aligned when x0 is given."""
        if self.y + space_before + leading > BOTTOM + 1:
            self.new_page()
        self.y += space_before
        w = self.mono.text_length(text, size)
        baseline = self.y + self.regular.ascender * size
        x = (centre - w / 2) if x0 is None else x0
        self.tw.append((x, baseline), text, font=self.mono, fontsize=size)
        self.y += leading + space_after

    def raw(self, text, size=9.6, leading=12.4, x0=LEFT, space_after=0.0):
        """Monospaced line drawn verbatim, with no inline markup."""
        if self.y + leading > BOTTOM + 1:
            self.new_page()
        if text.strip():
            baseline = self.y + self.regular.ascender * size
            self.tw.append((x0, baseline), text, font=self.mono, fontsize=size)
        self.y += leading + space_after

    def text_at(self, x, y_top, text, size, style=0, align="left", width=None):
        """Single line of text placed explicitly (headings, title page)."""
        words = self.parse(text)
        line = [w for w in words]
        baseline = y_top + self.regular.ascender * size
        if align == "center":
            total = sum(self.word_width(w, size) for w in line) + \
                self.regular.text_length(" ", size) * (len(line) - 1)
            self.draw_line(line, baseline, size, "left", x0=x - total / 2, width=total + 1)
        elif align == "right":
            total = sum(self.word_width(w, size) for w in line) + \
                self.regular.text_length(" ", size) * (len(line) - 1)
            self.draw_line(line, baseline, size, "left", x0=x - total, width=total + 1)
        else:
            self.draw_line(line, baseline, size, "left", x0=x, width=width or WIDTH)

    def line(self, y, x0=LEFT, x1=RIGHT, grey=0.7, width=0.6):
        self.page.draw_line((x0, y), (x1, y), color=(grey, grey, grey), width=width)

    def image(self, path, width, gap=8.0, centre=(LEFT + RIGHT) / 2):
        pix = pymupdf.Pixmap(path)
        h = width * pix.height / pix.width
        if self.y + gap + h > BOTTOM:
            self.new_page()
        self.y += gap
        x0 = centre - width / 2
        self.page.insert_image(pymupdf.Rect(x0, self.y, x0 + width, self.y + h), filename=path)
        self.y += h
