# -*- coding: utf-8 -*-
"""Gera o site estático em ../site. Uso: python build.py  (SITE_URL=https://dominio.com.br python build.py)"""
import os, sys, shutil, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout import *
from content import SERVICES, EXTRA_SERVICES, HOME_FAQ, STEPS, TESTIMONIALS
from blog import ARTICLES, CTA as BLOG_CTA
from PIL import Image, ImageDraw
from html import escape

from photos import PHOTO_ALT, TECH_PHOTOS, GENERAL, HOME_GALLERY

def mosaic(ids, grid=False):
    few = " few" if len(ids) <= 2 else ""
    out = f'<div class="mosaic{few}{" grid" if grid else ""}">'
    for pid in ids:
        out += (f'<figure class="rv"><button type="button" data-lb="/assets/img/{pid}.webp" data-alt="{escape(PHOTO_ALT[pid])}" aria-label="Ampliar foto">'
                f'{pic(pid, PHOTO_ALT[pid], sizes="(min-width:980px) 33vw, (min-width:560px) 50vw, 100vw")}</button></figure>')
    return out + "</div>"

def results_section(s):
    ids = TECH_PHOTOS.get(s["slug"])
    if not ids:
        return ""
    return (f'<section class="sec"><div class="wrap">{sec_head("Resultados", "Resultados de <em>" + s["short"].lower().replace("volume fox eyes", "Fox Eyes") + "</em> em Cosmos e Campo Grande", "Fotos de atendimentos reais. Toque para ampliar.")}'
            f'{mosaic(ids, True)}<div class="btns" style="justify-content:center;margin-top:40px">{wa_btn("Quero esse resultado")}</div></div></section>')

def clients_gallery():
    out = ""
    order = [("volume-brasileiro", "Volume brasileiro"), ("volume-egipcio", "Volume egípcio"), ("mega-volume-egipcio", "Mega volume egípcio"), ("volume-fox-eyes", "Fox Eyes")]
    for slug, nome in order:
        out += (f'<div class="gal-head rv"><h2>{nome}</h2><a class="more" href="/servicos/{slug}/">Ver o serviço</a></div>{mosaic(TECH_PHOTOS[slug], True)}')
    out += f'<div class="gal-head rv"><h2>Mais resultados</h2></div>{mosaic(GENERAL, True)}'
    return out

def service_cards(exclude=None, items=None):
    lst = [x for x in (items or SERVICES) if x["slug"] != exclude]
    out = f'<div class="cards{" c4" if len(lst) == 4 else ""}">'
    for s in lst:
        out += (f'<a class="card rv" href="/servicos/{s["slug"]}/"><div class="ph">'
                f'{pic(s["photo"], "Resultado de " + s["name"].lower() + " por Lavínia Monteiro", style="object-position:" + s["pos"])}</div>'
                f'<div class="tx"><h3>{s["short"]}</h3><p>{s["card"]}</p><span class="more">Saiba mais</span></div></a>')
    return out + "</div>"

def extras_block():
    return (f'<div class="sec-head rv" style="margin-top:clamp(56px,7vw,90px);margin-bottom:34px"><span class="eyebrow">Cuidado contínuo</span>'
            f'<h2 style="font-size:clamp(1.7rem,3vw,2.3rem)">Manutenção e <em>remoção</em></h2></div>' + service_cards(items=EXTRA_SERVICES))

def testimonials_section():
    """Só aparece quando houver depoimentos REAIS em content.TESTIMONIALS."""
    if not TESTIMONIALS:
        return ""
    cards = "".join(f'<figure class="depo rv"><blockquote>“{escape(t["texto"])}”</blockquote><figcaption><b>{escape(t["nome"])}</b>'
                    f'{" · " + escape(t["bairro"]) if t.get("bairro") else ""}{" · " + escape(t["servico"]) if t.get("servico") else ""}</figcaption></figure>' for t in TESTIMONIALS)
    return (f'<section class="sec"><div class="wrap">{sec_head("Depoimentos", "O que dizem as <em>clientes</em>")}<div class="depos">{cards}</div>'
            f'<div class="btns" style="justify-content:center;margin-top:36px"><a class="btn ghost" href="{MAPS}" target="_blank" rel="noopener">Ver avaliações no Google</a></div></div></section>')

def why_section():
    """5 cards factuais. Saem de cena quando houver depoimentos reais (TESTIMONIALS)."""
    items = [("Eu vou até você", "Atendimento a domicílio em Cosmos, Campo Grande, Paciência, Senador Vasconcelos, Inhoaíba e Santa Cruz. Sem trânsito e sem sair de casa."),
             ("Hora marcada", "Atenção exclusiva para você, sem fila e sem pressa, no horário combinado pelo WhatsApp."),
             ("Cinco técnicas", "Fio a fio, volume egípcio, volume brasileiro, mega volume e Fox Eyes. A gente escolhe juntas o efeito do seu olhar."),
             ("Manutenção e remoção", "O cuidado não termina na aplicação: reposição dos fios e remoção feita com cuidado, tudo em casa."),
             ("Cuidado com seus fios", "Aplicação feita com calma, respeitando o formato dos seus olhos e a saúde dos seus cílios naturais.")]
    cards = "".join(f'<div class="why-card rv"><h3>{t}</h3><p>{d}</p></div>' for t, d in items)
    return f'<section class="sec"><div class="wrap">{sec_head("Por que escolher", "O que as clientes <em>encontram</em> aqui")}<div class="why">{cards}</div></div></section>'

def review_invite():
    return (f'<section class="sec blush"><div class="wrap narrow center rv"><span class="eyebrow">Sua opinião</span><h2>Já foi atendida? <em>Conte como foi</em></h2>'
            f'<p class="lead">Sua avaliação no Google ajuda outras mulheres a me encontrarem e me motiva a continuar cuidando de cada olhar.</p>'
            f'<div class="btns" style="justify-content:center"><a class="btn" href="{MAPS}" target="_blank" rel="noopener">{ICON_PIN}<span>Avaliar no Google</span></a></div></div></section>')

def post_cards(items):
    out = '<div class="posts">'
    for a in items:
        out += (f'<a class="post rv" href="/blog/{a["slug"]}/"><div class="ph">{pic(a["photo"], a["h1"], sizes="(min-width:980px) 380px, 90vw")}</div>'
                f'<div class="pt"><span class="tag">{a["tag"]}</span><h3>{a["h1"]}</h3>'
                f'<p>{a["desc"]}</p><span class="meta">{a["min"]} min de leitura</span></div></a>')
    return out + "</div>"

def steps_html():
    return '<ol class="steps">' + "".join(f'<li class="rv d{i+1}"><h3>{t}</h3><p>{p}</p></li>' for i, (t, p) in enumerate(STEPS)) + "</ol>"

def sec_head(eyebrow, h2, lead=""):
    l = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<div class="sec-head rv"><span class="eyebrow">{eyebrow}</span><h2>{h2}</h2>{l}</div>'

def checks(items):
    return '<ul class="checks">' + "".join(f"<li>{ICON_CHECK}<span>{i}</span></li>" for i in items) + "</ul>"

def chips(links=True):
    out = '<ul class="chips">'
    for a in AREAS:
        if a == "Cosmos" and links: out += '<li><a href="/atendimento/cosmos/">Cosmos</a></li>'
        elif a == "Campo Grande" and links: out += '<li><a href="/atendimento/campo-grande/">Campo Grande RJ</a></li>'
        else: out += f"<li>{a}</li>"
    return out + "</ul>"

SCH_BUSINESS = business_schema()
WEBSITE = {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE_URL + "/#site", "url": SITE_URL + "/", "name": NAME, "inLanguage": "pt-BR", "publisher": {"@id": SITE_URL + "/#negocio"}}
pages = []  # para o sitemap

