# -*- coding: utf-8 -*-
"""Layout compartilhado: head/SEO, cabeçalho, rodapé, helpers de imagem e botões."""
import json, os, re
from html import escape
from urllib.parse import quote
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site")
IMG = os.path.join(OUT, "assets", "img")

# ---- CONFIG (trocar o domínio quando definido) ----
SITE_URL = os.environ.get("SITE_URL", "https://SITE_URL_PLACEHOLDER").rstrip("/")  # trocado no deploy pelo scripts/set-domain.mjs
NAME = "Lavínia Monteiro | Lash Designer"
PHONE_DISPLAY = "(21) 98842-0844"
PHONE_E164 = "+5521988420844"
WA_NUMBER = "5521988420844"
WA_TEXT = "Olá, vi seu site e gostaria de mais informações!"
INSTAGRAM = "https://www.instagram.com/laviniamonteiro_lash/"
INSTAGRAM_USER = "@laviniamonteiro_lash"
MAPS = "https://www.google.com/maps/place/Lavinia+Monteiro+%7C+Lash+Designer/@-22.9248479,-43.6058418,17z/data=!4m6!3m5!1s0x9be59efa3ec821:0x489149cbe8dea4c6!8m2!3d-22.9248479!4d-43.6058418!16s%2Fg%2F11p2slldlh?hl=pt-BR"
TODAY = "2026-11-25"  # lastmod do sitemap
WA_URL = f"https://wa.me/{WA_NUMBER}?text={quote(WA_TEXT)}"

AREAS = ["Cosmos", "Campo Grande", "Paciência", "Senador Vasconcelos", "Inhoaíba", "Santa Cruz"]

ICON_WA = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.5 3.5A11.8 11.8 0 0 0 12 0C5.4 0 .1 5.3.1 11.9c0 2.1.5 4.1 1.6 5.9L0 24l6.4-1.7a11.9 11.9 0 0 0 5.6 1.4c6.6 0 11.9-5.3 11.9-11.9 0-3.2-1.2-6.2-3.4-8.3zM12 21.7c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.8 1 1-3.7-.2-.4a9.8 9.8 0 0 1-1.5-5.1C2.1 6.5 6.5 2.1 12 2.1c2.6 0 5.1 1 6.9 2.9a9.7 9.7 0 0 1 2.9 6.9c0 5.4-4.4 9.8-9.8 9.8zm5.4-7.3c-.3-.1-1.7-.8-2-.9-.3-.1-.5-.1-.7.1l-.9 1.1c-.2.2-.3.2-.6.1-1.6-.8-2.6-1.4-3.7-3.2-.3-.5.3-.5.8-1.5.1-.2 0-.4 0-.5l-.9-2.1c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2.1 3.2 5.1 4.5 1.9.8 2.6.9 3.5.7.6-.1 1.7-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3z"/></svg>'
ICON_IG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r=".9" fill="currentColor" stroke="none"/></svg>'
ICON_PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 21s7-6.1 7-11.5A7 7 0 0 0 5 9.5C5 14.9 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.6"/></svg>'
ICON_CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M7.5 12.5l3 3 6-6.5"/></svg>'
ICON_HOME = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 11l9-7.5L21 11"/><path d="M5.5 9.5V20h13V9.5"/><path d="M10 20v-5.5h4V20"/></svg>'

# ---- logo (marca do olho) lida do SVG original ----
_logo = open(os.path.join(OUT, "assets", "img", "logo-lavinia.svg"), encoding="utf8").read()
_paths = re.findall(r'<path d="([^"]+)"', _logo)
_arc, _lashes = _paths[0], _paths[1:]
EYE_SYMBOL = (
    '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="eye" viewBox="180 292 360 156">'
    '<g fill="none" stroke="currentColor" stroke-linecap="round">'
    f'<path d="{_arc}" stroke-width="8"/><g stroke-width="6">'
    + "".join(f'<path d="{d}"/>' for d in _lashes)
    + "</g></g></symbol></svg>"
)
def eye(cls="", w=None):
    return f'<svg class="{cls}" viewBox="0 0 360 156" aria-hidden="true"><use href="#eye"/></svg>'

_sizes = {}
def img_size(name):
    if name not in _sizes:
        with Image.open(os.path.join(IMG, name + ".webp")) as im:
            _sizes[name] = im.size
        with Image.open(os.path.join(IMG, name + "-m.webp")) as im:
            _sizes[name + "-m"] = im.size
    return _sizes[name], _sizes[name + "-m"]

def pic(name, alt, sizes="(min-width:980px) 33vw, 90vw", eager=False, cls="", style=""):
    (w, h), (mw, mh) = img_size(name)
    attrs = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    st = f' style="{style}"' if style else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c}{st} src="/assets/img/{name}-m.webp" srcset="/assets/img/{name}-m.webp {mw}w, /assets/img/{name}.webp {w}w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{escape(alt)}" {attrs}>')

