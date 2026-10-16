/* Altes Theme-Skript ruft Bootstrap-Offcanvas der früheren Navigation auf */
if (window.jQuery && !jQuery.fn.offcanvas) { jQuery.fn.offcanvas = function () { return this; }; }

/* erdel metallbau – Menü und Kopfzeile */
(function () {
  var body = document.body;
  var head = document.getElementById('nxm-head');
  var menu = document.getElementById('nxm-menu');
  var btn = head && head.querySelector('.nxm-burger');
  if (!head || !menu || !btn) return;
  var label = btn.querySelector('.nxm-burger__label');
  var lastFocus = null;

  function setOpen(open) {
    menu.classList.toggle('is-open', open);
    body.classList.toggle('nxm-menu-open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    menu.setAttribute('aria-hidden', open ? 'false' : 'true');
    btn.setAttribute('aria-label', open ? 'Menü schließen' : 'Menü öffnen');
    if (label) label.textContent = open ? label.dataset.close : label.dataset.open;
    if (open) {
      lastFocus = document.activeElement;
      var first = menu.querySelector('.nxm-menu__nav a');
      setTimeout(function () { first && first.focus({ preventScroll: true }); }, 350);
    } else if (lastFocus) {
      lastFocus.focus({ preventScroll: true });
    }
  }

  btn.addEventListener('click', function () { setOpen(!menu.classList.contains('is-open')); });
  document.addEventListener('keydown', function (e) {
    if (!menu.classList.contains('is-open')) return;
    if (e.key === 'Escape') { setOpen(false); return; }
    if (e.key === 'Tab') {
      // Fokus im Menü (inkl. Schließen-Knopf) halten
      var items = [btn].concat([].slice.call(menu.querySelectorAll('a')));
      var i = items.indexOf(document.activeElement);
      if (e.shiftKey && i <= 0) { e.preventDefault(); items[items.length - 1].focus(); }
      else if (!e.shiftKey && i === items.length - 1) { e.preventDefault(); items[0].focus(); }
    }
  });
  menu.addEventListener('click', function (e) {
    var a = e.target.closest('a');
    if (a && !a.target) setOpen(false);
  });

  // Bildvorschau im Menü
  var imgs = menu.querySelectorAll('.nxm-menu__bg img');
  function show(n) {
    imgs.forEach(function (img) { img.classList.toggle('is-active', img.dataset.nxmImg === n); });
  }
  menu.querySelectorAll('.nxm-menu__nav a').forEach(function (a) {
    a.addEventListener('mouseenter', function () { show(a.dataset.nxmImg); });
    a.addEventListener('focus', function () { show(a.dataset.nxmImg); });
  });
  var cur = menu.querySelector('.nxm-menu__nav a[aria-current]');
  var home = cur ? cur.dataset.nxmImg : '0';
  show(home);
  // Verlässt die Maus die Liste, kehrt das Bild der aktuellen Seite zurück
  var list = menu.querySelector('.nxm-menu__nav ul');
  if (list) list.addEventListener('mouseleave', function () { show(home); });

  // Kopfzeile: beim Runterscrollen ausblenden, beim Hochscrollen zeigen
  var lastY = window.scrollY, ticking = false;
  function onScroll() {
    var y = window.scrollY;
    head.classList.toggle('is-scrolled', y > 10);
    if (!body.classList.contains('nxm-menu-open')) {
      head.classList.toggle('is-hidden', y > 320 && y > lastY + 4);
      if (y < lastY - 4) head.classList.remove('is-hidden');
    }
    lastY = y; ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  onScroll();
})();

/* Öffnungszeiten: Live-Status nach deutscher Zeit */
(function () {
  var box = document.querySelector('[data-nxm-open]');
  if (!box) return;
  var parts = {};
  try {
    new Intl.DateTimeFormat('de-DE', { timeZone: 'Europe/Berlin', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false })
      .formatToParts(new Date()).forEach(function (p) { parts[p.type] = p.value; });
  } catch (e) { return; }
  var day = ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa'].indexOf(parts.weekday.replace('.', ''));
  var min = parseInt(parts.hour, 10) * 60 + parseInt(parts.minute, 10);
  var open = (day >= 1 && day <= 4 && min >= 480 && min < 990) || (day === 5 && min >= 480 && min < 780);
  box.classList.add(open ? 'is-open' : 'is-closed');
  box.querySelector('.x-status__text').textContent = open ? 'Jetzt geöffnet' : 'Gerade geschlossen';
  box.querySelectorAll('[data-days]').forEach(function (row) {
    if (row.dataset.days.split(',').indexOf(String(day)) > -1) row.classList.add('is-today');
  });
})();

/* Hero-Claim: Schrift verkleinern, bis er in seine Spalte passt (nichts wird angeschnitten) */
(function () {
  var h = document.querySelector('header.featured-full-width-img h1');
  if (!h) return;
  function fit() {
    h.style.fontSize = '';
    var box = h.parentElement.getBoundingClientRect();
    var size = parseFloat(getComputedStyle(h).fontSize);
    var guard = 0;
    while (guard++ < 40 && size > 22) {
      var r = document.createRange(); r.selectNodeContents(h);
      var right = Math.max.apply(null, [].map.call(r.getClientRects(), function (x) { return x.right; }));
      var limit = Math.min(box.right, document.documentElement.clientWidth) - 16;
      if (right <= limit && h.scrollWidth <= h.clientWidth + 1) break;
      size -= 2; h.style.fontSize = size + 'px';
    }
  }
  fit();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
  var t; window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(fit, 120); });
})();