def add(path, title, desc, body, schemas=None, **kw):
    write(path, render(path, title, desc, body, schemas, **kw))
    pages.append(path)

# ===================== HOME =====================
def home():
    hero = f'''<section class="hero"><div class="wrap">
<div class="rv">
<span class="eyebrow">Lash designer a domicílio · Cosmos, RJ</span>
<h1>Extensão de cílios a domicílio em Cosmos e <em>Campo Grande</em></h1>
<p class="lead">Olá, eu sou a Lavínia. Faço extensão de cílios fio a fio e volume, manutenção e remoção, com técnica, cuidado e atenção a cada detalhe do seu olhar. E eu vou até a sua casa.</p>
<div class="btns">{wa_btn("Agendar pelo WhatsApp","","hero")}<a class="btn ghost" href="/servicos/">Conhecer os serviços</a></div>
<ul class="hero-points"><li>{ICON_HOME}Atendimento a domicílio</li><li>{ICON_CHECK}Sempre com hora marcada</li><li>{ICON_PIN}Cosmos · Campo Grande · mais 4 bairros</li></ul>
</div>
<div class="arch rv d1">
{pic("lavinia-monteiro-lash-designer", "Lavínia Monteiro, lash designer em Cosmos, Rio de Janeiro, segurando pinças e escovinha de cílios", sizes="(min-width:980px) 470px, 90vw", eager=True)}
<div class="badge">{eye()}<span><b>Eu vou até você</b>Cosmos, Campo Grande, Paciência, Vasconcelos, Inhoaíba e Santa Cruz</span></div>
</div></div></section>'''
    ticker_items = "".join(f"<li>{s['short']}</li>" for s in SERVICES)
    ticker = f'<div class="ticker" aria-hidden="true"><ul>{ticker_items}{ticker_items}{ticker_items}</ul></div>'
    services = f'''<section class="sec"><div class="wrap">
{sec_head("Serviços", "Cílios no <em>efeito</em> que combina com você", "Cinco técnicas para cada estilo de olhar, do mais natural ao mais marcante. Toque em uma delas para conhecer.")}
{service_cards()}{extras_block()}</div></section>'''
    how = f'''<section class="sec plum"><div class="wrap">
{sec_head("Como funciona", "Do WhatsApp ao olhar <em>pronto</em>", "Um atendimento pensado para você ter conforto e atenção do começo ao fim.")}
{steps_html()}
<div class="btns" style="justify-content:center;margin-top:54px">{wa_btn("Quero agendar","light","como-funciona")}</div></div></section>'''
    about = f'''<section class="sec"><div class="wrap"><div class="split">
<div class="media arch2 rv">{pic("lavinia-monteiro-lash-designer-2", "Lavínia Monteiro, lash designer, com pinças de extensão de cílios", sizes="(min-width:980px) 520px, 90vw")}</div>
<div class="rv d1"><span class="eyebrow">Quem sou</span>
<h2>Cuidado com cada <em>fio</em>, conforto na sua casa</h2>
<p>Sou a Lavínia Monteiro, lash designer em Cosmos, no Rio de Janeiro. Meu trabalho é realçar o seu olhar com extensão de cílios feita com calma, técnica e atenção ao formato dos seus olhos e aos seus cílios naturais.</p>
{checks(["<b>Atendimento a domicílio:</b> você não perde tempo no trânsito", "<b>Hora marcada:</b> atenção exclusiva para você", "<b>Aplicação cuidadosa:</b> que respeita seus fios naturais"])}
<a class="btn ghost" href="/quem-sou/">Conheça minha história</a></div></div></div></section>'''
    results = f'''<section class="sec blush"><div class="wrap">
{sec_head("Clientes", "Olhares que <em>saem</em> daqui", "Alguns resultados dos atendimentos. Toque para ampliar.")}
{mosaic(HOME_GALLERY)}
<div class="btns" style="justify-content:center;margin-top:44px"><a class="btn ghost" href="/clientes/">Ver mais resultados</a>{ig_btn("Ver no Instagram")}</div></div></section>'''
    areas = f'''<section class="sec"><div class="wrap">
{sec_head("Onde atendo", "Na sua casa, em <em>seis bairros</em> do Rio", "Atendimento a domicílio a partir de Cosmos. Confira os bairros e chame no WhatsApp se o seu não estiver na lista.")}
{chips()}
<p class="center rv" style="margin-top:34px"><a class="more" href="/atendimento/">Ver todas as regiões</a></p></div></section>'''
    faq = f'''<section class="sec blush"><div class="wrap">
{sec_head("Dúvidas frequentes", "Perguntas <em>mais</em> comuns")}
<div class="rv">{faq_html(HOME_FAQ)}</div></div></section>'''
    blog = f'''<section class="sec"><div class="wrap">
{sec_head("Blog", "Tudo sobre <em>extensão de cílios</em>", "Guias práticos para você escolher a técnica, cuidar dos cílios e tirar dúvidas.")}
{post_cards(ARTICLES[:3])}
<p class="center rv" style="margin-top:34px"><a class="more" href="/blog/">Ver todos os artigos</a></p></div></section>'''
    body = hero + ticker + services + how + about + results + (testimonials_section() or why_section()) + areas + faq + blog + final_cta()
    add("/", "Extensão de Cílios em Cosmos e Campo Grande RJ | Lavínia Monteiro",
        "Lash designer a domicílio em Cosmos, Campo Grande, Paciência, Inhoaíba e Santa Cruz (RJ). Fio a fio, volumes e Fox Eyes. Agende pelo WhatsApp.",
        body, [SCH_BUSINESS, WEBSITE, faq_schema(HOME_FAQ)])

