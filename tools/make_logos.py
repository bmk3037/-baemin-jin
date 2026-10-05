"""배민진컴퍼니 로고 SVG 생성기.

글자는 Pretendard(SIL OFL)에서 윤곽선(path)으로 뽑아 넣기 때문에,
SVG를 여는 컴퓨터에 글꼴이 없어도 똑같이 보입니다.

    pip install fonttools
    python tools/make_logos.py path/to/Pretendard-Black.otf path/to/Pretendard-Bold.otf
"""
import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

NAVY, ORANGE, IVORY, INK, WHITE = "#142454", "#FF5B14", "#F6F2E9", "#0D1530", "#FFFFFF"
OUT = Path(__file__).resolve().parent.parent / "brand" / "logo"

# ㅂ 심볼 (100×100 격자). 위가 열린 그릇 + 두 기둥을 잇는 가로획.
B_OUTER = "M24 20H41V41H59V20H76V80H24Z"
B_HOLE = "M41 54H59V66H41Z"
SQUARE = "M22 0H78A22 22 0 0 1 100 22V78A22 22 0 0 1 78 100H22A22 22 0 0 1 0 78V22A22 22 0 0 1 22 0Z"


def symbol(bg, fg, x=0.0, s=1.0):
    t = f'transform="translate({x:g} 0) scale({s:g})"'
    if fg is None:  # 단색: 사각형에서 ㅂ을 뚫어냄
        return f'<path {t} fill="{bg}" fill-rule="evenodd" d="{SQUARE}{B_OUTER}{B_HOLE}"/>'
    return (f'<g {t}><path fill="{bg}" d="{SQUARE}"/>'
            f'<path fill="{fg}" fill-rule="evenodd" d="{B_OUTER}{B_HOLE}"/></g>')


def text_path(font, text, x, baseline, size, tracking=0.0):
    """text를 path d 문자열로. tracking은 em 단위 자간. (d, 끝 x) 반환."""
    gs, cmap = font.getGlyphSet(), font.getBestCmap()
    upm = font["head"].unitsPerEm
    k = size / upm
    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
    cur = x
    for i, ch in enumerate(text):
        g = gs[cmap[ord(ch)]]
        g.draw(TransformPen(pen, (k, 0, 0, -k, cur, baseline)))
        cur += g.width * k + (tracking * size if i < len(text) - 1 else 0)
    return pen.getCommands(), cur


def svg(w, h, label, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" role="img" '
            f'aria-label="{label}"><title>{label}</title>{body}</svg>\n')


def write(name, content):
    (OUT / name).write_text(content, encoding="utf-8")
    print("wrote", name)


def main(black_path, bold_path):
    black, bold = TTFont(black_path), TTFont(bold_path)
    OUT.mkdir(parents=True, exist_ok=True)

    # 심볼
    write("symbol.svg", svg(100, 100, "배민진컴퍼니", symbol(NAVY, ORANGE)))
    write("symbol-on-dark.svg", svg(100, 100, "배민진컴퍼니", symbol(ORANGE, NAVY)))
    write("symbol-mono-black.svg", svg(100, 100, "배민진컴퍼니", symbol(INK, None)))
    write("symbol-mono-white.svg", svg(100, 100, "배민진컴퍼니", symbol(WHITE, None)))

    # 가로형: 심볼 + 국문(배민진 / 컴퍼니) + 영문 한 줄
    x0 = 124
    d1, x1 = text_path(black, "배민진", x0, 60, 60, -0.02)
    d2, x2 = text_path(black, "컴퍼니", x1 + 6, 60, 60, -0.02)
    d3, x3 = text_path(bold, "BAEMINJIN COMPANY", x0 + 2, 92, 17, 0.22)
    w = max(x2, x3) + 4

    def horizontal(sym_bg, sym_fg, c1, c2, c3):
        return (symbol(sym_bg, sym_fg) + f'<path fill="{c1}" d="{d1}"/>'
                f'<path fill="{c2}" d="{d2}"/><path fill="{c3}" d="{d3}"/>')

    write("logo-horizontal-on-light.svg", svg(w, 100, "배민진컴퍼니", horizontal(NAVY, ORANGE, NAVY, ORANGE, NAVY)))
    write("logo-horizontal-on-dark.svg", svg(w, 100, "배민진컴퍼니", horizontal(ORANGE, NAVY, IVORY, ORANGE, IVORY)))
    write("logo-horizontal-mono-black.svg", svg(w, 100, "배민진컴퍼니", horizontal(INK, None, INK, INK, INK)))
    write("logo-horizontal-mono-white.svg", svg(w, 100, "배민진컴퍼니", horizontal(WHITE, None, WHITE, WHITE, WHITE)))

    # 국문 워드마크 단독
    k1, kx1 = text_path(black, "배민진", 0, 64, 72, -0.02)
    k2, kx2 = text_path(black, "컴퍼니", kx1 + 7, 64, 72, -0.02)
    for name, c1 in (("wordmark-kr-on-light.svg", NAVY), ("wordmark-kr-on-dark.svg", IVORY)):
        write(name, svg(kx2 + 2, 80, "배민진컴퍼니",
                        f'<path fill="{c1}" d="{k1}"/><path fill="{ORANGE}" d="{k2}"/>'))


if __name__ == "__main__":
    main(*sys.argv[1:3])