def wa_btn(label="Agendar pelo WhatsApp", cls="", where="cta"):
    return (f'<a class="btn {cls}" href="{WA_URL}" target="_blank" rel="noopener" data-where="{where}">{ICON_WA}<span>{label}</span></a>')

def ig_btn(label="Ver o Instagram", cls="ghost"):
    return f'<a class="btn {cls}" href="{INSTAGRAM}" target="_blank" rel="noopener me">{ICON_IG}<span>{label}</span></a>'

def faq_html(items):
    out = '<div class="faq">'
    for q, a in items:
        paras = "".join(f"<p>{p}</p>" for p in a.split("\n\n"))
        out += f'<details><summary>{q}</summary><div class="ans">{paras}</div></details>'
    return out + "</div>"

def faq_schema(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": re.sub("<[^>]+>", "", q),
         "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a.replace("\n\n", " "))}} for q, a in items]}

def crumbs_schema(trail):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE_URL + u} for i, (n, u) in enumerate(trail)]}

def crumbs_html(trail):
    parts = []
    for i, (n, u) in enumerate(trail):
        parts.append(escape(n) if i == len(trail) - 1 else f'<a href="{u}">{escape(n)}</a>')
    return '<nav class="crumbs" aria-label="Você está em">' + "<span>›</span>".join(parts) + "</nav>"

def business_schema():
    return {
        "@context": "https://schema.org",
        "@type": ["BeautySalon", "LocalBusiness"],
        "@id": SITE_URL + "/#negocio",
        "name": NAME,
        "alternateName": "Lavínia Monteiro Lash Designer",
        "description": "Lash designer em Cosmos, Rio de Janeiro. Extensão de cílios fio a fio, volume egípcio, volume brasileiro, mega volume egípcio e Fox Eyes, com atendimento a domicílio em Cosmos, Campo Grande, Paciência, Senador Vasconcelos, Inhoaíba e Santa Cruz.",
        "url": SITE_URL + "/",
        "telephone": PHONE_E164,
        "image": SITE_URL + "/assets/img/og-lavinia.jpg",
        "logo": SITE_URL + "/assets/img/logo-lavinia.png",
        "address": {"@type": "PostalAddress", "addressLocality": "Cosmos, Rio de Janeiro", "addressRegion": "RJ", "addressCountry": "BR"},
        "areaServed": [{"@type": "Place", "name": f"{a}, Rio de Janeiro - RJ"} for a in AREAS],
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s}} for s in
                       ["Extensão de cílios fio a fio", "Volume egípcio", "Volume brasileiro", "Mega volume egípcio", "Volume Fox Eyes", "Manutenção de cílios", "Remoção de extensão de cílios"]],
        "foundingDate": "2024",
        "slogan": "Eu vou até você: extensão de cílios a domicílio",
        "founder": {"@type": "Person", "@id": SITE_URL + "/#lavinia", "name": "Lavínia Monteiro", "jobTitle": "Lash designer",
                    "url": SITE_URL + "/quem-sou/", "image": SITE_URL + "/assets/img/lavinia-monteiro-lash-designer.webp",
                    "sameAs": [INSTAGRAM, MAPS],
                    "knowsAbout": ["Extensão de cílios", "Extensão de cílios fio a fio", "Volume egípcio", "Volume brasileiro", "Mega volume egípcio", "Fox Eyes", "Manutenção de cílios", "Remoção de extensão de cílios"]},
        "sameAs": [INSTAGRAM, MAPS],
        "knowsLanguage": "pt-BR",
        "contactPoint": {"@type": "ContactPoint", "telephone": PHONE_E164, "contactType": "customer service", "availableLanguage": "Portuguese"},
    }

NAV = [("/", "Início"), ("/quem-sou/", "Quem sou"), ("/servicos/", "Serviços"), ("/clientes/", "Clientes"),
       ("/atendimento/", "Onde atendo"), ("/blog/", "Blog"), ("/contato/", "Contato")]

def header(path):
    links = ""
    for u, n in NAV:
        cur = ' aria-current="page"' if (u == path or (u != "/" and path.startswith(u))) else ""
        links += f'<a href="{u}"{cur}>{n}</a>'
    return f'''<a class="skip" href="#main">Pular para o conteúdo</a>
<div class="topbar">Atendimento a domicílio em Cosmos, Campo Grande, Paciência, Vasconcelos, Inhoaíba e Santa Cruz · <a href="{WA_URL}" target="_blank" rel="noopener">Agende pelo WhatsApp</a></div>
<header class="header"><div class="wrap">
<a class="brand" href="/">{eye()}<span><b>LAVÍNIA MONTEIRO</b><small>Lash Designer</small></span></a>
<button class="burger" aria-expanded="false" aria-controls="menu" aria-label="Abrir menu"><span></span><span></span><span></span></button>
<nav class="nav" id="menu" aria-label="Principal">{links}<a class="btn sm" href="{WA_URL}" target="_blank" rel="noopener">{ICON_WA}<span>Agendar</span></a></nav>
</div></header>'''