# ===================== QUEM SOU =====================
def about():
    trail = [("Início", "/"), ("Quem sou", "/quem-sou/")]
    stats = (f'<section class="stats"><div class="wrap"><div class="stat rv"><b>2024</b><span>comecei a transformar olhares</span></div>'
             f'<div class="stat rv d1"><b>5</b><span>técnicas de extensão</span></div>'
             f'<div class="stat rv d2"><b>+2</b><span>manutenção e remoção</span></div>'
             f'<div class="stat rv d3"><b>6</b><span>bairros atendidos em casa</span></div></div></section>')
    body = f'''<section class="phero"><div class="wrap"><div class="split">
<div class="rv">{crumbs_html(trail)}<span class="eyebrow">Quem sou</span>
<h1>Lavínia Monteiro, <em>lash designer</em> em Cosmos</h1>
<p class="lead">Desde 2024 eu transformo olhares, um fio de cada vez, e levo esse cuidado até a sua casa.</p></div>
<div class="media arch2 rv d1">{pic("lavinia-monteiro-lash-designer", "Lavínia Monteiro, lash designer em Cosmos, RJ", sizes="(min-width:980px) 520px, 90vw", eager=True)}</div></div></div></section>
{stats}
<section class="sec"><div class="wrap narrow prose rv">
<h2>Tudo começou em <em>2024</em></h2>
<p>Foi em 2024 que a extensão de cílios entrou na minha vida, e nunca mais saiu. O que começou como encantamento por uma técnica tão delicada virou profissão e, logo depois, paixão: realçar o olhar de cada mulher sem tirar dela o que ela tem de mais único.</p>
<p>Desde então, cada atendimento é um novo aprendizado. Estudo o formato dos olhos, observo como cada cílio natural cresce, treino o mapeamento, aperfeiçoo o toque. Porque aplicar um fio em um cílio fino como seda pede paciência, mão firme e muito respeito pelo que já é seu.</p>
<h2>Um fio de cada vez</h2>
<p>Acredito que a beleza que vale a pena é aquela que combina com você. Por isso não existe um olhar padrão: existe o seu estilo, a sua rotina e o efeito que faz você se sentir bem quando se olha no espelho. Antes de começar, a gente conversa, eu entendo o que você imagina e só então escolho, com você, a técnica e o mapeamento ideais, do <a href="/servicos/extensao-de-cilios-fio-a-fio/">fio a fio</a> delicado ao <a href="/servicos/mega-volume-egipcio/">mega volume</a> marcante.</p>
<blockquote>O melhor momento do atendimento é quando você abre os olhos e se enxerga no espelho.</blockquote>
<h2>Por que eu vou até você</h2>
<p>Escolhi atender a domicílio porque cuidar de si deveria ser leve. Sem trânsito, sem pressa, sem precisar sair de casa: você se deita, respira fundo e eu cuido do resto, com hora marcada e atenção só para você.</p>
<p>Atendo em Cosmos, Campo Grande, Paciência, Senador Vasconcelos, Inhoaíba e Santa Cruz, e o cuidado não termina na aplicação: também faço <a href="/servicos/manutencao-de-cilios/">manutenção</a> para manter o olhar sempre bonito e <a href="/servicos/remocao-de-cilios/">remoção</a> feita com todo o cuidado para preservar os seus cílios naturais.</p>
</div></section>
<section class="sec blush"><div class="wrap">
{sec_head("Meu jeito de trabalhar", "O que você pode <em>esperar</em> de mim")}
<div class="contact-grid" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">
<div class="ccard rv" style="text-align:left"><h3>Conversa antes de tudo</h3><p>Antes de começar, entendo o efeito que você quer e avalio os seus cílios naturais e o formato dos seus olhos.</p></div>
<div class="ccard rv d1" style="text-align:left"><h3>Aplicação cuidadosa</h3><p>Um fio de cada vez, com calma e técnica, para preservar os seus fios naturais e entregar um resultado bonito e confortável.</p></div>
<div class="ccard rv d2" style="text-align:left"><h3>Atendimento exclusivo</h3><p>Hora marcada, atenção só para você e todo o conforto da sua casa. Sem fila, sem pressa e sem deslocamento.</p></div>
<div class="ccard rv d3" style="text-align:left"><h3>Orientação no pós</h3><p>Explico como cuidar das suas extensões para que durem mais e continuem lindas, e estou por aqui para tirar dúvidas.</p></div>
</div></div></section>
<section class="sec"><div class="wrap">
{sec_head("O que eu faço", "Técnicas, manutenção e <em>cuidado</em>", "Escolho com você a técnica que mais combina com o seu estilo.")}
{service_cards()}{extras_block()}</div></section>
<section class="sec blush"><div class="wrap"><div class="split rev">
<div class="media rv">{pic("lavinia-monteiro-lash-designer-2", "Lavínia Monteiro com pinças e escovinha de cílios", sizes="(min-width:980px) 520px, 90vw")}</div>
<div class="rv d1"><span class="eyebrow">Fale comigo</span><h2>Vamos conversar sobre o <em>seu olhar</em>?</h2>
<p>Me chame no WhatsApp ou acompanhe meu trabalho no Instagram. Vou adorar te conhecer e ajudar você a escolher o efeito ideal. Valores e horários eu passo direto por lá.</p>
<div class="btns">{wa_btn("Chamar no WhatsApp")}{ig_btn()}</div></div></div></div></section>'''
    profile = {"@context": "https://schema.org", "@type": "ProfilePage", "mainEntity": {"@id": SITE_URL + "/#lavinia"}, "url": SITE_URL + "/quem-sou/", "inLanguage": "pt-BR"}
    add("/quem-sou/", "Quem Sou | Lavínia Monteiro, Lash Designer em Cosmos RJ",
        "Conheça a Lavínia Monteiro, lash designer em Cosmos, Rio de Janeiro, desde 2024. Extensão de cílios a domicílio com técnica, cuidado e atenção a cada detalhe.",
        body + review_invite() + final_cta(), [SCH_BUSINESS, profile, crumbs_schema(trail)])

# ===================== SERVIÇOS =====================
def services_pages():
    trail = [("Início", "/"), ("Serviços", "/servicos/")]
    cmp_rows = [("Fio a fio", "Um fio em cada cílio natural", "Natural, delicado, leve"),
                ("Volume brasileiro", "Fios em formato Y", "Preenchido, leve e natural"),
                ("Volume egípcio", "Leques de fios finos", "Mais cheio e definido"),
                ("Mega volume egípcio", "Leques com mais fios ultrafinos", "Bem cheio, denso e marcante"),
                ("Volume Fox Eyes", "Mapeamento que alonga o canto externo", "Olhar alongado e levantado")]
    table = '<div class="prose" style="overflow-x:auto"><table><thead><tr><th>Técnica</th><th>Como é</th><th>Efeito</th></tr></thead><tbody>' + \
        "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in cmp_rows) + "</tbody></table></div>"
    body = f'''<section class="phero"><div class="wrap center">{crumbs_html(trail)}<span class="eyebrow">Serviços</span>
<h1>Extensão de cílios a domicílio em <em>Cosmos</em> e Campo Grande</h1>
<p class="lead">Fio a fio, volume egípcio, volume brasileiro, mega volume egípcio e Fox Eyes, além de manutenção e remoção. Escolha o efeito que combina com você e eu vou até a sua casa.</p></div></section>
<section class="sec"><div class="wrap">{service_cards()}{extras_block()}</div></section>
<section class="sec blush"><div class="wrap narrow">
{sec_head("Comparativo", "Qual técnica <em>escolher</em>?", "Um resumo para você comparar. Em dúvida? Eu te ajudo pelo WhatsApp.")}
<div class="rv">{table}</div>
<p class="center rv" style="margin-top:30px"><a class="more" href="/blog/fio-a-fio-volume-egipcio-brasileiro-qual-escolher/">Ler o guia completo de técnicas</a></p></div></section>
<section class="sec"><div class="wrap narrow center rv">
<span class="eyebrow">Atendimento a domicílio</span><h2>Eu vou até <em>você</em></h2>
<p class="lead">Todos os serviços são feitos na sua casa, com hora marcada, em Cosmos, Campo Grande, Paciência, Senador Vasconcelos, Inhoaíba e Santa Cruz. Valores e horários eu passo pelo WhatsApp.</p>
{chips()}</div></section>'''
    add("/servicos/", "Serviços de Extensão de Cílios em Cosmos e Campo Grande RJ",
        "Fio a fio, volume egípcio, brasileiro, mega volume, Fox Eyes, manutenção e remoção de cílios a domicílio em Cosmos e Campo Grande, RJ. Agende.",
        body + final_cta(), [SCH_BUSINESS, crumbs_schema(trail)])

    for s in SERVICES + EXTRA_SERVICES:
        extra = s in EXTRA_SERVICES
        t = trail + [(s["short"], f"/servicos/{s['slug']}/")]
        what = "".join(f"<p>{p}</p>" for p in s["what"])
        svc_schema = {"@context": "https://schema.org", "@type": "Service", "name": s["name"] + " a domicílio",
                      "serviceType": s["name"], "provider": {"@id": SITE_URL + "/#negocio"},
                      "areaServed": [{"@type": "Place", "name": f"{a}, Rio de Janeiro - RJ"} for a in AREAS],
                      "description": s["desc"], "url": f"{SITE_URL}/servicos/{s['slug']}/"}
        faq_title = ("Perguntas sobre " + ("Fox Eyes" if s["short"] == "Volume Fox Eyes" else s["short"].lower()))
        if extra:
            others = f'{sec_head("Técnicas", "Conheça as técnicas de <em>extensão</em>")}{service_cards()}'
        else:
            others = (f'{sec_head("Outras técnicas", "Conheça também")}{service_cards(exclude=s["slug"])}'
                      f'<p class="center rv" style="margin-top:34px">Também faço <a class="more" href="/servicos/manutencao-de-cilios/">manutenção</a> &nbsp; e &nbsp; <a class="more" href="/servicos/remocao-de-cilios/">remoção</a></p>')
        body = f'''<section class="phero"><div class="wrap"><div class="split">
<div class="rv">{crumbs_html(t)}<span class="eyebrow">{s["short"]}</span><h1>{s["h1"]}</h1>
<p class="lead">{s["lead"]}</p><div class="btns" style="margin-top:28px">{wa_btn()}</div></div>
<div class="media arch2 rv d1">{pic(s["photo"], "Resultado de " + s["name"].lower() + " por Lavínia Monteiro, lash designer em Cosmos RJ", sizes="(min-width:980px) 520px, 90vw", eager=True, style="aspect-ratio:4/5;object-position:" + s["pos"])}</div>
</div></div></section>
<section class="sec"><div class="wrap narrow prose rv"><h2>{s["what_h2"]}</h2>{what}</div></section>
{results_section(s)}
<section class="sec blush"><div class="wrap"><div class="split">
<div class="rv"><span class="eyebrow">Para quem é</span><h2>{s.get("for_h2", "Essa técnica é <em>para você</em> se…")}</h2>{checks(s["for"])}</div>
<div class="rv d1 prose"><h3>Atendimento em casa, em Cosmos e Campo Grande</h3>
<p>Eu vou até você, com hora marcada. Atendo em <a href="/atendimento/cosmos/">Cosmos</a>, <a href="/atendimento/campo-grande/">Campo Grande (RJ)</a>, Paciência, Senador Vasconcelos, Inhoaíba e Santa Cruz.</p>
<p>Para saber valores e horários disponíveis, é só me chamar no WhatsApp.</p>
<div class="btns">{wa_btn("Quero agendar")}</div></div></div></div></section>
<section class="sec plum"><div class="wrap">{sec_head("Como funciona", "Do primeiro contato ao <em>olhar pronto</em>")}{steps_html()}</div></section>
<section class="sec"><div class="wrap">{sec_head("Dúvidas", faq_title)}<div class="rv">{faq_html(s["faq"])}</div></div></section>
<section class="sec blush"><div class="wrap">{others}</div></section>'''
        add(f"/servicos/{s['slug']}/", s["title"], s["desc"], body + final_cta(), [SCH_BUSINESS, svc_schema, faq_schema(s["faq"]), crumbs_schema(t)],
            og_image=f"/assets/img/{s['photo']}.webp")

