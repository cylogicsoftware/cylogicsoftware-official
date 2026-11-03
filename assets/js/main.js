/* CYLOGIC SOFTWARE – Digital Identity Hub (no dependencies) */
(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.add('js');

  // Language switcher
  var lang = document.querySelector('.lang');
  var langBtn = lang && lang.querySelector('.lang-btn');
  function closeLang() {
    if (!lang) return;
    lang.classList.remove('open');
    langBtn.setAttribute('aria-expanded', 'false');
  }
  if (langBtn) {
    langBtn.addEventListener('click', function (ev) {
      ev.stopPropagation();
      var open = lang.classList.toggle('open');
      langBtn.setAttribute('aria-expanded', String(open));
      if (open) {
        var first = lang.querySelector('.lang-menu a');
        if (first) first.focus();
      }
    });
    lang.addEventListener('keydown', function (ev) {
      var items = Array.prototype.slice.call(lang.querySelectorAll('.lang-menu a'));
      var i = items.indexOf(document.activeElement);
      if (ev.key === 'Escape') { closeLang(); langBtn.focus(); }
      else if (ev.key === 'ArrowDown' && i > -1) { ev.preventDefault(); items[(i + 1) % items.length].focus(); }
      else if (ev.key === 'ArrowUp' && i > -1) { ev.preventDefault(); items[(i - 1 + items.length) % items.length].focus(); }
    });
    lang.querySelectorAll('.lang-menu a').forEach(function (a) {
      a.addEventListener('click', function () {
        try { localStorage.setItem('cylogic-lang', a.getAttribute('lang')); } catch (e) { /* storage unavailable */ }
      });
    });
    document.addEventListener('click', function (ev) { if (!lang.contains(ev.target)) closeLang(); });
  }

  // Mobile menu
  var menuBtn = document.querySelector('.menu-btn');
  var links = document.getElementById('nav-links');
  if (menuBtn && links) {
    menuBtn.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', String(open));
    });
    links.addEventListener('click', function (ev) {
      if (ev.target.tagName === 'A') {
        links.classList.remove('open');
        menuBtn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // Reveal on scroll
  var els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add('in'); });
  }
})();
