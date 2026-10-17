(function () {
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("c-nav");
  var label = toggle ? toggle.querySelector(".visually-hidden") : null;

  function setOpen(open) {
    if (!nav || !toggle) return;
    nav.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    if (label) label.textContent = open ? "Sluiten" : "Menu";
    toggle.setAttribute("aria-label", open ? "Menu sluiten" : "Menu openen");
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      setOpen(!nav.classList.contains("is-open"));
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && nav.classList.contains("is-open")) {
        setOpen(false);
        toggle.focus();
      }
    });
    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        if (window.matchMedia("(max-width: 1180px)").matches) setOpen(false);
      });
    });
  }

  var hero = document.querySelector(".hero");
  var filmButton = document.querySelector(".film-toggle");
  var glyph = filmButton ? filmButton.querySelector(".film-glyph") : null;
  var filmText = filmButton ? filmButton.querySelector(".film-toggle-text") : null;
  if (filmButton && hero) {
    filmButton.addEventListener("click", function () {
      var paused = filmButton.getAttribute("aria-pressed") === "true";
      var next = !paused;
      filmButton.setAttribute("aria-pressed", next ? "true" : "false");
      hero.classList.toggle("is-paused", next);
      if (glyph) glyph.textContent = next ? "▶" : "❚❚";
      if (filmText) filmText.textContent = next ? "Speel schoolfilm [te bevestigen]" : "Pauzeer schoolfilm [te bevestigen]";
    });
  }

  var scroller = document.getElementById("filmstrip");
  var frames = scroller ? Array.prototype.slice.call(scroller.querySelectorAll(".frame")) : [];
  var counter = document.getElementById("film-count");
  var prev = document.querySelector(".film-prev");
  var next = document.querySelector(".film-next");

  function currentIndex() {
    if (!frames.length) return 0;
    var base = frames[0].offsetLeft;
    var x = scroller.scrollLeft + base;
    var best = 0;
    var bestDist = Infinity;
    frames.forEach(function (frame, i) {
      var dist = Math.abs(frame.offsetLeft - x);
      if (dist < bestDist) {
        bestDist = dist;
        best = i;
      }
    });
    return best;
  }

  function paint(index) {
    var n = index + 1;
    if (counter) counter.textContent = (n < 10 ? "0" : "") + n + " / 08";
    if (prev) prev.setAttribute("aria-disabled", index <= 0 ? "true" : "false");
    if (next) next.setAttribute("aria-disabled", index >= frames.length - 1 ? "true" : "false");
  }

  function go(index) {
    if (!frames.length) return;
    index = Math.max(0, Math.min(frames.length - 1, index));
    var left = frames[index].offsetLeft - frames[0].offsetLeft;
    scroller.scrollTo({ left: left, behavior: reduce ? "auto" : "smooth" });
    paint(index);
  }

  if (scroller && frames.length) {
    paint(0);
    scroller.addEventListener("scroll", function () { paint(currentIndex()); }, { passive: true });
    scroller.addEventListener("keydown", function (event) {
      if (event.key === "ArrowRight") {
        event.preventDefault();
        go(currentIndex() + 1);
      } else if (event.key === "ArrowLeft") {
        event.preventDefault();
        go(currentIndex() - 1);
      }
    });
    if (prev) prev.addEventListener("click", function () { go(currentIndex() - 1); });
    if (next) next.addEventListener("click", function () { go(currentIndex() + 1); });
  }

  var layers = document.querySelectorAll("[data-parallax]");
  if (!reduce && layers.length) {
    var ticking = false;
    function shift() {
      layers.forEach(function (el) {
        var speed = parseFloat(el.getAttribute("data-parallax")) || 0;
        var rect = el.getBoundingClientRect();
        var delta = (rect.top + rect.height / 2 - window.innerHeight / 2) * speed;
        el.style.transform = "translate3d(0," + delta.toFixed(1) + "px,0)";
      });
      ticking = false;
    }
    window.addEventListener("scroll", function () {
      if (!ticking) {
        ticking = true;
        window.requestAnimationFrame(shift);
      }
    }, { passive: true });
    shift();
  }

  var nodes = document.querySelectorAll(".reveal");
  if (reduce || !("IntersectionObserver" in window)) {
    nodes.forEach(function (node) { node.classList.add("is-in"); });
    return;
  }
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("is-in");
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.16, rootMargin: "0px 0px -8% 0px" });
  nodes.forEach(function (node) { observer.observe(node); });
})();
