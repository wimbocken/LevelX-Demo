(function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("p-nav");
  var label = toggle ? toggle.querySelector(".visually-hidden") : null;

  function setOpen(open) {
    if (!nav || !toggle) return;
    nav.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    if (label) label.textContent = open ? "Sluiten" : "Menu";
    toggle.setAttribute("aria-label", open ? "Menu sluiten" : "Menu openen");
  }

  if (!toggle || !nav) return;
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
})();