LOCAL_PREP = ("<h2>Como funciona o atendimento em casa em {local}</h2>"
  "<p>É simples: você me chama no WhatsApp, combinamos o efeito e o horário, e eu chego na sua casa com tudo o que preciso. Para o atendimento ficar perfeito, basta:</p>"
  "<ul><li>Escolher um cantinho confortável e bem iluminado, onde você possa ficar deitada ou reclinada;</li>"
  "<li>Chegar com o rosto limpo, sem máscara de cílios, curvex ou maquiagem nos olhos;</li>"
  "<li>Retirar as lentes de contato, se usar;</li>"
  "<li>Me avisar sobre alergias ou sensibilidade nos olhos.</li></ul>"
  "<p>Quer mais detalhes? Leia <a href=\"/blog/extensao-de-cilios-a-domicilio-como-funciona/\">como funciona a extensão de cílios a domicílio</a>.</p>")

# ===================== ATENDIMENTO =====================
def areas():
    trail = [("Início", "/"), ("Onde atendo", "/atendimento/")]
    hub_faq = [("Meu bairro não está na lista. Você atende?", "Atendo em Cosmos, Campo Grande, Paciência, Senador Vasconcelos, Inhoaíba e Santa Cruz. Se o seu bairro não aparece, chame no WhatsApp com o seu endereço aproximado e eu te digo se consigo atender."),
               ("Preciso ir até algum lugar?", "Não. O atendimento é a domicílio: eu vou até a sua casa, com hora marcada.")]
    body = f'''<section class="phero"><div class="wrap center">{crumbs_html(trail)}<span class="eyebrow">Onde atendo</span>
<h1>Extensão de cílios a domicílio em Cosmos, Campo Grande e <em>mais 4 bairros</em></h1>
<p class="lead">Atendo na sua casa em Cosmos, Campo Grande e região. Escolha a sua localidade para saber mais.</p></div></section>
<section class="sec"><div class="wrap"><div class="cards" style="grid-template-columns:repeat(auto-fit,minmax(300px,1fr));max-width:900px;margin:0 auto">
<a class="card rv" href="/atendimento/cosmos/"><div class="tx" style="padding:38px 34px"><span class="eyebrow">Atendimento principal</span><h3>Cílios em Cosmos</h3><p>Lash designer a domicílio em Cosmos, Rio de Janeiro. Fio a fio, volumes e Fox Eyes na sua casa.</p><span class="more">Ver página</span></div></a>
<a class="card rv d1" href="/atendimento/campo-grande/"><div class="tx" style="padding:38px 34px"><span class="eyebrow">Rio de Janeiro</span><h3>Cílios em Campo Grande RJ</h3><p>Extensão de cílios a domicílio em Campo Grande, no Rio de Janeiro, com hora marcada.</p><span class="more">Ver página</span></div></a>
</div></div></section>
<section class="sec blush"><div class="wrap">{sec_head("Outras regiões", "Também atendo em", "Chame no WhatsApp para confirmar a disponibilidade no seu bairro.")}{chips(False)}</div></section>
<section class="sec"><div class="wrap">{sec_head("Dúvidas", "Sobre o <em>atendimento</em>")}<div class="rv">{faq_html(hub_faq)}</div></div></section>'''
    add("/atendimento/", "Onde Atendo | Cílios a Domicílio em Cosmos e Campo Grande RJ",
        "Extensão de cílios a domicílio em Cosmos, Campo Grande, Paciência, Senador Vasconcelos, Inhoaíba e Santa Cruz, no Rio de Janeiro. Veja e agende.",
        body + final_cta(), [SCH_BUSINESS, faq_schema(hub_faq), crumbs_schema(trail)])

    def local_page(slug, nome, title, desc, h1, lead, paras, faq, extra=""):
        t = trail + [(nome, f"/atendimento/{slug}/")]
        pr = "".join(paras)
        body = f'''<section class="phero"><div class="wrap"><div class="split"><div class="rv">{crumbs_html(t)}<span class="eyebrow">{nome} · Rio de Janeiro</span><h1>{h1}</h1><p class="lead">{lead}</p>
<div class="btns" style="margin-top:28px">{wa_btn()}</div></div>
<div class="media arch2 rv d1">{pic("lavinia-monteiro-lash-designer", "Lavínia Monteiro, lash designer a domicílio em " + nome + ", RJ", sizes="(min-width:980px) 520px, 90vw", eager=True, style="aspect-ratio:4/5;object-position:50% 25%")}</div></div></div></section>
<section class="sec"><div class="wrap narrow prose rv">{pr}{extra}</div></section>
<section class="sec blush"><div class="wrap">{sec_head("Serviços", f"Técnicas que eu faço em {nome}")}{service_cards()}</div></section>
<section class="sec plum"><div class="wrap">{sec_head("Como funciona", "Simples, do <em>início ao fim</em>")}{steps_html()}</div></section>
<section class="sec"><div class="wrap">{sec_head("Dúvidas", f"Perguntas sobre cílios em {nome}")}<div class="rv">{faq_html(faq)}</div></div></section>
<section class="sec blush"><div class="wrap">{sec_head("Região de atendimento", "Bairros que eu <em>atendo</em>")}{chips()}</div></section>'''
        add(f"/atendimento/{slug}/", title, desc, body + final_cta(), [SCH_BUSINESS, faq_schema(faq), crumbs_schema(t)])

    cosmos_faq = [
     ("Tem lash designer que atende em casa em Cosmos?", "Tem: eu, Lavínia Monteiro. Sou lash designer em Cosmos e atendo a domicílio, com hora marcada, fazendo extensão de cílios fio a fio, volume egípcio, volume brasileiro, mega volume egípcio e Fox Eyes."),
     ("Preciso sair de Cosmos para fazer extensão de cílios?", "Não. Você faz a extensão na sua casa, no seu bairro. Eu levo tudo o que é necessário e você só precisa de um cantinho confortável e bem iluminado."),
     ("Você atende em qual parte de Cosmos?", "Atendo em Cosmos e nos bairros próximos. Para confirmar a disponibilidade na sua rua, chame no WhatsApp e informe o seu endereço aproximado."),
     ("Como agendo a extensão de cílios em Cosmos?", "Clique em qualquer botão de WhatsApp do site, conte o efeito que você quer e combinamos dia e horário."),
    ]
    local_page("cosmos", "Cosmos",
        "Extensão de Cílios em Cosmos RJ | Lash Designer a Domicílio",
        "Lash designer a domicílio em Cosmos, Rio de Janeiro. Fio a fio, volume egípcio, brasileiro, mega volume e Fox Eyes. Eu vou até você. Agende no WhatsApp.",
        "Extensão de cílios em <em>Cosmos</em>, RJ, na sua casa",
        "Sou a Lavínia, lash designer em Cosmos. Faço sua extensão de cílios no conforto de casa, com hora marcada e atendimento só para você.",
        ["<h2>Lash designer em Cosmos que vai até você</h2><p>Se você mora em Cosmos, no Rio de Janeiro, e procura uma lash designer perto de você, eu vou até a sua casa. Em vez de tirar um dia para ir até um estúdio, você faz a sua extensão de cílios no seu sofá ou na sua cama, sem trânsito e sem pressa.</p>",
         "<h2>Técnicas de extensão de cílios disponíveis em Cosmos</h2><p>Cada atendimento recebe o tempo e a atenção que o seu olhar merece, seja uma aplicação nova, uma <a href=\"/servicos/manutencao-de-cilios/\">manutenção</a> ou uma <a href=\"/servicos/remocao-de-cilios/\">remoção</a>. Antes de começar, conversamos sobre o efeito que você quer, desde o <a href=\"/servicos/extensao-de-cilios-fio-a-fio/\">fio a fio</a>, mais natural, até o <a href=\"/servicos/mega-volume-egipcio/\">mega volume egípcio</a>, mais marcante, passando pelo <a href=\"/servicos/volume-egipcio/\">volume egípcio</a>, pelo <a href=\"/servicos/volume-brasileiro/\">volume brasileiro</a> e pelo <a href=\"/servicos/volume-fox-eyes/\">Fox Eyes</a>.</p>" + LOCAL_PREP.format(local="Cosmos"),
         "<h2>Atendimento em Cosmos e bairros vizinhos</h2><p>Além de Cosmos, também atendo moradoras de Campo Grande, Paciência, Senador Vasconcelos, Inhoaíba e Santa Cruz. Quer conferir o meu perfil? <a href=\"" + MAPS + "\" target=\"_blank\" rel=\"noopener\">Encontre a Lavínia Monteiro | Lash Designer no Google Maps</a>.</p>"],
        cosmos_faq)

    cg_faq = [
     ("Você atende em Campo Grande, no Rio de Janeiro?", "Sim. Atendo a domicílio em Campo Grande, na Zona Oeste do Rio de Janeiro (RJ), com hora marcada. Para confirmar a disponibilidade no seu endereço, chame no WhatsApp."),
     ("Esse atendimento é em Campo Grande RJ ou Campo Grande MS?", "É em Campo Grande, no Rio de Janeiro (RJ). Não atendo em Campo Grande, no Mato Grosso do Sul."),
     ("Preciso ir até um estúdio em Campo Grande?", "Não. Eu vou até você, então você faz a extensão de cílios no conforto da sua casa."),
     ("Como agendo extensão de cílios em Campo Grande RJ?", "Pelo WhatsApp. Conte o efeito que você quer e combinamos dia e horário."),
    ]
    local_page("campo-grande", "Campo Grande RJ",
        "Extensão de Cílios em Campo Grande RJ | Lash a Domicílio",
        "Extensão de cílios a domicílio em Campo Grande, Rio de Janeiro (RJ). Fio a fio, volumes e Fox Eyes com hora marcada. Eu vou até você. Agende no WhatsApp.",
        "Extensão de cílios em <em>Campo Grande RJ</em>, a domicílio",
        "Lash designer a domicílio em Campo Grande, Rio de Janeiro. Eu vou até você, com hora marcada, para um olhar bonito sem sair de casa.",
        ["<h2>Extensão de cílios em Campo Grande, sem sair de casa</h2><p>Procurando extensão de cílios em Campo Grande, no Rio de Janeiro? Eu atendo a domicílio: vou até a sua casa, com tudo o que preciso, e você faz o procedimento deitada, relaxada e sem precisar enfrentar o trânsito da Zona Oeste.</p>",
         "<h2>Qual técnica escolher</h2><p>Escolha a técnica que mais combina com você: <a href=\"/servicos/extensao-de-cilios-fio-a-fio/\">fio a fio</a> para um olhar natural, <a href=\"/servicos/volume-brasileiro/\">volume brasileiro</a> ou <a href=\"/servicos/volume-egipcio/\">volume egípcio</a> para mais preenchimento, <a href=\"/servicos/mega-volume-egipcio/\">mega volume egípcio</a> para um olhar bem marcante, ou <a href=\"/servicos/volume-fox-eyes/\">Fox Eyes</a> para alongar e levantar os olhos.</p>" + LOCAL_PREP.format(local="Campo Grande"),
         "<h2>Atendimento em Campo Grande e região</h2><p>Sou de Cosmos, bairro vizinho de Campo Grande, e atendo também Paciência, Senador Vasconcelos, Inhoaíba e Santa Cruz. Sempre com hora marcada e atenção exclusiva, para você ter a sua melhor experiência.</p>"],
        cg_faq,
        extra='<div class="callout"><p><strong>Campo Grande RJ, não MS.</strong> Meu atendimento é em Campo Grande, na Zona Oeste do Rio de Janeiro (RJ).</p></div>')

