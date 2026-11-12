(function () {
  'use strict';
  var d = document, root = d.documentElement;
  root.classList.add('js');

  // header com sombra ao rolar
  var header = d.querySelector('.header');
  function onScroll() { if (header) header.classList.toggle('scrolled', window.scrollY > 8); }
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

  // menu mobile
  var burger = d.querySelector('.burger'), nav = d.querySelector('.nav');
  if (burger && nav) {
    function setMenu(open) {
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
      nav.classList.toggle('open', open);
      d.body.style.overflow = open ? 'hidden' : '';
    }
    burger.addEventListener('click', function () { setMenu(burger.getAttribute('aria-expanded') !== 'true'); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
    window.matchMedia('(min-width:981px)').addEventListener('change', function () { setMenu(false); });
  }

  // revelar ao rolar
  var items = d.querySelectorAll('.rv');
  if ('IntersectionObserver' in window && items.length) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  } else { items.forEach(function (el) { el.classList.add('in'); }); }

  // lightbox da galeria
  var shots = [].slice.call(d.querySelectorAll('[data-lb]'));
  if (shots.length) {
    var lb = d.createElement('div');
    lb.className = 'lb'; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true'); lb.setAttribute('aria-label', 'Foto ampliada');
    lb.innerHTML = '<button class="x" aria-label="Fechar">×</button><button class="pv" aria-label="Foto anterior">‹</button><img alt=""><button class="nx" aria-label="Próxima foto">›</button>';
    d.body.appendChild(lb);
    var img = lb.querySelector('img'), cur = 0, last = null;
    function show(i) {
      cur = (i + shots.length) % shots.length;
      img.src = shots[cur].getAttribute('data-lb');
      img.alt = shots[cur].getAttribute('data-alt') || '';
    }
    function open(i) { last = d.activeElement; show(i); lb.classList.add('open'); d.body.style.overflow = 'hidden'; lb.querySelector('.x').focus(); }
    function close() { lb.classList.remove('open'); d.body.style.overflow = ''; if (last) last.focus(); }
    shots.forEach(function (b, i) { b.addEventListener('click', function () { open(i); }); });
    lb.querySelector('.x').addEventListener('click', close);
    lb.querySelector('.pv').addEventListener('click', function () { show(cur - 1); });
    lb.querySelector('.nx').addEventListener('click', function () { show(cur + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    d.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(cur - 1);
      if (e.key === 'ArrowRight') show(cur + 1);
    });
  }
})();
