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
    label.textContent = open ? label.dataset.close : label.dataset.open;
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
  var imgs = menu.querySelectorAll('.nxm-menu__media img');
  function show(n) {
    imgs.forEach(function (img) { img.classList.toggle('is-active', img.dataset.nxmImg === n); });
  }
  menu.querySelectorAll('.nxm-menu__nav a').forEach(function (a) {
    a.addEventListener('mouseenter', function () { show(a.dataset.nxmImg); });
    a.addEventListener('focus', function () { show(a.dataset.nxmImg); });
  });
  var cur = menu.querySelector('.nxm-menu__nav a[aria-current]');
  if (cur) show(cur.dataset.nxmImg);

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