/* Überschriften im Inhalt: Schrift minimal verkleinern, falls ein gebundenes Wortpaar sonst überläuft */
(function () {
  var sel = 'main h1, main h2, main h3, .x-display, .x-h2, .nxm-teaser__title, .x-job__title, .x-partner__name';
  function fitAll() {
    document.querySelectorAll(sel).forEach(function (h) {
      if (h.closest('header.featured-full-width-img')) return;
      h.style.fontSize = '';
      var size = parseFloat(getComputedStyle(h).fontSize), min = size * 0.7, guard = 0;
      while (guard++ < 30 && size > min && h.scrollWidth > h.clientWidth + 1) {
        size -= 1; h.style.fontSize = size + 'px';
      }
    });
  }
  fitAll();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitAll);
  var t; window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(fitAll, 150); });
})();

/* Kontaktkacheln: eine gemeinsame Schriftgröße, bei der jeder Wert einzeilig in seine Kachel passt */
(function () {
  var vals = document.querySelectorAll('.x-tile__value');
  if (!vals.length) return;
  var root = vals[0].closest('.x-tiles');
  function fit() {
    var size = 26;
    root.style.setProperty('--x-tile-fs', size + 'px');
    var fits = function () { return [].every.call(vals, function (v) { return v.scrollWidth <= v.clientWidth + 1; }); };
    while (size > 15 && !fits()) { size -= 0.5; root.style.setProperty('--x-tile-fs', size + 'px'); }
  }
  fit();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
  var t; window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(fit, 150); });
})();

/* Kontaktformular: Themen-Chips setzen eine kurze Themenzeile ins Nachrichtenfeld */
(function () {
  var ta = document.querySelector('.x-formcard textarea');
  if (!ta) return;
  var topics = ['Tor', 'Zaun', 'Geländer', 'Treppe', 'Briefkasten', 'Vordach', 'Möbel', 'Sonstiges'];
  var box = document.createElement('div');
  box.className = 'x-chips';
  box.setAttribute('role', 'group');
  box.setAttribute('aria-label', 'Thema wählen');
  box.innerHTML = '<p class="x-chips__label">Worum geht es? (optional)</p>' + topics.map(function (t) {
    return '<button type="button" class="x-chip" aria-pressed="false">' + t + '</button>';
  }).join('');
  ta.parentNode.insertBefore(box, ta);
  var prefix = /^Thema: [^\n]*\n?/;
  box.addEventListener('click', function (e) {
    var b = e.target.closest('.x-chip');
    if (!b) return;
    var on = b.getAttribute('aria-pressed') !== 'true';
    box.querySelectorAll('.x-chip').forEach(function (c) { c.setAttribute('aria-pressed', 'false'); });
    var rest = ta.value.replace(prefix, '');
    if (on) { b.setAttribute('aria-pressed', 'true'); ta.value = ('Thema: ' + b.textContent + '\n' + rest).slice(0, ta.maxLength > 0 ? ta.maxLength : 9999); }
    else { ta.value = rest; }
    ta.dispatchEvent(new Event('input', { bubbles: true }));
    ta.dispatchEvent(new Event('keyup', { bubbles: true }));
  });
})();

/* Scroll-Animationen: Elemente blenden beim Hereinscrollen weich ein; Zeitleiste füllt sich */
(function () {
  if (!('IntersectionObserver' in window)) return;
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.documentElement.classList.add('nxm-js');
  var groups = [
    ['.x-intro .x-wrap > *', 0.08], ['.x-tile', 0.07], ['.x-formgrid > *', 0.1], ['.x-partner', 0.1],
    ['.x-job', 0.08], ['.x-benefits li', 0.1], ['.x-check li', 0.05], ['.x-cta__inner > *', 0.12],
    ['.x-tl__item', 0], ['.x-h2', 0], ['.x-section > .x-wrap > .x-eyebrow', 0],
    ['.malu-1 .row', 0], ['.two-col-section .row > *', 0.12], ['.hero-text', 0], ['.gallery-item', 0.04],
    ['.simple_content .content-width-50', 0], ['.member', 0.08]
  ];
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
  groups.forEach(function (g) {
    var list = document.querySelectorAll(g[0]);
    [].forEach.call(list, function (el, i) {
      if (el.closest('.nxm-menu') || el.classList.contains('nxm-reveal')) return;
      el.classList.add('nxm-reveal');
      if (g[1]) el.style.setProperty('--d', Math.min(i % 4, 3) * g[1] + 's');
      // schon sichtbare Elemente sofort zeigen (kein Aufblitzen beim Laden)
      var r = el.getBoundingClientRect();
      if (r.top < innerHeight * 0.92 && r.bottom > 0) el.classList.add('is-in'); else io.observe(el);
    });
  });
  // Zeitleiste: Linie füllt sich mit dem Scrollen
  var tl = document.querySelector('.x-tl');
  if (tl) {
    var tick = false;
    var upd = function () {
      var r = tl.getBoundingClientRect(), mid = innerHeight * 0.6;
      var p = Math.max(0, Math.min(1, (mid - r.top) / r.height));
      tl.style.setProperty('--x-progress', p.toFixed(3)); tick = false;
    };
    window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(upd); } }, { passive: true });
    upd();
  }
})();
