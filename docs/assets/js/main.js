(function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");

  function setOpen(open) {
    if (!nav || !toggle) return;
    nav.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.textContent = open ? "Sluiten" : "Menu";
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
        if (window.matchMedia("(max-width: 1040px)").matches) setOpen(false);
      });
    });
  }

  var form = document.querySelector("[data-filter-form]");
  if (!form) return;

  var input = form.querySelector("input[type='search']");
  var chips = form.querySelectorAll("[data-filter]");
  var blocks = document.querySelectorAll("[data-domain]");
  var count = document.getElementById("result-count");
  var empty = document.getElementById("empty-state");

  function normalize(value) {
    return (value || "")
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");
  }

  function activeDomain() {
    var pressed = form.querySelector("[data-filter][aria-pressed='true']");
    return pressed ? pressed.getAttribute("data-filter") : "alle";
  }

  function apply() {
    var query = normalize(input ? input.value.trim() : "");
    var domain = activeDomain();
    var visibleStops = 0;

    blocks.forEach(function (block) {
      var blockDomain = block.getAttribute("data-domain");
      var domainOk = domain === "alle" || domain === blockDomain;
      var stops = block.querySelectorAll("[data-stop]");
      var shown = 0;
      stops.forEach(function (stop) {
        var hay = normalize(stop.getAttribute("data-stop"));
        var match = domainOk && (!query || hay.indexOf(query) !== -1);
        stop.hidden = !match;
        if (match) shown += 1;
      });
      block.hidden = !domainOk || shown === 0;
      if (block.classList.contains("domain-block")) visibleStops += shown;
    });

    if (count) {
      var label = visibleStops === 1 ? "richting" : "richtingen";
      count.textContent = visibleStops + " " + label + " zichtbaar";
    }
    if (empty) empty.hidden = visibleStops !== 0;
  }

  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      chips.forEach(function (other) {
        other.setAttribute("aria-pressed", other === chip ? "true" : "false");
      });
      apply();
    });
  });

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    apply();
  });
  if (input) input.addEventListener("input", apply);

  var hash = (location.hash || "").replace("#", "");
  if (hash) {
    chips.forEach(function (chip) {
      if (chip.getAttribute("data-filter") === hash) {
        chips.forEach(function (other) {
          other.setAttribute("aria-pressed", other === chip ? "true" : "false");
        });
      }
    });
  }
  apply();
})();
