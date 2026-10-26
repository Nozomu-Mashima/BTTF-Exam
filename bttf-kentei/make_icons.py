# アイコン画像を、元の画像1枚から必要なサイズにまとめて作るスクリプト。
# 使い方：1024×1024 の正方形PNGを「icon-source.png」という名前でこのフォルダに置き、
#        python make_icons.py を実行する。icons フォルダに4つの画像ができます。
# 元の画像がない場合は、仮のアイコン（黒地に「88」）を作ります。
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
OUT = HERE / "icons"
OUT.mkdir(exist_ok=True)
SOURCE = HERE / "icon-source.png"
BG = (20, 23, 28)  # タイムサーキットの黒（#14171c）


def placeholder(size=1024):
    """仮アイコン：黒地にオレンジの「88」"""
    img = Image.new("RGB", (size, size), BG)
    draw = ImageDraw.Draw(img)
    font = None
    for name in ["arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf"]:
        try:
            font = ImageFont.truetype(name, int(size * 0.5))
            break
        except OSError:
            pass
    font = font or ImageFont.load_default()
    draw.text((size / 2, size / 2), "88", fill=(255, 138, 0), font=font, anchor="mm")
    return img


src = Image.open(SOURCE).convert("RGBA") if SOURCE.exists() else placeholder().convert("RGBA")


def flat(img, size):
    """透明部分を背景色で埋めて、指定サイズに縮小する（iPhoneは透明を黒く塗るため）"""
    base = Image.new("RGB", img.size, BG)
    base.paste(img, mask=img.split()[3])
    return base.resize((size, size), Image.LANCZOS)


flat(src, 192).save(OUT / "icon-192.png")
flat(src, 512).save(OUT / "icon-512.png")
flat(src, 180).save(OUT / "apple-touch-icon.png")

# マスカブル用（Androidで丸や角丸に切り抜かれる前提のアイコン）。
# 元画像は全面に絵があり、大事な「88」が中央80%に収まっているので、そのまま使う。
# 仮アイコンのときだけ、欠けないよう周りに余白を足す。
if SOURCE.exists():
    flat(src, 512).save(OUT / "icon-maskable-512.png")
else:
    pad = Image.new("RGB", (512, 512), BG)
    pad.paste(flat(src, 410), (51, 51))
    pad.save(OUT / "icon-maskable-512.png")

print("作成しました：", ", ".join(p.name for p in sorted(OUT.glob("*.png"))))
print("元画像：", SOURCE.name if SOURCE.exists() else "なし（仮アイコンを使用）")
