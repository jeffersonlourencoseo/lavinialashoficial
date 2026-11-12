# Site da Lavinia Monteiro | Lash Designer

Site estático (HTML/CSS/JS puro, sem dependências), 24 páginas, otimizado para Google e para buscadores/assistentes de IA.
Atendimento a domicílio em Cosmos, Campo Grande (RJ), Paciência, Senador Vasconcelos, Inhoaíba e Santa Cruz.

## Publicar na Vercel
1. Importar este repositório na Vercel (framework: **Other**). O `vercel.json` já define tudo:
   saída em `site/`, build `node scripts/set-domain.mjs`, cabeçalhos de cache e segurança.
2. O domínio é injetado no deploy (canonical, sitemap, Open Graph, schema, llms.txt):
   - Sem configurar nada: usa o domínio de produção da Vercel (`*.vercel.app`).
   - Domínio próprio: em *Settings > Environment Variables* crie `SITE_URL` = `https://www.seudominio.com.br` e faça redeploy.
3. Depois de publicar: colocar a URL no campo "Site" do Perfil da Empresa no Google, enviar `/sitemap.xml` no Search Console e no Bing Webmaster.

## Ranqueamento (Google + IAs)
- Title/description únicos, canonical, hreflang, Open Graph, 1 H1 por página, breadcrumbs.
- Schema.org em JSON-LD: BeautySalon/LocalBusiness (areaServed, founder, foundingDate), Person, Service (7), FAQPage, BlogPosting, BreadcrumbList, ProfilePage, WebSite.
- Páginas locais: Cosmos e Campo Grande RJ (com desambiguação de Campo Grande/MS).
- Para IAs: `robots.txt` libera GPTBot, ClaudeBot, PerplexityBot, Google-Extended etc.; `llms.txt` com resumo estruturado; respostas diretas ("Resposta rápida") no topo dos artigos; FAQ em formato pergunta/resposta.
- Performance: fontes locais (sem Google Fonts), imagens WebP com srcset, JS mínimo.
- Depoimentos: a seção só aparece quando houver depoimentos REAIS em `build/content.py` (`TESTIMONIALS`). Não inventar avaliações (viola as regras do Google e o CDC).

## Editar e ver local
```bash
python build/process_photos.py   # converte as fotos de "Nova pasta" (nomeadas por serviço) em WebP
python build/build.py          # regenera site/ (requer Python + Pillow)
python -m http.server 8080 --directory site
```
No Windows: `iniciar-site.bat`. Textos em `build/content.py` e `build/blog.py`; estilo em `site/assets/css/style.css`.

## Pendências com a Lavinia
- Confirmar o texto da página "Quem sou" (história desde 2024).
- Valores, dias/horários e eventual taxa de deslocamento: seguem por WhatsApp (não estão no site de propósito).
- Quando o GMN tiver avaliações reais, preencher `TESTIMONIALS`.
