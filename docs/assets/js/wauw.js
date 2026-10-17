(function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("w-nav");
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
        if (window.matchMedia("(max-width: 1100px)").matches) setOpen(false);
      });
    });
  }

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
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
