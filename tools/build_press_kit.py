"""Rebuild the printable press kit and downloadable media archive."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "START HERE - Grimoire of Blanks Press Kit.pdf"
ARCHIVE = ROOT / "download/grimoire-of-blanks-press-kit-assets.zip"
W, H = A4
LEFT = 40
RIGHT = W - LEFT

NIGHT = colors.HexColor("#090508")
CARD = colors.HexColor("#1b0d13")
PAPER = colors.HexColor("#f1e5cc")
PALE = colors.HexColor("#fbf1dc")
TEAL = colors.HexColor("#41e4cf")
GOLD = colors.HexColor("#f4dfb8")
INK = colors.HexColor("#211a16")
MUTED = colors.HexColor("#736b5d")


def register_fonts():
    fonts = ROOT / "assets/fonts"
    pdfmetrics.registerFont(TTFont("Atkinson", str(fonts / "AtkinsonHyperlegible.ttf")))
    pdfmetrics.registerFont(TTFont("Atkinson-Bold", str(fonts / "AtkinsonHyperlegible-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Pixeloid", str(fonts / "PixeloidSans.ttf")))
    pdfmetrics.registerFont(TTFont("Pixeloid-Bold", str(fonts / "PixeloidSans-Bold.ttf")))


def text(c, value, x, top, *, font="Atkinson", size=10, color=INK, width=None, leading=None):
    """Draw wrapped text using top-down page coordinates; return the next top."""
    c.setFont(font, size)
    c.setFillColor(color)
    lines = simpleSplit(value, font, size, width) if width else [value]
    step = leading or size * 1.42
    for line in lines:
        c.drawString(x, H - top - size, line)
        top += step
    return top


def label(c, value, x, top, color=TEAL):
    return text(c, value.upper(), x, top, font="Pixeloid-Bold", size=9, color=color)


def footer(c, page, light=False):
    tint = MUTED if light else colors.HexColor("#b6a991")
    c.setStrokeColor(colors.HexColor("#c8b88f") if light else TEAL)
    c.setLineWidth(0.4)
    c.line(LEFT, 31, RIGHT, 31)
    text(c, "Grimoire of Blanks - Press Kit", LEFT, 814, size=7.5, color=tint)
    c.setFont("Atkinson", 7.5)
    c.setFillColor(tint)
    c.drawRightString(RIGHT, H - 814 - 7.5, f"{page} / 3")


def box(c, x, top, width, height, fill, border=None, radius=5):
    c.setFillColor(fill)
    c.setStrokeColor(border or fill)
    c.roundRect(x, H - top - height, width, height, radius, stroke=bool(border), fill=1)


def fact(c, title, value, x, top):
    box(c, x, top, 248, 49, CARD)
    text(c, title.upper(), x + 12, top + 7, size=7, color=TEAL)
    text(c, value, x + 12, top + 23, font="Atkinson-Bold", size=10, color=colors.white)


def cover(c):
    c.setFillColor(NIGHT)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    label(c, "Official press kit", LEFT, 38)
    art = ImageReader(str(ROOT / "assets/key-art/main-key-art.png"))
    c.drawImage(art, LEFT, H - 72 - 295, width=515, height=295, mask="auto")
    c.setStrokeColor(colors.HexColor("#6d4939"))
    c.rect(LEFT, H - 72 - 295, 515, 295, stroke=1, fill=0)

    text(c, "Every spell is unfinished. The consequences aren't.", LEFT, 387,
         font="Pixeloid-Bold", size=12, color=TEAL)
    text(c, "A 1-4 player roguelite spellcrafting deckbuilder where cards are unfinished "
         "sentences and the words placed in their blanks decide what happens next.",
         LEFT, 412, size=10, color=colors.white, width=515, leading=14)

    label(c, "Quick facts", LEFT, 472, GOLD)
    for title, value, x, top in [
        ("Developer / publisher", "Esteran Games", LEFT, 496),
        ("Release", "November 10, 2026", 307, 496),
        ("Platform", "Windows PC - Steam", LEFT, 553),
        ("Price", "$9.99 USD", 307, 553),
        ("Players", "1-4, online co-op", LEFT, 610),
        ("Demo", "Available now", 307, 610),
    ]:
        fact(c, title, value, x, top)

    label(c, "Links", LEFT, 692, GOLD)
    text(c, "Steam page and free demo", LEFT, 714, font="Atkinson-Bold", size=9.5, color=GOLD)
    c.linkURL("https://store.steampowered.com/app/4945980/Grimoire_of_Blanks/",
              (LEFT, H - 730, 200, H - 710), relative=0)
    text(c, "Press kit and downloads", LEFT, 739, font="Atkinson-Bold", size=9.5, color=GOLD)
    c.linkURL("https://esterangames.github.io/GrimoireOfBlanksPress/",
              (LEFT, H - 755, 190, H - 735), relative=0)
    text(c, "Seven gameplay screenshots, illustrated key art, capsule and thumbnail artwork, "
         "the official gameplay trailer, and downloadable ZIP packages.",
         307, 714, size=9, color=GOLD, width=248, leading=13)
    footer(c, 1)
    c.showPage()


def feature(c, title, description, x, top):
    box(c, x, top, 162, 117, PALE, colors.HexColor("#ceb47f"))
    text(c, title, x + 11, top + 13, font="Pixeloid-Bold", size=9, color=INK)
    text(c, description, x + 11, top + 38, size=8.5, color=MUTED, width=140, leading=12)


def inside(c):
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    label(c, "The hook", LEFT, 39)
    text(c, "Write the spell. Survive what you wrote.", LEFT, 71,
         font="Pixeloid-Bold", size=14, color=INK)
    text(c, "A card is not a fixed action - it is a sentence frame. Words placed into "
         "its blanks can alter the effect, target, condition, scale, timing, and price of the magic.",
         LEFT, 112, size=9.5, width=515, leading=14)
    feature(c, "WRITE THE SPELL", "Drag words into blanks during combat. The same card can become a "
            "room-wide burn, a delayed trap, or a dangerous burst of power.", LEFT, 168)
    feature(c, "PLAY TOGETHER", "Solo play and up to four-player online co-op. Each player builds "
            "a separate spellbook and can extend an ally's setup.", 217, 168)
    feature(c, "CHOOSE A SCHOOL", "Four classes reshape the system through repetition, seals and frost, "
            "life-fueled power, or astral cycles.", 393, 168)

    label(c, "Current gameplay screenshots", LEFT, 310)
    for n, x in [(1, LEFT), (2, 307)]:
        path = ROOT / f"assets/screenshots/screenshot-{n:02}.png"
        c.drawImage(ImageReader(str(path)), x, H - 340 - 140, width=248, height=140, mask="auto")
        text(c, f"Gameplay screenshot {n}", x, 485, size=8, color=MUTED)

    label(c, "Built for different runs", LEFT, 533)
    text(c, "Branch through battle seals, elite fights, events, shops, upgrades, healing rooms, and bosses. "
         "Build around changing pools of spell cards, words, trinkets, subclasses, and consequences that "
         "can turn a drawback into the center of a run.",
         LEFT, 559, size=9.5, width=515, leading=14)
    label(c, "About", LEFT, 638)
    box(c, LEFT, 665, 248, 116, PALE, colors.HexColor("#ceb47f"))
    box(c, 307, 665, 248, 116, PALE, colors.HexColor("#ceb47f"))
    text(c, "ABOUT THE GAME", LEFT + 12, 678, font="Pixeloid-Bold", size=9)
    text(c, "Grimoire of Blanks is a roguelite spellcrafting deckbuilder about writing "
         "magic into unfinished cards, playable solo or in up to four-player online co-op.",
         LEFT + 12, 707, size=8.5, color=MUTED, width=224, leading=12)
    text(c, "ABOUT ESTERAN GAMES", 319, 678, font="Pixeloid-Bold", size=9)
    text(c, "Esteran Games is the independent studio behind Grimoire of Blanks, combining "
         "roguelite deckbuilding with a word-driven spellcrafting system.",
         319, 707, size=8.5, color=MUTED, width=224, leading=12)
    footer(c, 2, light=True)
    c.showPage()


def guidelines(c):
    c.setFillColor(NIGHT)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    label(c, "Creator notes", LEFT, 39, GOLD)
    text(c, "Coverage guidelines", LEFT, 73, font="Pixeloid-Bold", size=18, color=colors.white)
    text(c, "Everything needed for a clean first look, review, stream, or co-op feature.",
         LEFT, 110, size=9.5, color=GOLD)
    for x, heading, body in [
        (LEFT, "DEMO COVERAGE", "Recording, streaming, and publishing the current Steam demo are "
         "allowed. There is no demo embargo."),
        (307, "FULL-GAME FOOTAGE", "Recipients of a full-game review key may record, stream, "
         "and publish footage from all acts. Review keys will be available closer to launch."),
    ]:
        box(c, x, 157, 248, 133, CARD, TEAL)
        text(c, heading, x + 14, 178, font="Pixeloid-Bold", size=10, color=GOLD)
        text(c, body, x + 14, 211, size=9, color=GOLD, width=220, leading=13)

    label(c, "Available assets", LEFT, 324, GOLD)
    items = [
        "Seven full-resolution gameplay screenshots",
        "Game and studio logos",
        "New key art, Steam capsules, and thumbnail bases",
        "Official 70-second 1080p60 gameplay trailer MP4",
        "Downloadable screenshot and media ZIPs",
        "Plain-text factsheet",
    ]
    for index, item in enumerate(items):
        text(c, "-  " + item, LEFT + 4, 356 + index * 31, size=9.5, color=GOLD)

    box(c, LEFT, 579, 515, 195, CARD, TEAL)
    label(c, "Press contact", LEFT + 16, 596, GOLD)
    text(c, "Kevin, Esteran Games", LEFT + 16, 630,
         font="Pixeloid-Bold", size=14, color=colors.white)
    text(c, "esterangames@gmail.com", LEFT + 16, 672,
         font="Atkinson-Bold", size=10.5, color=GOLD)
    c.linkURL("mailto:esterangames@gmail.com", (LEFT + 16, H - 690, 300, H - 665), relative=0)
    text(c, "For review keys, interviews, additional assets, or co-op coverage arrangements.",
         LEFT + 16, 703, size=9, color=GOLD)
    text(c, "Discord   |   X   |   Instagram   |   YouTube", LEFT + 16, 741,
         font="Atkinson-Bold", size=8.5, color=GOLD)
    footer(c, 3)
    c.showPage()


def build_pdf():
    register_fonts()
    c = canvas.Canvas(str(PDF), pagesize=A4, pageCompression=1)
    c.setTitle("Grimoire of Blanks - Press Kit")
    c.setAuthor("Esteran Games")
    cover(c)
    inside(c)
    guidelines(c)
    c.save()


def build_archive():
    paths = [
        *sorted((ROOT / "assets/clips").glob("*")),
        *sorted((ROOT / "assets/key-art").glob("*")),
        *sorted((ROOT / "assets/logos").glob("*")),
        *sorted((ROOT / "assets/screenshots").glob("*")),
        *sorted((ROOT / "assets/thumbnails").glob("*")),
        ROOT / "factsheet.txt",
        PDF,
        ROOT / "START HERE - Read Me.txt",
    ]
    with ZipFile(ARCHIVE, "w", compression=ZIP_DEFLATED, compresslevel=6) as archive:
        for path in paths:
            info = ZipInfo(path.relative_to(ROOT / "assets").as_posix()
                           if path.is_relative_to(ROOT / "assets")
                           else path.name)
            info.date_time = (2026, 10, 19, 0, 0, 0)
            info.compress_type = ZIP_DEFLATED
            archive.writestr(info, path.read_bytes(), compress_type=ZIP_DEFLATED, compresslevel=6)


if __name__ == "__main__":
    build_pdf()
    build_archive()
