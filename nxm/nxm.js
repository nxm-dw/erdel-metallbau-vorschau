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

/* Datenschutz-Einwilligung: ohne Haken kein Absenden (läuft vor allen anderen Absende-Handlern) */
window.addEventListener('submit', function (e) {
  var f = e.target;
  if (!f || f.tagName !== 'FORM') return;
  var box = f.querySelector('[data-nxm-consent]');
  if (!box) return;
  var err = box.closest('.forminator-field').querySelector('.nxm-consent__error');
  if (box.checked) { if (err) err.hidden = true; box.removeAttribute('aria-invalid'); return; }
  e.preventDefault(); e.stopImmediatePropagation();
  box.setAttribute('aria-invalid', 'true');
  if (err) err.hidden = false;
  box.closest('.forminator-field').scrollIntoView({ behavior: 'smooth', block: 'center' });
  box.focus({ preventScroll: true });
}, true);
document.addEventListener('change', function (e) {
  if (!e.target.matches || !e.target.matches('[data-nxm-consent]') || !e.target.checked) return;
  var err = e.target.closest('.forminator-field').querySelector('.nxm-consent__error');
  if (err) err.hidden = true; e.target.removeAttribute('aria-invalid');
});

/* Konfigurator-Anfrage: drei kurze Schritte, Prüfung je Schritt, Seitenleiste zeigt den Stand (Vorschau: kein Versand) */
(function () {
  document.querySelectorAll('form[data-nxm-wizard]').forEach(function (f) {
    var steps = [].slice.call(f.querySelectorAll('.x-wiz__step')), cur = 0;
    var bar = f.querySelector('.x-wiz__progress span'), count = f.querySelector('[data-wiz-count]');
    var side = f.closest('.x-formgrid') ? f.closest('.x-formgrid').querySelector('.x-formside') : null;
    var sideSteps = side ? [].slice.call(side.querySelectorAll('.x-steps li')) : [];
    if (side) side.classList.add('x-wiz-side');

    function show(i, scroll) {
      cur = i;
      steps.forEach(function (s, k) { s.hidden = k !== i; });
      if (bar) bar.style.width = ((i + 1) / steps.length * 100) + '%';
      if (count) count.textContent = 'Schritt ' + (i + 1) + ' von ' + steps.length;
      sideSteps.forEach(function (li, k) { li.classList.toggle('is-current', k === i); li.classList.toggle('is-done', k < i); });
      if (i === steps.length - 1) summary();
      if (scroll) {
        var top = f.getBoundingClientRect().top + window.scrollY - 120;
        if (top < window.scrollY) window.scrollTo({ top: top, behavior: 'smooth' });
      }
    }
    function valid(i) {
      var s = steps[i], ok = true, names = {};
      [].forEach.call(s.querySelectorAll('input[type=radio][required]'), function (r) { names[r.name] = true; });
      Object.keys(names).forEach(function (n) {
        var g = s.querySelector('[data-group="' + n + '"]'), bad = !f.querySelector('input[name="' + n + '"]:checked');
        if (g) g.classList.toggle('is-invalid', bad);
        if (bad) ok = false;
      });
      [].forEach.call(s.querySelectorAll('.x-field input[required], .x-field textarea[required]'), function (el) {
        var bad = !el.checkValidity();
        el.closest('.x-field').classList.toggle('is-invalid', bad);
        if (bad) ok = false;
      });
      var err = s.querySelector('.x-wiz__error');
      if (err) err.hidden = ok;
      if (!ok) {
        var first = s.querySelector('.is-invalid input, .x-field.is-invalid input');
        if (first) first.focus({ preventScroll: true });
        var bad = s.querySelector('.is-invalid');
        if (bad) bad.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
      return ok;
    }
    function summary() {
      var el = f.querySelector('[data-wiz-summary]');
      if (!el) return;
      var parts = [];
      ['produkt', 'situation'].forEach(function (n) { var r = f.querySelector('input[name="' + n + '"]:checked'); if (r) parts.push(r.value); });
      el.textContent = parts.length ? 'Ihre Auswahl: ' + parts.join(' · ') : '';
      el.hidden = !parts.length;
    }
    f.addEventListener('click', function (e) {
      if (e.target.closest('[data-wiz-next]')) { if (valid(cur)) show(cur + 1, true); }
      else if (e.target.closest('[data-wiz-prev]')) show(cur - 1, true);
    });
    f.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && e.target.tagName === 'INPUT' && e.target.type !== 'checkbox' && cur < steps.length - 1) {
        e.preventDefault(); if (valid(cur)) show(cur + 1, true);
      }
    });
    f.addEventListener('change', function (e) {
      var el = e.target, wrap = el.closest('.is-invalid');
      if (wrap && (el.type === 'radio' || el.checkValidity())) wrap.classList.remove('is-invalid');
      var err = steps[cur].querySelector('.x-wiz__error');
      if (err && !steps[cur].querySelector('.is-invalid')) err.hidden = true;
      if (el.type === 'file') {
        var up = el.closest('.x-upload'), list = up.querySelector('[data-upload-list]');
        list.textContent = [].map.call(el.files, function (x) { return x.name; }).join(', ');
        up.classList.toggle('has-files', el.files.length > 0);
      }
    });
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!valid(cur)) return;
      steps.forEach(function (s) { s.hidden = true; });
      var done = f.querySelector('.x-wiz__done');
      if (done) { done.hidden = false; done.focus(); }
      if (bar) bar.style.width = '100%';
      if (count) count.textContent = 'Gesendet';
      sideSteps.forEach(function (li) { li.classList.add('is-done'); li.classList.remove('is-current'); });
    });
    show(0, false);
  });
})();

/* Bewerbung: „Jetzt bewerben“ an einer Stelle trägt die Stelle ins Formular ein (auch per ?stelle= in der Adresse) */
(function () {
  var form = document.querySelector('#bewerbung form');
  if (!form) return;
  var head = form.closest('.x-formcard') ? form.closest('.x-formcard').querySelector('.x-formcard__head') : null;
  var ta = form.querySelector('textarea');
  function setStelle(name) {
    if (!name) return;
    if (head) {
      var tag = head.querySelector('.x-formcard__stelle');
      if (!tag) { tag = document.createElement('p'); tag.className = 'x-formcard__stelle'; head.insertBefore(tag, head.firstChild); }
      tag.textContent = 'Bewerbung als ' + name;
    }
    if (ta) {
      var rest = ta.value.replace(/^Bewerbung als: [^\n]*\n?/, '');
      ta.value = ('Bewerbung als: ' + name + '\n' + rest).slice(0, ta.maxLength > 0 ? ta.maxLength : 9999);
      ta.dispatchEvent(new Event('input', { bubbles: true }));
    }
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[data-stelle]') : null;
    if (a) setStelle(a.getAttribute('data-stelle'));
  }, true);
  var q = new URLSearchParams(location.search).get('stelle');
  if (q) setStelle(q);
})();