# ===================== CLIENTES =====================
def clients():
    trail = [("Início", "/"), ("Clientes", "/clientes/")]
    body = f'''<section class="phero"><div class="wrap center">{crumbs_html(trail)}<span class="eyebrow">Clientes</span>
<h1>Resultados de <em>extensão de cílios</em> das minhas clientes</h1>
<p class="lead">Olhares reais, atendidos em casa, em Cosmos, Campo Grande e região. Toque em uma foto para ampliar.</p></div></section>
<section class="sec"><div class="wrap">{clients_gallery()}
<div class="btns" style="justify-content:center;margin-top:48px">{wa_btn("Quero o meu olhar assim")}{ig_btn("Mais fotos no Instagram")}</div></div></section>
<section class="sec blush"><div class="wrap">{sec_head("Escolha a sua", "Cada olhar pede um <em>efeito</em>")}{service_cards()}</div></section>''' + testimonials_section() + review_invite()
    add("/clientes/", "Clientes e Resultados | Extensão de Cílios em Cosmos RJ",
        "Veja resultados reais de extensão de cílios feitos por Lavínia Monteiro, lash designer a domicílio em Cosmos e Campo Grande, RJ.",
        body + final_cta(), [SCH_BUSINESS, crumbs_schema(trail)])

# ===================== BLOG =====================
def blog():
    trail = [("Início", "/"), ("Blog", "/blog/")]
    body = f'''<section class="phero"><div class="wrap center">{crumbs_html(trail)}<span class="eyebrow">Blog</span>
<h1>Tudo sobre <em>extensão de cílios</em></h1>
<p class="lead">Guias práticos para escolher a técnica, cuidar das suas extensões e tirar as dúvidas mais comuns.</p></div></section>
<section class="sec"><div class="wrap">{post_cards(ARTICLES)}</div></section>'''
    add("/blog/", "Blog de Extensão de Cílios | Lavínia Monteiro Lash Designer",
        "Dicas e guias sobre extensão de cílios: técnicas, cuidados, manutenção, valores e dúvidas. Por Lavínia Monteiro, lash designer em Cosmos, RJ.",
        body + final_cta(), [SCH_BUSINESS, crumbs_schema(trail)])
    cta = BLOG_CTA.replace("{WA}", wa_btn("Agendar pelo WhatsApp", "light", "blog"))
    for a in ARTICLES:
        t = trail + [(a["h1"], f"/blog/{a['slug']}/")]
        content = a["html"].replace("{CTA}", cta)
        others = [x for x in ARTICLES if x["slug"] != a["slug"]][:3]
        faq = ""
        if a.get("faq"):
            faq = f'<section class="sec blush"><div class="wrap">{sec_head("Perguntas rápidas", "Resposta <em>direta</em>")}<div class="rv">{faq_html(a["faq"])}</div></div></section>'
        schema = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["h1"], "description": a["desc"],
                  "image": f"{SITE_URL}/assets/img/{a['photo']}.webp", "datePublished": TODAY, "dateModified": TODAY,
                  "inLanguage": "pt-BR", "mainEntityOfPage": f"{SITE_URL}/blog/{a['slug']}/",
                  "author": {"@id": SITE_URL + "/#lavinia"}, "about": a["tag"], "isPartOf": {"@id": SITE_URL + "/#site"},
                  "publisher": {"@id": SITE_URL + "/#negocio"}}
        sch = [SCH_BUSINESS, schema, crumbs_schema(t)] + ([faq_schema(a["faq"])] if a.get("faq") else [])
        body = f'''<article class="article"><div class="wrap narrow">{crumbs_html(t)}
<span class="eyebrow">{a["tag"]}</span><h1>{a["h1"]}</h1>
<p class="meta">Por <a href="/quem-sou/">Lavínia Monteiro</a>, lash designer · <time datetime="{TODAY}">12 de novembro de 2026</time> · {a["min"]} min de leitura</p>
{pic(a["photo"], a["h1"], sizes="(min-width:800px) 760px, 100vw", eager=True, style="width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:20px;margin-bottom:2.2rem")}
<div class="callout tldr"><p><strong>Resposta rápida:</strong> {a["tldr"]}</p></div><div class="prose">{content}</div></div></article>{faq}
<section class="sec"><div class="wrap">{sec_head("Continue lendo", "Outros <em>artigos</em>")}{post_cards(others)}</div></section>'''
        add(f"/blog/{a['slug']}/", a["title"], a["desc"], body, sch, og_image=f"/assets/img/{a['photo']}.webp", og_type="article")

