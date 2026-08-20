# Gera capa.png (1200x630) para o cartão OG do WhatsApp — Portal Preço do Combustível ARI
# Estilo: mesma linguagem visual do cadastro-ari (fundo escuro, moldura scan, laranja ARI).
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "logo-ari.png")
BOMBA = os.path.join(HERE, "bomba.jpg")
OUT = os.path.join(HERE, "capa.png")

W, H = 1200, 630
VOID  = (14, 17, 22)
LINE  = (38, 46, 57)
STRAP = (255, 107, 26)
HIVIZ = (200, 240, 49)
MIST  = (232, 236, 241)

F = "C:/Windows/Fonts/"


def font(name, sz):
    return ImageFont.truetype(F + name, sz)


bahn = lambda sz: font("bahnschrift.ttf", sz)


def rounded_mask(size, rad):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], rad, fill=255)
    return m


def logo_transparent(path):
    im = Image.open(path).convert("RGB")
    px = im.load()
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    op = out.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b = px[x, y]
            a = 255 - min(r, g, b)
            if a <= 8:
                continue
            if (r - (g + b) // 2) > 35 and r > 110:
                op[x, y] = (232, 45, 40, a)
            else:
                op[x, y] = (233, 237, 242, a)
    return out


def bomba_transparent(path):
    im = Image.open(path).convert("RGB")
    px = im.load()
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    op = out.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b = px[x, y]
            if r > 245 and g > 245 and b > 245:  # fundo branco -> transparente
                continue
            op[x, y] = (r, g, b, 255)
    return out


# ---------- fundo com glows ----------
img = Image.new("RGB", (W, H), VOID)
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(glow).ellipse([300, -380, 1000, 240], fill=(255, 107, 26, 44))
ImageDraw.Draw(glow).ellipse([350, 420, 950, 860], fill=(200, 240, 49, 18))
img = Image.alpha_composite(img.convert("RGBA"),
                            glow.filter(ImageFilter.GaussianBlur(120))).convert("RGB")
d = ImageDraw.Draw(img)

# ---------- moldura scan ----------
m, ln, tk = 30, 42, 3
for cx, cy, dx, dy in [(m, m, 1, 1), (W - m, m, -1, 1),
                       (m, H - m, 1, -1), (W - m, H - m, -1, -1)]:
    d.line([(cx, cy), (cx + dx * ln, cy)], fill=LINE, width=tk)
    d.line([(cx, cy), (cx, cy + dy * ln)], fill=LINE, width=tk)

# ---------- 1) LOGO ARI transparente ----------
logo = logo_transparent(LOGO)
lw = 300
lh = round(lw * logo.height / logo.width)
logo = logo.resize((lw, lh), Image.LANCZOS)
img.paste(logo, ((W - lw) // 2, 20), logo)

# ---------- 2) BOMBA centralizada ----------
bomba = bomba_transparent(BOMBA)
bw = 300
bh = round(bw * bomba.height / bomba.width)
bomba = bomba.resize((bw, bh), Image.LANCZOS)
bx = (W - bw) // 2
by = 22 + lh + 6
img.paste(bomba, (bx, by), bomba)

# ---------- 3) TÍTULO ----------
d = ImageDraw.Draw(img)
tf = bahn(66)
ker = -2
segs = [("PREÇO DO ", MIST), ("COMBUSTÍVEL", STRAP)]
tw = 0
for seg, _ in segs:
    for c in seg:
        tw += d.textlength(c, font=tf) + ker
tw -= ker
ty = by + bh + 18
x = (W - tw) // 2
for txt, col in segs:
    for c in txt:
        d.text((x, ty), c, font=tf, fill=col)
        x += d.textlength(c, font=tf) + ker

# ---------- 4) BOTÃO ----------
bf, btxt = bahn(30), "ABRIR PORTAL"
bt = d.textlength(btxt, font=bf)
btnw = int(26 + bt + 18 + 22 + 22)
btnh = 50
btnx = (W - btnw) // 2
btny = ty + 88
d.rounded_rectangle([btnx, btny, btnx + btnw, btny + btnh], 14, fill=STRAP)
d.text((btnx + 26, btny + 12), btxt, font=bf, fill=(26, 13, 4))
axx, ayy = btnx + 26 + bt + 18, btny + btnh / 2
d.line([(axx, ayy), (axx + 22, ayy)], fill=(26, 13, 4), width=4)
d.line([(axx + 13, ayy - 8), (axx + 22, ayy), (axx + 13, ayy + 8)],
       fill=(26, 13, 4), width=4, joint="curve")

img.save(OUT)
print("ok", img.size, "->", OUT)
