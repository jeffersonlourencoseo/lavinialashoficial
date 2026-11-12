# -*- coding: utf-8 -*-
"""Converte as fotos de 'Nova pasta' (nomeadas por serviço) em WebP otimizado dentro de site/assets/img.
Uso: python build/process_photos.py
Cada item: (arquivo original, giro em graus [horário negativo], nome final sem extensão, recortar faixas pretas?)"""
import os, glob
from PIL import Image, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "Nova pasta")
DST = os.path.join(ROOT, "site", "assets", "img")

ITEMS = [
    # serviço rotulado pela Lavinia/Jefferson
    ("fox eyes (2).jpeg",            0, "fox-eyes-cosmos-rj-01", False),
    ("fox eyes.jpeg",              -90, "fox-eyes-cosmos-rj-02", False),
    ("mega volume egipcio 1.jpg",    0, "mega-volume-egipcio-cosmos-rj-01", False),
    ("mega volume egipcio.jpg",    180, "mega-volume-egipcio-cosmos-rj-02", False),
    ("volume brasileiro.jpeg",     -90, "volume-brasileiro-cosmos-rj-01", False),
    ("volume brasileiro (3).jpeg",   0, "volume-brasileiro-cosmos-rj-02", False),
    ("volume brasileiro (2).jpeg", -90, "volume-brasileiro-cosmos-rj-03", False),
    ("volume egipcio.jpeg",          0, "volume-egipcio-cosmos-rj-01", False),
    ("volume egipcio (2).jpeg",     90, "volume-egipcio-cosmos-rj-02", True),
    # ainda sem rótulo de técnica (uso geral)
    ("lavinia.lash.designer.jpeg", -90, "extensao-de-cilios-cosmos-rj-01", False),
    ("lavinia.lash.designer_4.jpeg", 90, "extensao-de-cilios-cosmos-rj-02", False),
    ("lavinia.lash.designer_7.jpeg",  0, "extensao-de-cilios-cosmos-rj-03", False),
    ("lavinia.lash.designer_8.jpeg", 90, "extensao-de-cilios-cosmos-rj-04", False),
]

def save(im, name, maxe=1400, q=80):
    t = im.copy(); t.thumbnail((maxe, maxe), Image.LANCZOS)
    t.save(os.path.join(DST, name + ".webp"), "WEBP", quality=q, method=6)
    s = t.copy(); s.thumbnail((700, 700), Image.LANCZOS)
    s.save(os.path.join(DST, name + "-m.webp"), "WEBP", quality=76, method=6)
    return t.size

if __name__ == "__main__":
    # remove as versões antigas (nomes genéricos numerados da primeira versão)
    for f in glob.glob(os.path.join(DST, "extensao-de-cilios-cosmos-rj-*.webp")):
        os.remove(f)
    for fn, rot, name, crop in ITEMS:
        im = Image.open(os.path.join(SRC, fn)).convert("RGB")
        if rot:
            im = im.rotate(rot, expand=True)
        if crop:  # recorta faixas pretas de frame de vídeo
            diff = ImageChops.difference(im, Image.new("RGB", im.size, (0, 0, 0))).convert("L").point(lambda p: 255 if p > 28 else 0)
            im = im.crop(diff.getbbox())
        print(name, save(im, name))