# ===================== CONTATO =====================
def contact():
    trail = [("Início", "/"), ("Contato", "/contato/")]
    faq = HOME_FAQ[4:6] + [HOME_FAQ[0]]
    body = f'''<section class="phero"><div class="wrap center">{crumbs_html(trail)}<span class="eyebrow">Contato</span>
<h1>Vamos <em>conversar</em> sobre o seu olhar?</h1>
<p class="lead">O jeito mais rápido de agendar é pelo WhatsApp. Conte o efeito que você quer, e eu respondo com valores e horários disponíveis.</p></div></section>
<section class="sec"><div class="wrap"><div class="contact-grid">
<div class="ccard rv">{ICON_WA}<h3>WhatsApp</h3><p>{PHONE_DISPLAY}<br>Agendamentos, valores e dúvidas.</p><div class="btns" style="justify-content:center">{wa_btn("Chamar agora")}</div></div>
<div class="ccard rv d1">{ICON_IG}<h3>Instagram</h3><p>{INSTAGRAM_USER}<br>Veja o meu trabalho e novidades.</p><div class="btns" style="justify-content:center">{ig_btn("Abrir Instagram")}</div></div>
<div class="ccard rv d2">{ICON_PIN}<h3>Atendimento a domicílio</h3><p>Cosmos, Campo Grande, Paciência, Sen. Vasconcelos, Inhoaíba e Santa Cruz.<br>Sempre com hora marcada.</p><div class="btns" style="justify-content:center"><a class="btn ghost" href="/atendimento/">Ver regiões</a></div></div>
</div></div></section>
<section class="sec blush"><div class="wrap">{sec_head("Antes de agendar", "Perguntas <em>frequentes</em>")}<div class="rv">{faq_html(faq)}</div></div></section>
<section class="sec"><div class="wrap narrow center rv"><span class="eyebrow">Google</span><h2>Encontre a Lavínia no <em>Google Maps</em></h2>
<p class="lead">Veja o perfil da Lavínia Monteiro | Lash Designer no Google, em Cosmos, Rio de Janeiro.</p>
<div class="btns" style="justify-content:center"><a class="btn ghost" href="{MAPS}" target="_blank" rel="noopener">{ICON_PIN}<span>Abrir no Google Maps</span></a></div></div></section>'''
    add("/contato/", "Contato e Agendamento | Lavínia Monteiro Lash Designer",
        "Agende sua extensão de cílios a domicílio em Cosmos, Campo Grande e região (RJ). Fale com a Lavínia pelo WhatsApp (21) 98842-0844.",
        body + final_cta("Pronta para o seu novo olhar?"), [SCH_BUSINESS, faq_schema(faq), crumbs_schema(trail)])


# ===================== PÁGINAS LEGAIS =====================
LEGAL_UPDATED = "12 de novembro de 2026"

def legal_page(slug, title, desc, h1, body_html):
    path = f"/{slug}/"
    trail = [("Início", "/"), (h1, path)]
    body = (f'<section class="phero"><div class="wrap narrow">{crumbs_html(trail)}<span class="eyebrow">Informações legais</span><h1>{h1}</h1>'
            f'<p class="lead">Última atualização: {LEGAL_UPDATED}.</p></div></section>'
            f'<section class="sec"><div class="wrap narrow prose legalpage">{body_html}</div></section>')
    add(path, title, desc, body, [SCH_BUSINESS, crumbs_schema(trail)])

