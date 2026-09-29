/* ============================================================
   MAIN - CC Coaching & Consulting

   Vanilla, no dependencies, no third-party requests.
   Four jobs: sticky header state, mobile navigation,
   scroll reveal, and the active nav link.
   ============================================================ */

(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- Sticky header ---------------------------------- */

  var header = document.querySelector('[data-header]');

  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-scrolled', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }


  /* ---- Mobile navigation ------------------------------ */

  var nav = document.querySelector('[data-nav]');
  var openBtn = document.querySelector('[data-nav-open]');
  var closeBtn = document.querySelector('[data-nav-close]');

  function setNav(open) {
    if (!nav) return;
    nav.classList.toggle('is-open', open);
    if (openBtn) openBtn.setAttribute('aria-expanded', String(open));
    document.body.style.overflow = open ? 'hidden' : '';
    if (open && closeBtn) closeBtn.focus();
    else if (!open && openBtn) openBtn.focus();
  }

  if (openBtn) openBtn.addEventListener('click', function () { setNav(true); });
  if (closeBtn) closeBtn.addEventListener('click', function () { setNav(false); });

  /* Any link inside the overlay closes it. */
  if (nav) {
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setNav(false);
    });
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav && nav.classList.contains('is-open')) {
      setNav(false);
    }
  });


  /* ---- Scroll reveal ----------------------------------
     One primitive: fade + rise, staggered within a group.
     Under reduced motion everything is shown at once. */

  var revealables = document.querySelectorAll('[data-reveal]');

  if (reduceMotion || !('IntersectionObserver' in window)) {
    revealables.forEach(function (el) { el.classList.add('is-visible'); });
  } else {
    var stagger = parseInt(
      getComputedStyle(document.documentElement)
        .getPropertyValue('--reveal-stagger'), 10
    ) || 60;

    var observer = new IntersectionObserver(function (entries) {
      var shown = 0;
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var delay = shown * stagger;
        shown++;
        setTimeout(function () {
          entry.target.classList.add('is-visible');
        }, delay);
        observer.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });

    revealables.forEach(function (el) { observer.observe(el); });
  }



  /* ---- Smooth scrolling ------------------------------------
     CSS already sets scroll-behavior: smooth, which is the fallback when
     JavaScript is unavailable. When it is available we take over, so that
     in-page navigation uses the same easing curve as every other transition
     on the site (--ease) rather than the browser's generic one.

     Native smooth scrolling is switched off from here, not from the
     stylesheet: if this file fails to load, the CSS fallback still works. */

  function cubicBezier(p1x, p1y, p2x, p2y) {
    function A(a1, a2) { return 1 - 3 * a2 + 3 * a1; }
    function B(a1, a2) { return 3 * a2 - 6 * a1; }
    function C(a1) { return 3 * a1; }
    function calc(t, a1, a2) { return ((A(a1, a2) * t + B(a1, a2)) * t + C(a1)) * t; }
    function slope(t, a1, a2) { return 3 * A(a1, a2) * t * t + 2 * B(a1, a2) * t + C(a1); }
    return function (x) {
      if (x <= 0) return 0;
      if (x >= 1) return 1;
      var t = x;
      for (var i = 0; i < 6; i++) {
        var s = slope(t, p1x, p2x);
        if (s === 0) break;
        t -= (calc(t, p1x, p2x) - x) / s;
      }
      return calc(t, p1y, p2y);
    };
  }

  /* Same control points as --ease in tokens.css. */
  var easeScroll = cubicBezier(0.22, 1, 0.36, 1);
  var root = document.documentElement;

  function targetOffset(el) {
    /* scroll-padding-top carries the sticky-header offset, so reading it
       keeps this in step with --header-h instead of duplicating the value. */
    var pad = parseFloat(getComputedStyle(root).scrollPaddingTop) || 0;
    var max = document.body.scrollHeight - window.innerHeight;
    var y = el.getBoundingClientRect().top + window.scrollY - pad;
    return Math.max(0, Math.min(y, max));
  }

  function scrollToElement(el, done) {
    var start = window.scrollY;
    var end = targetOffset(el);
    var dist = end - start;

    if (reduceMotion || Math.abs(dist) < 2) {
      window.scrollTo(0, end);
      done();
      return;
    }

    /* Longer journeys take a little longer, but never enough to feel slow. */
    var dur = Math.min(1100, Math.max(420, Math.abs(dist) * 0.45));
    var t0 = performance.now();
    var finished = false;

    /* Browsers throttle or pause rAF in background tabs. Without this guard
       a paused animation would strand the reader mid-page with the hash and
       focus never updated, so the scroll always completes one way or another. */
    var guard = setTimeout(complete, dur + 300);

    function complete() {
      if (finished) return;
      finished = true;
      clearTimeout(guard);
      window.scrollTo(0, end);
      done();
    }

    requestAnimationFrame(function frame(now) {
      if (finished) return;
      var p = Math.min(1, (now - t0) / dur);
      window.scrollTo(0, start + dist * easeScroll(p));
      if (p < 1) requestAnimationFrame(frame);
      else complete();
    });
  }

  if ('requestAnimationFrame' in window) {
    root.style.scrollBehavior = 'auto';

    document.addEventListener('click', function (e) {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey ||
          e.shiftKey || e.altKey) return;

      var link = e.target.closest('a[href]');
      if (!link) return;

      var href = link.getAttribute('href');
      if (!href || href.charAt(0) !== '#' || href === '#') return;

      var el = document.getElementById(href.slice(1));
      if (!el) return;

      e.preventDefault();
      scrollToElement(el, function () {
        if (window.history && history.replaceState) {
          history.replaceState(null, '', href);
        }
        /* Keyboard and screen-reader users must land on the section, not
           stay behind on the link they just activated. */
        if (!el.hasAttribute('tabindex')) el.setAttribute('tabindex', '-1');
        el.focus({ preventScroll: true });
      });
    });
  }

  /* ---- Active nav link -------------------------------- */

  var sections = document.querySelectorAll('section[id]');
  var navLinks = document.querySelectorAll('[data-nav-link]');

  if (sections.length && navLinks.length && 'IntersectionObserver' in window) {
    var linkFor = {};
    navLinks.forEach(function (link) {
      var id = (link.getAttribute('href') || '').replace('#', '');
      if (id) linkFor[id] = link;
    });

    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var link = linkFor[entry.target.id];
        if (!link) return;
        if (entry.isIntersecting) {
          navLinks.forEach(function (l) { l.classList.remove('is-active'); });
          link.classList.add('is-active');
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px', threshold: 0 });

    sections.forEach(function (s) { spy.observe(s); });
  }
})();
