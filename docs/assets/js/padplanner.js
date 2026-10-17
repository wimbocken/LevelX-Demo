(function () {
  var LOGO = {
    "level-1": "../assets/img/wauw/domein-level1.png",
    business: "../assets/img/wauw/domein-business.png",
    care: "../assets/img/wauw/domein-care.png",
    design: "../assets/img/wauw/domein-design.png",
    it: "../assets/img/wauw/domein-it.png",
    stem: "../assets/img/wauw/domein-stem.png",
    "leren-werken": "../assets/img/wauw/domein-leren.png",
    wereldklas: "../assets/img/wauw/domein-wereld.png"
  };
  var FIN = {
    D: {
      woord: "Doorstroom",
      lijn: "volle lijn",
      uitleg: "Je kind kan daarna vooral verder studeren, in het hoger onderwijs."
    },
    DF: {
      woord: "Dubbele finaliteit",
      lijn: "streepjeslijn",
      uitleg: "Daarna kan je kind gaan werken of verder studeren."
    },
    A: {
      woord: "Arbeidsmarkt",
      lijn: "stippellijn",
      uitleg: "Deze richting leidt naar een beroep. Een professionele bachelor kan daarna via 7NXT."
    }
  };

  var data, nodes, out, inc, pos;
  var mapBuilt = false;
  var state = {
    mode: "heen",
    stroom: null,
    domein: null,
    g2: null,
    g3: null,
    einde: null,
    doel: null
  };

  function esc(value) {
    return String(value == null ? "" : value).replace(/[&<>"']/g, function (ch) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch];
    });
  }

  function announce(message) {
    var live = document.getElementById("live");
    live.textContent = "";
    window.setTimeout(function () { live.textContent = message; }, 20);
  }

  function outgoing(id) { return out[id] || []; }
  function incoming(id) { return inc[id] || []; }

  function reachableFrom(id) {
    var seen = {};
    var queue = [id];
    seen[id] = true;
    while (queue.length) {
      var current = queue.shift();
      outgoing(current).forEach(function (edge) {
        if (!seen[edge.naar]) {
          seen[edge.naar] = true;
          queue.push(edge.naar);
        }
      });
    }
    return seen;
  }

  function isTbc(node, edge) {
    return (node && node.status === "te bevestigen") || (edge && edge.status === "te bevestigen");
  }

  function badges(node, edge) {
    var html = "";
    if (!node) return html;
    if (node.finaliteit && FIN[node.finaliteit]) {
      html += '<span class="badge badge-fin">' + esc(FIN[node.finaliteit].woord) + "</span>";
    }
    if (node.duaal || node.leren_werken) html += '<span class="badge badge-duaal">duaal leren</span>';
    (node.labels || []).forEach(function (label) {
      if (label === "nieuw") html += '<span class="badge badge-new">nieuw</span>';
      if (label === "FLEX") html += '<span class="badge badge-flex">FLEX</span>';
    });
    if (node.type === "verwijzing") html += '<span class="badge badge-new">via een ander domein</span>';
    if (isTbc(node, edge)) html += '<span class="badge badge-tbc">te bevestigen</span>';
    return html;
  }

  function finText(node) {
    if (!node || !node.finaliteit || !FIN[node.finaliteit]) return "";
    var fin = FIN[node.finaliteit];
    return fin.uitleg + " Op het metroplan is dat een " + fin.lijn + ".";
  }

  function viaText(node) {
    var ref = node && node.verwijst_naar;
    if (!ref) return "";
    var ids = Array.isArray(ref) ? ref : [ref];
    var names = ids.map(function (id) { return nodes[id] ? nodes[id].naam : id; });
    return "Je volgt daarvoor: " + names.join(" of ") + ".";
  }

  function externalLink(url, label) {
    if (!url) return "";
    return '<a href="' + esc(url) + '" target="_blank" rel="noopener noreferrer">' + esc(label) +
      '<span class="visually-hidden"> (opent in een nieuw venster)</span></a>';
  }

  function domainMeta(dom) {
    if (dom.id === "level-1") {
      return { enabled: false, reason: "Level 1 is de eerste graad. Die kies je in stap 1." };
    }
    if (dom.id === "wereldklas") {
      return { enabled: true, apart: true, edge: null };
    }
    if (!state.stroom) {
      return { enabled: false, reason: "Kies eerst een stroom in de eerste graad." };
    }
    var edge = outgoing(state.stroom).filter(function (item) { return item.naar === "dom:" + dom.id; })[0];
    if (edge) return { enabled: true, edge: edge };
    if (dom.id === "leren-werken") {
      var reach = reachableFrom(state.stroom);
      var hit = outgoing("dom:leren-werken").some(function (item) { return reach[item.naar]; });
      if (hit) return { enabled: true, via: true, edge: null };
    }
    return { enabled: false, reason: "Vanuit deze stroom loopt er geen lijn naar " + dom.naam + "." };
  }

  function step3Items() {
    if (!state.domein) return [];
    var items = [];
    outgoing("dom:" + state.domein).forEach(function (edge) {
      var node = nodes[edge.naar];
      if (!node) return;
      items.push({ node: node, edge: edge, direct: node.graad === 3 });
    });
    if (state.domein === "it" && !items.some(function (item) { return item.node.graad === 2; })) {
      data.richtingen.filter(function (node) {
        return node.domein === "it" && node.graad === 2;
      }).forEach(function (node) {
        items.push({ node: node, edge: null, via: true, direct: false });
      });
    }
    return items;
  }

  function step4Items() {
    if (state.g2 && nodes[state.g2] && nodes[state.g2].graad === 2) {
      return outgoing(state.g2).filter(function (edge) {
        return nodes[edge.naar] && nodes[edge.naar].graad === 3;
      }).map(function (edge) {
        return { node: nodes[edge.naar], edge: edge };
      });
    }
    if (state.g3 && nodes[state.g3]) return [{ node: nodes[state.g3], edge: null, locked: true }];
    return [];
  }

  function endSource() {
    if (state.g3) return state.g3;
    if (state.g2 && nodes[state.g2] && nodes[state.g2].graad !== 2) return state.g2;
    return null;
  }

  function step5Items() {
    var source = endSource();
    if (!source) return [];
    return outgoing(source).filter(function (edge) {
      var node = nodes[edge.naar];
      return node && (node.graad === 7 || node.id === "7nxt" || node.kind === "uitstroom");
    }).map(function (edge) {
      return { node: nodes[edge.naar], edge: edge };
    });
  }

  function chosenIds() {
    var ids = [];
    if (state.domein !== "wereldklas" && state.stroom) ids.push(state.stroom);
    if (state.domein) ids.push("dom:" + state.domein);
    if (state.g2) ids.push(state.g2);
    if (state.g3) ids.push(state.g3);
    if (state.einde) ids.push(state.einde);
    if (state.einde && nodes[state.einde] && nodes[state.einde].kind !== "uitstroom") {
      var next = outgoing(state.einde).filter(function (edge) {
        return nodes[edge.naar] && nodes[edge.naar].kind === "uitstroom";
      })[0];
      if (next) ids.push(next.naar);
    }
    return ids;
  }

  function clearAfter(level) {
    if (level < 2) state.domein = null;
    if (level < 3) state.g2 = null;
    if (level < 4) state.g3 = null;
    if (level < 5) state.einde = null;
  }

  function selectStroom(id) {
    state.mode = "heen";
    state.stroom = id;
    clearAfter(1);
    if (id === "2b-opstroom") {
      announce("2B opstroom. De vervolgstappen staan nog niet vast.");
    } else {
      announce(nodes[id].naam + ". Kies nu een domein.");
    }
    render({ focus: "stap2" });
  }

  function selectDomain(id) {
    state.mode = "heen";
    if (id === "wereldklas") state.stroom = null;
    state.domein = id;
    clearAfter(2);
    announce(nodes["dom:" + id].naam + ". Kies nu een richting.");
    render({ focus: "stap3" });
  }

  function selectProgram(node) {
    state.mode = "heen";
    if (node.graad === 3) {
      state.g2 = null;
      state.g3 = node.id;
      state.einde = null;
      announce(node.naam + " in de derde graad. Kies wat daarna kan.");
      render({ focus: "stap5" });
      return;
    }
    state.g2 = node.id;
    state.g3 = null;
    state.einde = null;
    if (node.type === "onthaal") {
      announce(node.naam + ". Kies de uitstroom.");
      render({ focus: "stap5" });
      return;
    }
    announce(node.naam + ". Kies nu een richting in de derde graad.");
    render({ focus: "stap4" });
  }

  function selectG3(id) {
    state.g3 = id;
    state.einde = null;
    announce(nodes[id].naam + ". Kies een zevende jaar, 7NXT of de uitstroom.");
    render({ focus: "stap5" });
  }

  function selectEinde(id) {
    state.einde = id;
    announce("Einde van de route: " + nodes[id].naam + ".");
    render({ focus: "overzicht-titel" });
  }

  function writeHash() {
    var hash = "";
    if (state.mode === "terug" && state.doel && !state.g2 && !state.g3 && !state.einde && !state.domein) {
      hash = "#terug=" + encodeURIComponent(state.doel);
    } else if (state.stroom || state.domein || state.g2 || state.g3 || state.einde) {
      var parts = [
        state.domein === "wereldklas" ? "" : (state.stroom || ""),
        state.domein || "",
        state.g2 || "",
        state.g3 || "",
        state.einde || ""
      ];
      while (parts.length && parts[parts.length - 1] === "") parts.pop();
      hash = "#heen=" + parts.map(encodeURIComponent).join(",");
    }
    var next = location.pathname + location.search + hash;
    if (location.pathname + location.search + location.hash !== next) {
      history.replaceState(null, "", next);
    }
  }

  function readHash() {
    state.mode = "heen";
    state.stroom = null;
    state.domein = null;
    state.g2 = null;
    state.g3 = null;
    state.einde = null;
    state.doel = null;
    var raw = location.hash.replace(/^#/, "");
    if (!raw) return;
    if (raw.indexOf("terug=") === 0) {
      state.mode = "terug";
      var doel = decodeURIComponent(raw.slice(6));
      state.doel = nodes[doel] ? doel : null;
      return;
    }
    if (raw.indexOf("heen=") !== 0) return;
    var parts = raw.slice(5).split(",").map(decodeURIComponent);
    var stroom = parts[0], domein = parts[1], g2 = parts[2], g3 = parts[3], einde = parts[4];
    if (nodes[stroom] && nodes[stroom].kind === "stroom") state.stroom = stroom;
    if (domein && nodes["dom:" + domein]) state.domein = domein;
    if (nodes[g2]) state.g2 = g2;
    if (nodes[g3]) state.g3 = g3;
    if (nodes[einde]) state.einde = einde;
    state.mode = "heen";
  }

  function choiceButton(item, checked, onPick) {
    var node = item.node;
    var button = document.createElement("button");
    button.type = "button";
    button.className = "choice";
    button.setAttribute("role", "radio");
    button.setAttribute("aria-checked", checked ? "true" : "false");
    var html = '<span class="choice-name">' + esc(node.naam) + "</span>" + badges(node, item.edge);
    if (node.duaal || node.leren_werken) {
      html += '<span class="why">Deels op school, deels op de werkvloer.</span>';
    }
    if (item.direct) html += '<span class="why">Deze richting start meteen in de derde graad.</span>';
    if (item.via || node.type === "verwijzing") html += '<span class="why">' + esc(viaText(node)) + "</span>";
    if (checked) html += '<span class="why">' + esc(finText(node)) + "</span>";
    button.innerHTML = html;
    button.addEventListener("click", function () { onPick(node); });
    var wrap = document.createElement("div");
    wrap.appendChild(button);
    if (node.url) {
      var more = document.createElement("p");
      more.className = "more-link";
      more.innerHTML = externalLink(node.url, "Lees meer op levelx.be");
      wrap.appendChild(more);
    }
    return wrap;
  }

  function radioKeys(group) {
    group.addEventListener("keydown", function (event) {
      var keys = ["ArrowDown", "ArrowUp", "ArrowRight", "ArrowLeft"];
      if (keys.indexOf(event.key) === -1) return;
      var buttons = Array.prototype.slice.call(group.querySelectorAll('[role="radio"]:not(:disabled)'));
      if (!buttons.length) return;
      var index = buttons.indexOf(document.activeElement);
      if (index === -1) index = 0;
      var next = event.key === "ArrowUp" || event.key === "ArrowLeft" ? index - 1 : index + 1;
      if (next < 0) next = buttons.length - 1;
      if (next >= buttons.length) next = 0;
      event.preventDefault();
      buttons[next].focus();
    });
  }

  function renderHeen(root) {
    var list = document.createElement("ol");
    list.className = "steps";

    list.appendChild(stepBlock(1, "Eerste graad", "In welke stroom zit je kind?", function (body) {
      var group = document.createElement("div");
      group.className = "choices";
      group.setAttribute("role", "radiogroup");
      group.setAttribute("aria-labelledby", "stap1");
      data.stroom.forEach(function (item) {
        var button = document.createElement("button");
        button.type = "button";
        button.className = "choice";
        button.setAttribute("role", "radio");
        button.setAttribute("aria-checked", state.stroom === item.id && state.domein !== "wereldklas" ? "true" : "false");
        button.innerHTML = '<span class="choice-name">' + esc(item.naam) + "</span>" + badges(item, null);
        button.addEventListener("click", function () { selectStroom(item.id); });
        var wrap = document.createElement("div");
        wrap.appendChild(button);
        if (item.url) {
          var more = document.createElement("p");
          more.className = "more-link";
          more.innerHTML = externalLink(item.url, "Lees meer op levelx.be");
          wrap.appendChild(more);
        }
        group.appendChild(wrap);
      });
      radioKeys(group);
      body.appendChild(group);
    }));

    list.appendChild(stepBlock(2, "Domein", "Welk domein trekt? We laten zien wat vanuit de gekozen stroom bereikbaar is.", function (body) {
      if (!state.stroom && state.domein !== "wereldklas") {
        body.appendChild(note("Kies een stroom, of start bij Wereldklas als je kind nieuw is in het Nederlands."));
      }
      if (state.stroom === "2b-opstroom") {
        body.appendChild(note("Voor 2B opstroom liggen de vervolgstappen nog niet vast. Dit onderdeel stemmen we nog af met de school."));
      }
      var grid = document.createElement("div");
      grid.className = "domains";
      grid.setAttribute("role", "radiogroup");
      grid.setAttribute("aria-labelledby", "stap2");
      data.domeinen.forEach(function (dom) {
        var meta = domainMeta(dom);
        var button = document.createElement("button");
        button.type = "button";
        button.className = "domain";
        button.setAttribute("role", "radio");
        button.setAttribute("aria-checked", state.domein === dom.id ? "true" : "false");
        if (!meta.enabled) button.disabled = true;
        var edge = meta.edge;
        button.innerHTML = '<img src="' + esc(LOGO[dom.id]) + '" alt="" width="44" height="44"><span><span class="domain-name">' +
          esc(dom.naam) + "</span>" + badges({ status: edge && edge.status, labels: [] }, edge) +
          (meta.apart ? '<span class="why">Apart onthaaljaar, niet via 1A of 1B.</span>' : "") +
          (meta.via ? '<span class="why">Duaal leren: dezelfde richtingen, vertrokken vanuit leren en werken.</span>' : "") +
          (!meta.enabled ? '<span class="why">' + esc(meta.reason) + "</span>" : "") +
          "</span>";
        button.addEventListener("click", function () { if (meta.enabled) selectDomain(dom.id); });
        grid.appendChild(button);
      });
      radioKeys(grid);
      body.appendChild(grid);
    }));

    list.appendChild(stepBlock(3, "Tweede graad", "Kies een richting in het 3e en 4e jaar, of een richting die meteen in de derde graad start.", function (body) {
      var items = step3Items();
      if (!state.domein) {
        body.appendChild(note("Kies eerst een domein."));
        return;
      }
      if (!items.length) {
        body.appendChild(note("Vanuit dit domein zijn er nog geen richtingen in het plan."));
        return;
      }
      var early = items.filter(function (item) { return item.node.graad === 2 || item.via; });
      var onthaal = items.filter(function (item) { return item.node.type === "onthaal"; });
      var direct = items.filter(function (item) { return item.node.graad === 3; });
      if (onthaal.length) {
        body.appendChild(label("Onthaaljaar", "lab-onthaal"));
        body.appendChild(choiceGroup("keuze-onthaal", "lab-onthaal", onthaal, function (node) {
          return state.g2 === node.id;
        }, selectProgram));
      }
      if (early.length) {
        body.appendChild(label("Tweede graad", "lab-g2"));
        body.appendChild(choiceGroup("keuze-g2", "lab-g2", early, function (node) {
          return state.g2 === node.id;
        }, selectProgram));
      }
      if (direct.length) {
        body.appendChild(label("Meteen in de derde graad", "lab-direct"));
        body.appendChild(choiceGroup("keuze-direct", "lab-direct", direct, function (node) {
          return state.g3 === node.id && !state.g2;
        }, selectProgram));
      }
    }));

    list.appendChild(stepBlock(4, "Derde graad", "Kies de richting in het 5e en 6e jaar.", function (body) {
      if (state.g2 && nodes[state.g2] && nodes[state.g2].type === "onthaal") {
        body.appendChild(note("Na het onthaaljaar is er geen tweede of derde graad. Kies hieronder de uitstroom."));
        return;
      }
      var items = step4Items();
      if (!state.g2 && !state.g3) {
        body.appendChild(note("Kies eerst een richting in de tweede graad."));
        return;
      }
      if (!items.length) {
        body.appendChild(note("Vanuit deze richting is er geen derde graad in het plan."));
        return;
      }
      body.appendChild(choiceGroup("keuze-g3", "stap4", items, function (node) {
        return state.g3 === node.id;
      }, function (node) { selectG3(node.id); }));
    }));

    list.appendChild(stepBlock(5, "Daarna", "Een zevende jaar, 7NXT, of meteen de uitstroom.", function (body) {
      var items = step5Items();
      if (!endSource()) {
        body.appendChild(note("Kies eerst de richting in de derde graad."));
        return;
      }
      if (!items.length) {
        body.appendChild(note("Voor deze halte staat nog niet vast wat daarna kan."));
        return;
      }
      var years = items.filter(function (item) { return item.node.graad === 7 || item.node.id === "7nxt"; });
      var exits = items.filter(function (item) { return item.node.kind === "uitstroom"; });
      if (years.length) {
        body.appendChild(label("7e jaar en 7NXT", "lab-jaren"));
        body.appendChild(choiceGroup("keuze-jaren", "lab-jaren", years, function (node) {
          return state.einde === node.id;
        }, function (node) { selectEinde(node.id); }));
      }
      if (exits.length) {
        body.appendChild(label("Uitstroom", "lab-uit"));
        body.appendChild(choiceGroup("keuze-uit", "lab-uit", exits, function (node) {
          return state.einde === node.id;
        }, function (node) { selectEinde(node.id); }));
      }
    }));

    root.appendChild(list);
  }

  function stepBlock(number, title, help, fill) {
    var item = document.createElement("li");
    item.className = "step";
    var heading = document.createElement("h2");
    heading.id = "stap" + number;
    heading.textContent = number + ". " + title;
    item.appendChild(heading);
    var helpNode = document.createElement("p");
    helpNode.className = "step-help";
    helpNode.textContent = help;
    item.appendChild(helpNode);
    var body = document.createElement("div");
    fill(body);
    item.appendChild(body);
    return item;
  }

  function note(text) {
    var p = document.createElement("p");
    p.className = "step-help";
    p.textContent = text;
    return p;
  }

  function label(text, id) {
    var p = document.createElement("p");
    p.className = "group-label";
    if (id) p.id = id;
    p.textContent = text;
    return p;
  }

  function choiceGroup(id, labelId, items, isChecked, onPick) {
    var group = document.createElement("div");
    group.className = "choices";
    group.id = id;
    group.setAttribute("role", "radiogroup");
    if (labelId) group.setAttribute("aria-labelledby", labelId);
    items.forEach(function (item) {
      group.appendChild(choiceButton(item, isChecked(item.node), onPick));
    });
    radioKeys(group);
    return group;
  }

  function routesTo(goal, limit) {
    var routes = [];
    var entries = { "1a": true, "1b": true, "2b-opstroom": true, "dom:leren-werken": true, "dom:wereldklas": true };
    function walk(node, stack, seen) {
      if (routes.length >= limit) return;
      if (entries[node] && stack.length > 1) {
        routes.push(stack.slice().reverse());
        return;
      }
      var parents = incoming(node);
      if (!parents.length) return;
      parents.forEach(function (edge) {
        if (seen[edge.van] || routes.length >= limit) return;
        seen[edge.van] = true;
        stack.push(edge.van);
        walk(edge.van, stack, seen);
        stack.pop();
        delete seen[edge.van];
      });
    }
    var seen = {};
    seen[goal] = true;
    walk(goal, [goal], seen);
    return routes;
  }

  function applyIds(ids) {
    state.stroom = null;
    state.domein = null;
    state.g2 = null;
    state.g3 = null;
    state.einde = null;
    ids.forEach(function (id) {
      var node = nodes[id];
      if (!node) return;
      if (node.kind === "stroom") state.stroom = id;
      else if (node.kind === "domein") state.domein = node.domeinId;
      else if (node.graad === 2 || node.type === "onthaal") state.g2 = id;
      else if (node.graad === 3) state.g3 = id;
      else if (node.graad === 7 || node.id === "7nxt") state.einde = id;
      else if (node.kind === "uitstroom" && (!state.einde || nodes[state.einde].kind === "uitstroom")) state.einde = id;
    });
    state.mode = "heen";
  }

  function renderTerug(root) {
    var intro = document.createElement("p");
    intro.className = "step-help";
    intro.textContent = "Kies waar je kind later wil staan. We tonen de routes die daar naartoe lopen.";
    root.appendChild(intro);

    var goals = document.createElement("div");
    goals.className = "goal-list";
    goals.setAttribute("role", "group");
    goals.setAttribute("aria-label", "Doelen");
    root.appendChild(label("Na het secundair"));
    data.uitstroom.forEach(function (item) { goals.appendChild(goalButton(item)); });
    root.appendChild(goals);

    var nxt = nodes["7nxt"];
    if (nxt) {
      root.appendChild(label("Schakeljaar"));
      var nxtWrap = document.createElement("div");
      nxtWrap.className = "goal-list";
      nxtWrap.appendChild(goalButton(nxt));
      root.appendChild(nxtWrap);
    }

    root.appendChild(label("Een zevende jaar"));
    var years = document.createElement("div");
    years.className = "goal-list";
    data.richtingen.filter(function (node) { return node.graad === 7; }).forEach(function (node) {
      years.appendChild(goalButton(node));
    });
    root.appendChild(years);

    if (!state.doel || !nodes[state.doel]) return;
    var routes = routesTo(state.doel, 100);
    var heading = document.createElement("h2");
    heading.className = "h3";
    heading.textContent = "Routes naar " + nodes[state.doel].naam;
    heading.id = "routes-titel";
    root.appendChild(heading);
    if (!routes.length) {
      root.appendChild(note("We kunnen nog geen volledige route naar deze halte tonen."));
      return;
    }
    if (routes.length >= 100) {
      root.appendChild(note("Er zijn veel routes. We tonen de eerste 100. Kies een zevende jaar om te verfijnen."));
    }
    var groups = {};
    routes.forEach(function (route) {
      var domain = route.filter(function (id) { return nodes[id] && nodes[id].kind === "domein"; })[0] || "overig";
      if (!groups[domain]) groups[domain] = [];
      groups[domain].push(route);
    });
    Object.keys(groups).forEach(function (key, index) {
      var details = document.createElement("details");
      details.open = index === 0 || Object.keys(groups).length < 4;
      var summary = document.createElement("summary");
      summary.textContent = (nodes[key] ? nodes[key].naam : "Overige") + " (" + groups[key].length + ")";
      details.appendChild(summary);
      var box = document.createElement("div");
      box.className = "route-list";
      groups[key].forEach(function (route) {
        var button = document.createElement("button");
        button.type = "button";
        button.className = "route";
        button.textContent = route.map(function (id) { return nodes[id] ? nodes[id].naam : id; }).join(" → ");
        button.addEventListener("click", function () {
          applyIds(route);
          announce("Route geladen: " + button.textContent);
          render({ focus: "overzicht-titel" });
        });
        box.appendChild(button);
      });
      details.appendChild(box);
      root.appendChild(details);
    });
  }

  function goalButton(node) {
    var button = document.createElement("button");
    button.type = "button";
    button.className = "goal";
    button.setAttribute("aria-pressed", state.doel === node.id ? "true" : "false");
    button.innerHTML = '<span class="choice-name">' + esc(node.naam) + "</span>" + badges(node, null);
    button.addEventListener("click", function () {
      state.mode = "terug";
      state.doel = node.id;
      state.stroom = null;
      state.domein = null;
      state.g2 = null;
      state.g3 = null;
      state.einde = null;
      announce("Doel: " + node.naam + ". De mogelijke routes staan hieronder.");
      render({ focus: "routes-titel" });
    });
    return button;
  }

  function renderSummary() {
    var body = document.getElementById("summary-body");
    var ids = chosenIds();
    if (!ids.length) {
      body.innerHTML = "<p>Nog geen keuze. Begin bij de eerste graad, of kies een doel bij “Ik wil later…”.</p>";
    } else {
      var html = "<ol>";
      ids.forEach(function (id) {
        var node = nodes[id];
        html += "<li><strong>" + esc(node.naam) + "</strong> " + badges(node, null);
        if (node.finaliteit) html += '<div class="why">' + esc(finText(node)) + "</div>";
        if (node.duaal || node.leren_werken) html += '<div class="why">Duaal leren: deels op school, deels op de werkvloer.</div>';
        if (node.url) html += "<div>" + externalLink(node.url, "Lees meer op levelx.be") + "</div>";
        html += "</li>";
      });
      html += "</ol>";
      body.innerHTML = html;
    }
    var words = document.getElementById("map-text");
    words.innerHTML = "";
    if (!ids.length) {
      var empty = document.createElement("li");
      empty.textContent = "Nog geen route gekozen.";
      words.appendChild(empty);
    } else {
      ids.forEach(function (id) {
        var item = document.createElement("li");
        item.textContent = nodes[id].naam;
        words.appendChild(item);
      });
    }
    var phone = data.meta && data.meta.contact;
    if (phone) {
      document.getElementById("phone-line").textContent = "Liever bellen? " + phone.telefoon + ".";
    }
  }

  function domainColor(id) {
    var node = nodes[id];
    var domId = node && (node.domeinId || node.domein);
    var dom = data.domeinen.filter(function (item) { return item.id === domId; })[0];
    if (dom) return dom.kleur;
    if (node && node.kind === "uitstroom") return "#0b4d3b";
    if (node && node.id === "7nxt") return "#1b4332";
    return "#1b4332";
  }

  function dashFor(edge) {
    var target = nodes[edge.naar];
    var source = nodes[edge.van];
    var fin = (target && target.finaliteit) || (source && source.finaliteit);
    if (fin === "DF") return "8 6";
    if (fin === "A") return "2 5";
    return null;
  }

  function buildMap() {
    var ROW = 42;
    var GAP = 26;
    var col = { stroom: 36, domein: 250, g2: 560, g3: 900, g7: 1240, uit: 1540 };
    pos = {};
    var y = 48;
    var bands = {};
    data.domeinen.forEach(function (dom) {
      var g2 = data.richtingen.filter(function (node) { return node.domein === dom.id && node.graad === 2; });
      var g3 = data.richtingen.filter(function (node) { return node.domein === dom.id && node.graad === 3; });
      var g7 = data.richtingen.filter(function (node) { return node.domein === dom.id && node.graad === 7; });
      var extra = data.speciaal.filter(function (node) { return node.domein === dom.id; });
      var count = Math.max(g2.length, g3.length, g7.length, extra.length, 1);
      if (dom.id === "level-1") count = Math.max(count, data.stroom.length);
      bands[dom.id] = { y: y, h: count * ROW, g2: g2, g3: g3, g7: g7, extra: extra };
      y += count * ROW + GAP;
    });
    var height = y + 36;
    var width = 1760;

    function place(list, x, band) {
      list.forEach(function (node, index) {
        pos[node.id] = { x: x, y: band.y + 18 + index * ROW };
      });
    }
    data.domeinen.forEach(function (dom) {
      var band = bands[dom.id];
      pos["dom:" + dom.id] = { x: col.domein, y: band.y + band.h / 2 };
      place(band.g2, col.g2, band);
      place(band.g3, col.g3, band);
      place(band.g7, col.g7, band);
      place(band.extra, col.g3, band);
    });
    data.stroom.forEach(function (item, index) {
      var band = bands["level-1"];
      pos[item.id] = { x: col.stroom, y: band.y + 18 + index * ROW };
    });
    if (nodes["7nxt"]) {
      var lastY = Math.max.apply(null, data.richtingen.filter(function (node) { return node.graad === 7; }).map(function (node) {
        return pos[node.id] ? pos[node.id].y : 0;
      }).concat([80]));
      pos["7nxt"] = { x: col.g7, y: Math.min(lastY + ROW, height - 28) };
    }
    data.uitstroom.forEach(function (item, index) {
      pos[item.id] = { x: col.uit, y: 80 + index * ((height - 140) / Math.max(data.uitstroom.length - 1, 1)) };
    });

    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("viewBox", "0 0 " + width + " " + height);
    svg.setAttribute("width", String(width));
    svg.setAttribute("height", String(height));
    svg.setAttribute("role", "group");
    svg.setAttribute("aria-label", "Metroplan. Elke halte is een knop.");

    var g7ys = data.richtingen.filter(function (node) { return node.graad === 7 && pos[node.id]; }).map(function (node) { return pos[node.id].y; });
    if (pos["7nxt"]) g7ys.push(pos["7nxt"].y);
    if (g7ys.length > 1) {
      var line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      line.setAttribute("class", "collector-line");
      line.setAttribute("x1", String(col.g7));
      line.setAttribute("x2", String(col.g7));
      line.setAttribute("y1", String(Math.min.apply(null, g7ys)));
      line.setAttribute("y2", String(Math.max.apply(null, g7ys)));
      svg.appendChild(line);
      var tag = document.createElementNS("http://www.w3.org/2000/svg", "text");
      tag.setAttribute("x", String(col.g7 + 16));
      tag.setAttribute("y", String(Math.min.apply(null, g7ys) - 12));
      tag.setAttribute("fill", "#1b4332");
      tag.setAttribute("font-size", "13");
      tag.setAttribute("font-family", "Inter, sans-serif");
      tag.setAttribute("font-weight", "700");
      tag.textContent = "7e jaar";
      svg.appendChild(tag);
    }

    data.edges.forEach(function (edge) {
      if (!pos[edge.van] || !pos[edge.naar]) return;
      var path = document.createElementNS("http://www.w3.org/2000/svg", "path");
      var from = pos[edge.van];
      var to = pos[edge.naar];
      var mid = (from.x + to.x) / 2;
      path.setAttribute("d", "M " + from.x + " " + from.y + " C " + mid + " " + from.y + ", " + mid + " " + to.y + ", " + to.x + " " + to.y);
      path.setAttribute("class", "edge");
      path.setAttribute("data-van", edge.van);
      path.setAttribute("data-naar", edge.naar);
      path.setAttribute("stroke", domainColor(edge.naar));
      path.setAttribute("stroke-width", "2.5");
      path.setAttribute("opacity", "0.35");
      var dash = dashFor(edge);
      if (dash) path.setAttribute("stroke-dasharray", dash);
      svg.appendChild(path);
    });

    Object.keys(pos).forEach(function (id) {
      if (!nodes[id]) return;
      var point = pos[id];
      var group = document.createElementNS("http://www.w3.org/2000/svg", "g");
      group.setAttribute("class", "station");
      group.setAttribute("tabindex", "0");
      group.setAttribute("role", "button");
      group.setAttribute("aria-pressed", "false");
      group.setAttribute("data-id", id);
      group.setAttribute("aria-label", nodes[id].naam);
      var ring = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      ring.setAttribute("class", "ring");
      ring.setAttribute("cx", String(point.x));
      ring.setAttribute("cy", String(point.y));
      ring.setAttribute("r", "12");
      var dot = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      dot.setAttribute("class", "dot");
      dot.setAttribute("cx", String(point.x));
      dot.setAttribute("cy", String(point.y));
      dot.setAttribute("r", "7");
      dot.setAttribute("fill", domainColor(id));
      var text = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text.setAttribute("x", String(point.x + 16));
      text.setAttribute("y", String(point.y + 4));
      text.setAttribute("fill", "#1f2421");
      text.setAttribute("font-size", "12");
      text.setAttribute("font-family", "Inter, sans-serif");
      var name = nodes[id].naam;
      if (name.length > 34) {
        var cut = name.lastIndexOf(" ", 34);
        if (cut < 12) cut = 34;
        text.textContent = name.slice(0, cut);
        var line2 = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
        line2.setAttribute("x", String(point.x + 16));
        line2.setAttribute("dy", "13");
        line2.textContent = name.slice(cut).trim();
        text.appendChild(line2);
        text.setAttribute("y", String(point.y - 2));
      } else {
        text.textContent = name;
      }
      group.appendChild(ring);
      group.appendChild(dot);
      group.appendChild(text);
      group.addEventListener("click", function () { openStation(id); });
      group.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          openStation(id);
        }
      });
      svg.appendChild(group);
    });

    var host = document.getElementById("map-host");
    host.innerHTML = "";
    host.appendChild(svg);
    mapBuilt = true;
  }

  function updateMap() {
    if (!mapBuilt) buildMap();
    var ids = chosenIds();
    var on = {};
    ids.forEach(function (id) { on[id] = true; });
    document.querySelectorAll(".edge").forEach(function (edge) {
      var from = edge.getAttribute("data-van");
      var to = edge.getAttribute("data-naar");
      var index = ids.indexOf(from);
      var active = index >= 0 && ids[index + 1] === to;
      edge.setAttribute("opacity", active ? "1" : "0.28");
      edge.setAttribute("stroke-width", active ? "4.5" : "2.5");
    });
    document.querySelectorAll(".station").forEach(function (station) {
      var active = !!on[station.getAttribute("data-id")];
      station.classList.toggle("is-on", active);
      station.setAttribute("aria-pressed", active ? "true" : "false");
    });
  }

  function shortestTo(target) {
    if (!nodes[target]) return null;
    if (nodes[target].kind === "stroom") return [target];
    var cost = {};
    var prev = {};
    var queue = [{ id: target, cost: 0 }];
    cost[target] = 0;
    var found = null;
    while (queue.length) {
      queue.sort(function (a, b) { return a.cost - b.cost; });
      var current = queue.shift();
      if (current.cost !== cost[current.id]) continue;
      if (current.id !== target && (nodes[current.id].kind === "stroom" || current.id === "dom:wereldklas")) {
        found = current.id;
        break;
      }
      incoming(current.id).forEach(function (edge) {
        var weight = edge.status === "te bevestigen" ? 3 : 1;
        var next = current.cost + weight;
        if (cost[edge.van] == null || next < cost[edge.van]) {
          cost[edge.van] = next;
          prev[edge.van] = current.id;
          queue.push({ id: edge.van, cost: next });
        }
      });
    }
    if (!found) return null;
    var path = [found];
    var cursor = found;
    var guard = 0;
    while (cursor !== target && guard < 30) {
      cursor = prev[cursor];
      if (!cursor) return null;
      path.push(cursor);
      guard += 1;
    }
    return path;
  }

  function fallbackPath(id) {
    var node = nodes[id];
    if (!node) return null;
    if (node.kind === "domein") {
      var stroom = data.stroom.filter(function (item) {
        return outgoing(item.id).some(function (edge) { return edge.naar === id; });
      })[0];
      return stroom ? [stroom.id, id] : [id];
    }
    if (node.domein) {
      var dom = "dom:" + node.domein;
      var start = data.stroom.filter(function (item) {
        return outgoing(item.id).some(function (edge) { return edge.naar === dom; });
      })[0];
      var path = [];
      if (start && node.domein !== "wereldklas") path.push(start.id);
      path.push(dom);
      if (node.graad === 3 || node.graad === 7) {
        var parent = incoming(id).map(function (edge) { return edge.van; }).filter(function (van) {
          return nodes[van] && (nodes[van].graad === 2 || nodes[van].graad === 3);
        })[0];
        if (parent && node.graad === 7 && nodes[parent].graad === 3) {
          var mid = fallbackPath(parent) || [];
          return mid.concat([id]);
        }
        if (parent && node.graad === 3) path.push(parent);
      }
      path.push(id);
      return path;
    }
    return [id];
  }

  function openStation(id) {
    var path = shortestTo(id);
    if (!path) {
      var node = nodes[id];
      if (node && node.graad !== 2 && node.kind !== "domein" && node.kind !== "stroom") {
        state.mode = "heen";
        state.stroom = null;
        state.domein = null;
        state.g2 = null;
        state.g3 = null;
        state.einde = id;
        announce(node.naam + ". Voor deze halte kunnen we nog geen volledige route tonen.");
        render();
        return;
      }
      path = fallbackPath(id);
    }
    if (!path) {
      announce("Voor deze halte kunnen we nog geen route tonen.");
      return;
    }
    applyIds(path);
    announce("Route geopend vanaf " + nodes[path[0]].naam + ".");
    render();
  }

  function render(options) {
    options = options || {};
    var root = document.getElementById("planner-body");
    root.innerHTML = "";
    document.getElementById("mode-heen").setAttribute("aria-pressed", state.mode === "heen" ? "true" : "false");
    document.getElementById("mode-terug").setAttribute("aria-pressed", state.mode === "terug" ? "true" : "false");
    if (state.mode === "terug") renderTerug(root);
    else renderHeen(root);
    renderSummary();
    updateMap();
    writeHash();
    if (options.focus) {
      var target = document.getElementById(options.focus);
      if (target) {
        if (!target.hasAttribute("tabindex")) target.setAttribute("tabindex", "-1");
        target.focus();
      }
    }
  }

  function bindChrome() {
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.getElementById("pad-nav");
    var hidden = toggle.querySelector(".visually-hidden");
    function setOpen(open) {
      nav.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Menu sluiten" : "Menu openen");
      hidden.textContent = open ? "Sluiten" : "Menu";
    }
    toggle.addEventListener("click", function () { setOpen(!nav.classList.contains("is-open")); });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && nav.classList.contains("is-open")) {
        setOpen(false);
        toggle.focus();
      }
    });
    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        if (window.matchMedia("(max-width: 720px)").matches) setOpen(false);
      });
    });
    document.getElementById("mode-heen").addEventListener("click", function () {
      state.mode = "heen";
      announce("Je bouwt een route van de eerste graad naar later.");
      render({ focus: "stap1" });
    });
    document.getElementById("mode-terug").addEventListener("click", function () {
      state.mode = "terug";
      announce("Kies een doel. We zoeken de routes terug.");
      render();
    });
    document.getElementById("btn-print").addEventListener("click", function () { window.print(); });
    document.getElementById("btn-share").addEventListener("click", function () {
      writeHash();
      var url = location.href;
      var status = document.getElementById("share-status");
      var field = document.getElementById("share-url");
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(function () {
          status.textContent = "Link gekopieerd. Je kan ze plakken in een bericht.";
          field.hidden = true;
          announce("De link van deze route is gekopieerd.");
        }).catch(function () {
          field.hidden = false;
          field.value = url;
          field.focus();
          field.select();
          status.textContent = "Kopieer de link hieronder.";
        });
      } else {
        field.hidden = false;
        field.value = url;
        field.focus();
        field.select();
        status.textContent = "Kopieer de link hieronder.";
      }
    });
    if (window.matchMedia("(min-width: 960px)").matches) {
      document.getElementById("map-panel").open = true;
    }
  }

  bindChrome();
  fetch("metroplan.json").then(function (response) {
    if (!response.ok) throw new Error("load");
    return response.json();
  }).then(function (json) {
    data = json;
    nodes = {};
    out = {};
    inc = {};
    data.stroom.forEach(function (item) { item.kind = "stroom"; nodes[item.id] = item; });
    data.domeinen.forEach(function (item) {
      nodes["dom:" + item.id] = {
        id: "dom:" + item.id,
        domeinId: item.id,
        naam: item.naam,
        kind: "domein",
        kleur: item.kleur,
        status: "bevestigd",
        labels: []
      };
    });
    data.richtingen.forEach(function (item) { item.kind = item.type === "verwijzing" ? "richting" : "richting"; nodes[item.id] = item; });
    data.speciaal.forEach(function (item) { item.kind = "speciaal"; nodes[item.id] = item; });
    data.uitstroom.forEach(function (item) { item.kind = "uitstroom"; nodes[item.id] = item; });
    data.edges.forEach(function (edge) {
      if (edge.van === "?") return;
      if (!out[edge.van]) out[edge.van] = [];
      if (!inc[edge.naar]) inc[edge.naar] = [];
      out[edge.van].push(edge);
      inc[edge.naar].push(edge);
    });
    var phone = data.meta && data.meta.contact && data.meta.contact.telefoon;
    if (phone) {
      document.getElementById("footer-phone").textContent = phone;
    }
    readHash();
    render();
    window.addEventListener("hashchange", function () {
      readHash();
      render();
    });
  }).catch(function () {
    document.getElementById("planner-body").textContent = "Het metroplan kon niet geladen worden. Herlaad de pagina.";
  });
})();