def legal():
    contato = (f'<p>Para qualquer assunto sobre esta página ou sobre os seus dados, fale com a Lavínia pelo WhatsApp '
               f'<a href="{WA_URL}" target="_blank" rel="noopener">{PHONE_DISPLAY}</a>.</p>')
    legal_page("politica-de-privacidade", "Política de Privacidade | Lavínia Monteiro Lash Designer",
        "Como o site da Lavínia Monteiro | Lash Designer trata dados pessoais, de acordo com a LGPD (Lei 13.709/2018).",
        "Política de Privacidade", f"""
<p>Esta Política explica como o site <strong>{SITE_URL}</strong>, de <strong>Lavínia Monteiro | Lash Designer</strong>, trata dados pessoais, em conformidade com a Lei Geral de Proteção de Dados (LGPD, Lei nº 13.709/2018).</p>

<h2>1. Quem é a responsável</h2>
<p>A controladora dos dados é Lavínia Monteiro, lash designer com atendimento a domicílio em Cosmos, no Rio de Janeiro (RJ). Contato: WhatsApp {PHONE_DISPLAY}.</p>

<h2>2. Quais dados são tratados</h2>
<ul>
<li><strong>Dados que você envia ao chamar no WhatsApp ou Instagram:</strong> nome, telefone, bairro, endereço aproximado para o atendimento, preferências de serviço e as informações que você escolher compartilhar (por exemplo, alergias ou sensibilidade nos olhos). Essa conversa acontece nas plataformas WhatsApp e Instagram, e não dentro deste site.</li>
<li><strong>Dados de uso do site (estatística):</strong> com o seu consentimento, usamos o Google Analytics 4 para medir visitas, páginas acessadas, tempo de permanência, rolagem e cliques em botões (WhatsApp, Instagram e Google Maps) e na abertura de fotos. Essas medições são estatísticas e não nos permitem saber quem é você. Se você recusar, nenhum cookie de estatística é gravado.</li>
<li><strong>Dados técnicos de acesso:</strong> como em qualquer site, o servidor de hospedagem pode registrar de forma automática dados como endereço IP, data e hora, páginas acessadas, tipo de navegador e dispositivo. Esses registros servem para segurança e funcionamento do site.</li>
</ul>
<p>Este site <strong>não possui formulários, cadastro, comentários nem área de login</strong> e não coleta dados pessoais diretamente por campos de preenchimento.</p>

<h2>3. Para que usamos os dados</h2>
<ul>
<li>Responder mensagens, combinar horários e realizar o atendimento (execução do serviço solicitado);</li>
<li>Prestar orientações sobre cuidados antes e depois do procedimento;</li>
<li>Garantir a segurança e o bom funcionamento do site;</li>
<li>Cumprir obrigações legais, quando houver.</li>
</ul>

<h2>4. Bases legais</h2>
<p>O tratamento ocorre com base na <strong>execução de contrato ou de procedimentos preliminares</strong> a pedido da cliente, no <strong>consentimento</strong> (quando você compartilha informações voluntariamente, inclusive de saúde, como alergias), no <strong>legítimo interesse</strong> (segurança do site) e no <strong>cumprimento de obrigação legal</strong>.</p>

<h2>5. Com quem os dados podem ser compartilhados</h2>
<p>Não vendemos nem cedemos seus dados. Eles podem ser tratados por prestadores necessários ao funcionamento dos canais: a hospedagem do site (Vercel Inc.), o Google Analytics (Google LLC), o WhatsApp e o Instagram (Meta Platforms) e o Google Maps (Google). Cada um deles tem a sua própria política de privacidade.</p>

<h2>6. Por quanto tempo guardamos</h2>
<p>Mantemos as informações pelo tempo necessário para o atendimento e para o relacionamento com a cliente, e por prazos legais quando aplicável. Você pode pedir a exclusão a qualquer momento, observadas as obrigações legais.</p>

<h2>7. Fotos de clientes</h2>
<p>Fotos de resultados exibidas neste site são publicadas somente com a autorização da cliente. Se você aparece em uma foto e deseja que ela seja removida, é só pedir pelo contato abaixo.</p>

<h2>8. Seus direitos</h2>
<p>Conforme o art. 18 da LGPD, você pode solicitar: confirmação de que tratamos seus dados; acesso; correção de dados incompletos ou desatualizados; anonimização, bloqueio ou eliminação; portabilidade; informação sobre compartilhamento; e revogação do consentimento. Você também pode reclamar à Autoridade Nacional de Proteção de Dados (ANPD).</p>

<h2>9. Segurança</h2>
<p>O site é servido por conexão segura (HTTPS) e adotamos medidas razoáveis para proteger as informações. Nenhum sistema é totalmente imune a riscos, mas tratamos os dados com cuidado e apenas para as finalidades descritas.</p>

<h2>10. Links para outros sites</h2>
<p>O site contém links para serviços de terceiros (WhatsApp, Instagram e Google Maps). Ao clicar, você passa a ser regido pelas políticas dessas plataformas.</p>

<h2>11. Crianças e adolescentes</h2>
<p>Os serviços são destinados a pessoas adultas. Dados de menores só devem ser compartilhados com autorização de um responsável.</p>

<h2>12. Alterações desta Política</h2>
<p>Podemos atualizar esta Política para refletir mudanças no site ou na lei. A data da última atualização fica sempre no topo desta página.</p>

<h2>13. Contato</h2>
{contato}
<p>Veja também a <a href="/politica-de-cookies/">Política de Cookies</a> e os <a href="/termos-de-uso/">Termos de Uso</a>.</p>
""")

    legal_page("politica-de-cookies", "Política de Cookies | Lavínia Monteiro Lash Designer",
        "Quais cookies o site da Lavínia Monteiro | Lash Designer usa (Google Analytics, somente com seu consentimento) e como gerenciá-los.",
        "Política de Cookies", f"""
<p>Esta Política explica o uso de cookies e tecnologias semelhantes no site <strong>{SITE_URL}</strong>.</p>

<h2>1. O que são cookies</h2>
<p>Cookies são pequenos arquivos que um site pode salvar no seu navegador para lembrar preferências ou medir como o site é usado.</p>

<h2>2. Quais cookies usamos</h2>
<table>
<thead><tr><th>Tipo</th><th>Usado?</th><th>Detalhes</th></tr></thead>
<tbody>
<tr><td>Estritamente necessários</td><td>Não</td><td>O site funciona sem cookies. Guardamos apenas a sua escolha de cookies no armazenamento local do navegador (chave <code>lm_consent</code>).</td></tr>
<tr><td>Estatística (Google Analytics 4)</td><td>Somente se você aceitar</td><td>Cookies <code>_ga</code> e <code>_ga_*</code> (até 2 anos) para contar visitas e medir o uso do site, de forma estatística.</td></tr>
<tr><td>Marketing / publicidade</td><td>Não</td><td>Nenhum pixel de anúncios está ativo.</td></tr>
</tbody></table>

<h2>3. O que medimos</h2>
<p>Com o seu consentimento, medimos visitas e páginas acessadas, tempo no site, profundidade de rolagem, cliques nos botões de WhatsApp, Instagram e Google Maps, abertura de fotos e perguntas frequentes. Não coletamos nome, telefone nem outros dados que identifiquem você por meio dessas medições.</p>

<h2>4. Sua escolha</h2>
<p>Ao entrar no site, você vê um aviso com as opções <strong>Aceitar</strong> e <strong>Recusar</strong>. Se recusar, o Google Analytics não grava cookies no seu navegador. O Google pode receber apenas sinais técnicos agregados, sem cookies, para estatísticas gerais (Consent Mode). Você pode mudar de ideia a qualquer momento clicando em <strong>Gerenciar cookies</strong> no rodapé de qualquer página.</p>

<h2>5. Cookies de terceiros ao clicar em links</h2>
<p>Ao clicar em links para o WhatsApp, o Instagram ou o Google Maps, você sai deste site e acessa plataformas que podem usar seus próprios cookies, conforme as respectivas políticas. A hospedagem do site também pode registrar dados técnicos de acesso (como o endereço IP) em registros de servidor.</p>

<h2>6. Como gerenciar cookies no navegador</h2>
<p>Você também pode bloquear ou apagar cookies nas configurações do seu navegador (Chrome, Safari, Firefox, Edge), em geral em Configurações &gt; Privacidade e segurança.</p>

<h2>7. Contato</h2>
{contato}
<p>Veja também a <a href="/politica-de-privacidade/">Política de Privacidade</a>.</p>
""")

    legal_page("termos-de-uso", "Termos de Uso | Lavínia Monteiro Lash Designer",
        "Termos de uso do site da Lavínia Monteiro | Lash Designer: conteúdo, links externos, propriedade intelectual e agendamento.",
        "Termos de Uso", f"""
<p>Ao acessar o site <strong>{SITE_URL}</strong>, você concorda com os termos abaixo.</p>

<h2>1. Sobre o site</h2>
<p>Este site apresenta os serviços de extensão de cílios (fio a fio, volume egípcio, volume brasileiro, mega volume egípcio, Fox Eyes, manutenção e remoção) de Lavínia Monteiro | Lash Designer, com atendimento a domicílio em Cosmos, Campo Grande (RJ), Paciência, Senador Vasconcelos, Inhoaíba e Santa Cruz.</p>

<h2>2. Caráter informativo</h2>
<p>Os textos e os artigos do blog têm finalidade informativa e <strong>não substituem avaliação profissional nem orientação médica</strong>. Em caso de vermelhidão, coceira, ardência, inchaço ou qualquer desconforto nos olhos, procure um profissional de saúde.</p>

<h2>3. Resultados</h2>
<p>As fotos mostram resultados reais de atendimentos, mas o resultado varia de pessoa para pessoa, conforme o formato dos olhos, a condição dos cílios naturais, a técnica escolhida e os cuidados após a aplicação. Não há garantia de resultado idêntico ao das imagens.</p>

<h2>4. Agendamento, valores e horários</h2>
<p>Agendamentos, valores, horários disponíveis e eventuais condições são combinados diretamente com a Lavínia pelo WhatsApp. As informações do site não constituem proposta comercial vinculante.</p>

<h2>5. Propriedade intelectual</h2>
<p>Textos, fotos, logotipo, identidade visual e demais conteúdos deste site pertencem à Lavínia Monteiro | Lash Designer ou são usados com autorização. É proibida a reprodução, total ou parcial, sem permissão prévia, salvo citações com indicação da fonte.</p>

<h2>6. Links externos</h2>
<p>O site pode conter links para WhatsApp, Instagram, Google Maps e outros serviços de terceiros. Não controlamos esses ambientes e não nos responsabilizamos pelo seu conteúdo ou pelas suas políticas.</p>

<h2>7. Disponibilidade</h2>
<p>Buscamos manter o site sempre disponível e atualizado, mas ele pode ficar temporariamente indisponível ou conter informações desatualizadas.</p>

<h2>8. Privacidade e cookies</h2>
<p>O tratamento de dados está descrito na <a href="/politica-de-privacidade/">Política de Privacidade</a> e na <a href="/politica-de-cookies/">Política de Cookies</a>.</p>

<h2>9. Alterações e lei aplicável</h2>
<p>Estes Termos podem ser atualizados a qualquer momento, e a versão vigente é sempre a publicada nesta página. Eles são regidos pelas leis da República Federativa do Brasil.</p>

<h2>10. Contato</h2>
{contato}
""")