def footer():
    return f'''<footer class="footer"><div class="wrap">
<div class="grid">
<div><a class="brand" href="/">{eye()}<span><b>LAVÍNIA MONTEIRO</b><small>Lash Designer</small></span></a>
<p>Extensão de cílios a domicílio em Cosmos, Campo Grande, Paciência, Senador Vasconcelos, Inhoaíba e Santa Cruz, no Rio de Janeiro. Eu vou até você.</p></div>
<div><p class="fh">Serviços</p><ul>
<li><a href="/servicos/extensao-de-cilios-fio-a-fio/">Fio a fio</a></li>
<li><a href="/servicos/volume-egipcio/">Volume egípcio</a></li>
<li><a href="/servicos/volume-brasileiro/">Volume brasileiro</a></li>
<li><a href="/servicos/mega-volume-egipcio/">Mega volume egípcio</a></li>
<li><a href="/servicos/volume-fox-eyes/">Volume Fox Eyes</a></li>
<li><a href="/servicos/manutencao-de-cilios/">Manutenção</a></li>
<li><a href="/servicos/remocao-de-cilios/">Remoção</a></li></ul></div>
<div><p class="fh">Navegue</p><ul>
<li><a href="/quem-sou/">Quem sou</a></li><li><a href="/clientes/">Clientes</a></li>
<li><a href="/atendimento/cosmos/">Cílios em Cosmos</a></li><li><a href="/atendimento/campo-grande/">Cílios em Campo Grande RJ</a></li>
<li><a href="/blog/">Blog</a></li><li><a href="/contato/">Contato</a></li></ul></div>
<div><p class="fh">Fale comigo</p><ul>
<li><a href="{WA_URL}" target="_blank" rel="noopener">WhatsApp {PHONE_DISPLAY}</a></li>
<li><a href="{INSTAGRAM}" target="_blank" rel="noopener me">Instagram {INSTAGRAM_USER}</a></li>
<li><a href="{MAPS}" target="_blank" rel="noopener">Perfil no Google Maps</a></li>
<li>Cosmos, Rio de Janeiro - RJ<br><small>Atendimento a domicílio, com hora marcada</small></li></ul></div>
</div>
<div class="bar"><span>© 2026 Lavínia Monteiro | Lash Designer. Todos os direitos reservados.</span><span>Cosmos · Campo Grande · Paciência · Sen. Vasconcelos · Inhoaíba · Santa Cruz</span><nav class="legal" aria-label="Informações legais"><a href="/politica-de-privacidade/">Política de Privacidade</a><a href="/politica-de-cookies/">Política de Cookies</a><a href="/termos-de-uso/">Termos de Uso</a><button type="button" class="linkbtn" data-cookie-settings>Gerenciar cookies</button></nav><span class="credit">Site criado por Jefferson Lourenço</span></div>
</div></footer>
<a class="wafab" href="{WA_URL}" target="_blank" rel="noopener" aria-label="Agendar no WhatsApp com a Lavínia">{ICON_WA}<span>Agendar no WhatsApp</span></a>'''

def render(path, title, desc, body, schemas=None, og_image="/assets/img/og-lavinia.jpg", og_type="website", noindex=False, extra_head=""):
    url = SITE_URL + path
    schemas = schemas or []
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False, separators=(",", ":"))}</script>' for s in schemas)
    robots = '<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    css = open(os.path.join(OUT, "assets", "fonts.css"), encoding="utf8").read()
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
{robots}
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="pt-BR" href="{url}"><link rel="alternate" hreflang="x-default" href="{url}">
<meta name="author" content="Lavínia Monteiro"><meta name="geo.region" content="BR-RJ"><meta name="geo.placename" content="Cosmos, Rio de Janeiro">
<meta name="theme-color" content="#5A2A3C">
<meta property="og:locale" content="pt_BR"><meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE_URL}{og_image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/cormorant-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/jost-normal.woff2" as="font" type="font/woff2" crossorigin>
<style>{css}</style>
<link rel="stylesheet" href="/assets/css/style.css?v=2">
{extra_head}{ld}
</head>
<body>
{EYE_SYMBOL}
{header(path)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/main.js?v=1" defer></script>
<script src="/assets/js/analytics.js?v=1" defer></script>
</body>
</html>'''

def write(path, html):
    fp = os.path.join(OUT, path.strip("/"), "index.html") if path != "/" else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w", encoding="utf8").write(html)

def final_cta(title="Vamos cuidar do seu olhar?", text="Me chame no WhatsApp, conte o efeito que você sonha e eu vou até a sua casa, com hora marcada."):
    return f'''<section class="cta"><div class="wrap rv">
{eye("mark")}
<h2>{title}</h2><p>{text}</p>
<div class="btns">{wa_btn("Agendar pelo WhatsApp","light","cta-final")}</div></div></section>'''
