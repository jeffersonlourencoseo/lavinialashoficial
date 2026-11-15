/* Google Analytics 4 com Consent Mode v2 + banner de cookies (LGPD).
   - Começa com analytics_storage NEGADO: sem consentimento não grava cookie.
   - Eventos: visita (page_view), WhatsApp, Instagram, Maps, telefone, abertura de foto, FAQ, rolagem. */
(function () {
  'use strict';
  var GA_ID = 'G-76EZQX5XWH', KEY = 'lm_consent', d = document, w = window;
  w.dataLayer = w.dataLayer || [];
  function gtag() { w.dataLayer.push(arguments); }
  w.gtag = gtag;

  function store(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  function stored() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function setConsent(granted) {
    gtag('consent', 'update', { analytics_storage: granted ? 'granted' : 'denied' });
  }

  // consentimento padrão: negado
  gtag('consent', 'default', { ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', analytics_storage: 'denied', wait_for_update: 500 });
  if (stored() === 'granted') setConsent(true);

  gtag('js', new Date());
  gtag('config', GA_ID, { transport_type: 'beacon' });

  // carrega o gtag.js sem atrapalhar o carregamento da página
  var LOCAL = /^(localhost|127\.|0\.0\.0\.0)/.test(location.hostname); // testes locais não enviam dados
  function loadGtag() {
    if (LOCAL) return;
    var s = d.createElement('script');
    s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    d.head.appendChild(s);
  }
  if (d.readyState === 'complete') { setTimeout(loadGtag, 800); }
  else { w.addEventListener('load', function () { ('requestIdleCallback' in w) ? requestIdleCallback(loadGtag, { timeout: 2500 }) : setTimeout(loadGtag, 1200); }); }

  // ----- banner de cookies -----
  var banner;
  function closeBanner() { if (banner) { banner.remove(); banner = null; } d.body.classList.remove('cookie-open'); }
  function openBanner() {
    if (banner) return;
    banner = d.createElement('div');
    banner.className = 'cookiebar'; banner.setAttribute('role', 'region'); banner.setAttribute('aria-label', 'Aviso de cookies');
    banner.innerHTML = '<p>Usamos cookies de estatística (Google Analytics) para entender como o site é usado e melhorá-lo. A escolha é sua. Veja a <a href="/politica-de-cookies/">Política de Cookies</a>.</p>' +
      '<div class="cb-btns"><button type="button" class="btn sm ghost" data-c="deny">Recusar</button><button type="button" class="btn sm" data-c="allow">Aceitar</button></div>';
    d.body.appendChild(banner); d.body.classList.add('cookie-open');
    banner.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-c]'); if (!b) return;
      var ok = b.getAttribute('data-c') === 'allow';
      store(ok ? 'granted' : 'denied'); setConsent(ok); closeBanner();
      if (ok) gtag('event', 'cookie_consent', { choice: 'accepted' });
    });
  }
  if (!stored()) { w.addEventListener('load', function () { setTimeout(openBanner, 900); }); }
  d.addEventListener('click', function (e) { if (e.target.closest('[data-cookie-settings]')) { e.preventDefault(); openBanner(); } });

  // ----- eventos -----
  function page() { return location.pathname; }
  d.addEventListener('click', function (e) {
    var a = e.target.closest('a[href]');
    if (a) {
      var h = a.getAttribute('href') || '';
      var where = a.getAttribute('data-where') || (a.closest('.header') ? 'cabecalho' : a.closest('.footer') ? 'rodape' : a.classList.contains('wafab') ? 'botao-flutuante' : 'pagina');
      if (h.indexOf('wa.me') > -1 || h.indexOf('whatsapp.com') > -1) {
        gtag('event', 'whatsapp_click', { link_location: where, page_path: page(), link_text: (a.textContent || '').trim().slice(0, 40) });
        gtag('event', 'generate_lead', { method: 'whatsapp', link_location: where, page_path: page() });
      } else if (h.indexOf('instagram.com') > -1) {
        gtag('event', 'instagram_click', { link_location: where, page_path: page() });
      } else if (h.indexOf('google.com/maps') > -1) {
        gtag('event', 'maps_click', { link_location: where, page_path: page() });
      } else if (h.indexOf('tel:') === 0) {
        gtag('event', 'phone_click', { link_location: where, page_path: page() });
      }
    }
    var shot = e.target.closest('[data-lb]');
    if (shot) gtag('event', 'gallery_open', { image: (shot.getAttribute('data-lb') || '').split('/').pop(), page_path: page() });
  }, true);

  d.addEventListener('toggle', function (e) {
    var t = e.target;
    if (t && t.tagName === 'DETAILS' && t.open) {
      var s = t.querySelector('summary');
      gtag('event', 'faq_open', { question: s ? s.textContent.trim().slice(0, 80) : '', page_path: page() });
    }
  }, true);

  // rolagem: 25 / 50 / 75 / 100 %
  var marks = { 25: 0, 50: 0, 75: 0, 100: 0 };
  function onScroll() {
    var h = d.documentElement.scrollHeight - w.innerHeight; if (h <= 0) return;
    var p = Math.round((w.scrollY / h) * 100);
    [25, 50, 75, 100].forEach(function (m) {
      if (!marks[m] && p >= m - (m === 100 ? 2 : 0)) { marks[m] = 1; gtag('event', 'scroll_depth', { percent: m, page_path: page() }); }
    });
  }
  w.addEventListener('scroll', onScroll, { passive: true });
})();