# ===================== EXTRAS =====================
def extras():
    # 404
    body = f'''<section class="phero"><div class="wrap center" style="padding:60px 0">{eye("mark")}<span class="eyebrow">Erro 404</span><h1>Essa página <em>não foi encontrada</em></h1>
<p class="lead">O endereço pode ter mudado ou não existe mais. Que tal voltar para o início ou chamar a Lavínia no WhatsApp?</p>
<div class="btns" style="justify-content:center;margin-top:28px"><a class="btn" href="/">Ir para o início</a>{wa_btn("Chamar no WhatsApp","ghost")}</div></div></section>'''
    html = render("/404.html", "Página não encontrada | Lavínia Monteiro Lash Designer", "Página não encontrada.", body, noindex=True)
    open(os.path.join(OUT, "404.html"), "w", encoding="utf8").write(html)
    # sitemap/robots
    urls = "".join(f"<url><loc>{SITE_URL}{p}</loc><lastmod>{TODAY}</lastmod></url>" for p in pages)
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf8").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User", "Claude-SearchBot", "anthropic-ai", "PerplexityBot", "Perplexity-User",
            "Google-Extended", "Applebot-Extended", "Bingbot", "CCBot", "cohere-ai", "meta-externalagent", "Amazonbot", "DuckAssistBot"]
    robots = "User-agent: *\nAllow: /\n\n# Buscadores e assistentes de IA: liberados de propósito (queremos ser citados)\n"
    robots += "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"Sitemap: {SITE_URL}/sitemap.xml\n"
    open(os.path.join(OUT, "robots.txt"), "w", encoding="utf8").write(robots)
    # llms.txt (resumo estruturado para IAs)
    L = [f"# {NAME}", "",
         "> Lash designer em Cosmos, Rio de Janeiro (RJ). Faz extensão de cílios fio a fio, volume egípcio, volume brasileiro, mega volume egípcio e volume Fox Eyes, além de manutenção e remoção, sempre a domicílio (a profissional vai até a casa da cliente), com hora marcada.", "",
         "## Fatos do negócio",
         "- Profissional: Lavínia Monteiro, lash designer desde 2024",
         "- Atendimento: somente a domicílio, em Cosmos, Campo Grande (RJ), Paciência, Senador Vasconcelos, Inhoaíba e Santa Cruz, no Rio de Janeiro",
         "- Não é Campo Grande (MS): o atendimento é em Campo Grande, Rio de Janeiro (RJ)",
         f"- WhatsApp: {PHONE_DISPLAY} ({PHONE_E164}); agendamento, valores e horários são combinados por lá",
         f"- Instagram: {INSTAGRAM}", f"- Google Maps: {MAPS}", "- Idioma: português do Brasil", "",
         "## Serviços"]
    for sv in SERVICES + EXTRA_SERVICES:
        L.append(f"- [{sv['name']}]({SITE_URL}/servicos/{sv['slug']}/): {sv['lead']}")
    L += ["", "## Onde atendo", f"- [Hub de atendimento]({SITE_URL}/atendimento/)", f"- [Cílios em Cosmos]({SITE_URL}/atendimento/cosmos/)", f"- [Cílios em Campo Grande RJ]({SITE_URL}/atendimento/campo-grande/)", "", "## Guias (blog)"]
    for a in ARTICLES:
        L.append(f"- [{a['h1']}]({SITE_URL}/blog/{a['slug']}/): {a['tldr']}")
    L += ["", "## Outras páginas", f"- [Quem sou]({SITE_URL}/quem-sou/)", f"- [Clientes e resultados]({SITE_URL}/clientes/)", f"- [Contato]({SITE_URL}/contato/)", ""]
    open(os.path.join(OUT, "llms.txt"), "w", encoding="utf8").write("\n".join(L))
    # favicon
    lashes = "".join(f'<path d="{d}"/>' for d in _lashes)
    fav = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="120 130 480 480"><rect x="120" y="130" width="480" height="480" rx="110" fill="#F8E9E4"/>'
           f'<g fill="none" stroke="#5A2A3C" stroke-linecap="round" transform="translate(0,-12)"><path d="{_arc}" stroke-width="22"/><g stroke-width="17">{lashes}</g></g></svg>')
    open(os.path.join(IMG, "favicon.svg"), "w", encoding="utf8").write(fav)
    logo = Image.open(os.path.join(IMG, "logo-lavinia.png")).convert("RGB")
    logo.resize((180, 180), Image.LANCZOS).save(os.path.join(IMG, "apple-touch-icon.png"))
    # og
    capa = Image.open(os.path.join(ROOT, "logo", "capa-gmn-lavinia.png")).convert("RGB")
    og = capa.resize((1200, 675), Image.LANCZOS).crop((0, 22, 1200, 652))
    og.save(os.path.join(IMG, "og-lavinia.jpg"), quality=88)

if __name__ == "__main__":
    for f in ("index.html", "404.html"):
        p = os.path.join(OUT, f)
        if os.path.exists(p): os.remove(p)
    for d in ("servicos", "atendimento", "blog", "clientes", "quem-sou", "contato"):
        shutil.rmtree(os.path.join(OUT, d), ignore_errors=True)
    from layout import _lashes, _arc
    home(); about(); services_pages(); areas(); clients(); blog(); contact(); legal(); extras()
    print(f"OK: {len(pages)} páginas | SITE_URL={SITE_URL}")
