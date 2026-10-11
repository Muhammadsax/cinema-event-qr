from pathlib import Path

import qrcode
import arabic_reshaper
from PIL import Image, ImageDraw, ImageFont
from bidi.algorithm import get_display


OUTPUT_DIR = Path(__file__).resolve().parent
CANVAS_SIZE = (900, 900)
QR_SIZE = 900
FORM_URL = (
    "https://docs.google.com/forms/d/e/"
    "1FAIpQLSdFu6BA4E6z1BNWOVvT4mejagWYyYNA_CtmlNxrMWbVrmVftw/viewform?usp=dialog"
)
EVENT_POST_URL = "https://www.facebook.com/share/p/1P24BtrWPF/"

INK = "#160b0a"
POST_INK = "#241018"
BLACK = "#080505"
WINE = "#3a0710"
RED = "#9a1f2d"
GOLD = "#bd7940"
GOLD_LIGHT = "#f0c589"
CREAM = "#fff5df"
MUTED = "#c7a882"
FONT_DIR = Path("C:/Windows/Fonts")


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size)


def centered_text(
    draw: ImageDraw.ImageDraw,
    y: int,
    text: str,
    selected_font: ImageFont.FreeTypeFont,
    fill: str,
) -> None:
    shaped_text = get_display(arabic_reshaper.reshape(text))
    box = draw.textbbox((0, 0), shaped_text, font=selected_font)
    x = (CANVAS_SIZE[0] - (box[2] - box[0])) // 2
    draw.text((x, y), shaped_text, font=selected_font, fill=fill)


def make_qr(url: str, ink: str) -> Image.Image:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(fill_color=ink, back_color=CREAM).convert("RGB").resize(
        (QR_SIZE, QR_SIZE), Image.Resampling.NEAREST
    )


def add_camera_mark(image: Image.Image) -> None:
    """Mark the form QR with a compact camera icon."""
    draw = ImageDraw.Draw(image)
    center = QR_SIZE // 2
    radius = 82
    draw.ellipse(
        (center - radius, center - radius, center + radius, center + radius),
        fill=CREAM,
        outline=GOLD,
        width=8,
    )
    body = (center - 54, center - 28, center + 42, center + 35)
    draw.rounded_rectangle(body, radius=9, fill=INK)
    draw.polygon(
        [(center + 42, center - 16), (center + 74, center - 31),
         (center + 74, center + 25), (center + 42, center + 11)],
        fill=INK,
    )
    draw.ellipse(
        (center - 30, center - 15, center + 8, center + 23),
        outline=GOLD_LIGHT,
        width=7,
    )
    draw.ellipse(
        (center - 24, center - 9, center + 2, center + 17),
        outline=GOLD_LIGHT,
        width=4,
    )


def add_film_reel_mark(image: Image.Image) -> None:
    """Mark the event-post QR with a distinct film-reel icon."""
    draw = ImageDraw.Draw(image)
    center = QR_SIZE // 2
    radius = 82
    draw.ellipse(
        (center - radius, center - radius, center + radius, center + radius),
        fill=CREAM,
        outline=RED,
        width=8,
    )
    draw.ellipse(
        (center - 51, center - 51, center + 51, center + 51),
        outline=GOLD,
        width=8,
    )
    for dx, dy in ((-24, -24), (24, -24), (-24, 24), (24, 24)):
        hole_radius = 12
        draw.ellipse(
            (center + dx - hole_radius, center + dy - hole_radius,
             center + dx + hole_radius, center + dy + hole_radius),
            fill=RED,
        )
    draw.ellipse(
        (center - 10, center - 10, center + 10, center + 10),
        fill=GOLD,
    )


def create_branded_qr(filename: str, url: str, ink: str, marker: str) -> None:
    image = make_qr(url, ink)
    if marker == "camera":
        add_camera_mark(image)
    else:
        add_film_reel_mark(image)
    image.save(OUTPUT_DIR / filename, "PNG", optimize=True)


def main() -> None:
    create_branded_qr("form.png", FORM_URL, INK, "camera")
    create_branded_qr("event-post.png", EVENT_POST_URL, POST_INK, "film-reel")
    print("Generated form.png and event-post.png")


if __name__ == "__main__":
    main()
