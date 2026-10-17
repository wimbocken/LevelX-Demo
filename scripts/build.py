#!/usr/bin/env python3
"""Generate the static Level X demo into /docs."""

import hashlib
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "docs"
OVERVIEW = "https://www.levelx.be/studieaanbod-overzicht"
A_URL = "https://www.levelx.be/studieaanbod/eerste-graad-a-stroom"
B_URL = "https://www.levelx.be/studieaanbod/eerste-graad-b-stroom"
EG_URL = "https://www.levelx.be/studieaanbod/eerste-graad"
WERELD_URL = "https://www.levelx.be/studieaanbod/wereldklas"
DUAAL_URL = "https://www.levelx.be/duaal"
MW_URL = "https://www.levelx.be/studieaanbod/maatschappij-welzijnswetenschappen"
ICW_URL = "https://www.levelx.be/studieaanbod/informatie-en-communicatiewetenschappen-d"
APP_URL = "https://www.levelx.be/studieaanbod/applicatie-en-databeheer-d-a"
INSCH_URL = "https://www.levelx.be/je-kind-inschrijven"
CONTACT_URL = "https://www.levelx.be/contact"
OUDERS_URL = "https://www.levelx.be/informatie-voor-ouders"
SCHOOL_URL = "https://www.levelx.be/"
FB_URL = "https://facebook.com/GOnextLevelx"

DOMAINS = [
    ("level1", "Level 1", "level 1", "Eerste graad: proeven van alle domeinen en ontdekken wat bij je past.", "eerste-graad/"),
    ("business", "Business", "business", "Economie, organisatie en ondernemen.", "studieaanbod/#business"),
    ("care", "Care", "care", "Zorg, welzijn en werken met mensen.", "studieaanbod/#care"),
    ("design", "Design", "design", "Creatie, vormgeving en beeld.", "studieaanbod/#design"),
    ("it", "IT", "IT", "Informatica, netwerken en programmeren.", "studieaanbod/#it"),
    ("stem", "STEM", "STEM", "Wetenschap, techniek en wiskunde.", "studieaanbod/#stem"),
    ("leren", "Leren & Werken", "leren & werken", "Duaal leren: op school én op de werkvloer.", "studieaanbod/#leren"),
    ("wereld", "Wereldklas", "wereld klas", "Onthaalonderwijs voor anderstalige nieuwkomers (OKAN).", "studieaanbod/#wereld"),
]

# grade: "2" tweede, "3" derde, "7" zevende, "1" eerste
# Programs follow levelx.be/studieaanbod-overzicht unless a blurb cites another page.
PROGRAMS = [
    ("Bedrijfswetenschappen", "business", "2", "Doorstroom", "", OVERVIEW, "Tweede graad, doorstroomfinaliteit, volgens het studieaanbod-overzicht."),
    ("Bedrijf en Organisatie", "business", "2", "Dubbele finaliteit", "", OVERVIEW, "Tweede graad, dubbele finaliteit, volgens het studieaanbod-overzicht."),
    ("Organisatie & Logistiek", "business", "2", "Arbeidsmarkt", "", OVERVIEW, "Tweede graad, arbeidsmarktfinaliteit, volgens het studieaanbod-overzicht."),
    ("Maatschappij & welzijnswetenschappen", "care", "2", "Doorstroom", "", MW_URL, "Tweede graad (3e en 4e leerjaar), doorstroom, studiedomein Maatschappij en welzijn. De richting combineert een brede algemene basisvorming met sociale, gedrags- en cultuurwetenschappen. Lessentabel op de schoolsite: 32 uur."),
    ("Maatschappij & Welzijn", "care", "2", "Dubbele finaliteit", "", OVERVIEW, "Tweede graad, dubbele finaliteit, volgens het studieaanbod-overzicht."),
    ("Wellness & Lifestyle", "care", "2", "Dubbele finaliteit", "", OVERVIEW, "Tweede graad, dubbele finaliteit, volgens het studieaanbod-overzicht."),
    ("Zorg & Welzijn", "care", "2", "Arbeidsmarkt", "", OVERVIEW, "Tweede graad, arbeidsmarktfinaliteit, volgens het studieaanbod-overzicht."),
    ("Haar- & Schoonheidsverzorging", "care", "2", "Arbeidsmarkt", "", OVERVIEW, "Tweede graad, arbeidsmarktfinaliteit, volgens het studieaanbod-overzicht."),
    ("Fotografie", "design", "2", "Dubbele finaliteit", "", OVERVIEW, "Tweede graad, dubbele finaliteit, volgens het studieaanbod-overzicht."),
    ("Grafische technieken", "design", "2", "Dubbele finaliteit", "", OVERVIEW, "Tweede graad, dubbele finaliteit, volgens het studieaanbod-overzicht."),
    ("Decor en Etalage", "design", "2", "Arbeidsmarkt", "", OVERVIEW, "Tweede graad, arbeidsmarktfinaliteit, volgens het studieaanbod-overzicht."),
    ("Printmedia", "design", "2", "Arbeidsmarkt", "nieuw", OVERVIEW, "Tweede graad, arbeidsmarktfinaliteit. Op het overzicht aangeduid als nieuw."),
    ("Technologische wetenschappen met extra programmeren", "it", "2", "Via STEM", "", ICW_URL, "Op het studieaanbod-overzicht staat bij IT in de tweede graad geen aparte richtingnaam, wel deze formulering. De pagina Informatica- en communicatiewetenschappen noemt de tweede graad technologische wetenschappen (met extra programmeren) als aangewezen vooropleiding."),
    ("Technologische wetenschappen", "stem", "2", "Doorstroom", "", OVERVIEW, "Tweede graad, doorstroomfinaliteit, volgens het studieaanbod-overzicht."),
    ("Biotechnologische STEM-wetenschappen", "stem", "2", "Doorstroom", "", OVERVIEW, "Tweede graad, doorstroomfinaliteit, volgens het studieaanbod-overzicht."),
    ("Biotechnieken", "stem", "2", "Dubbele finaliteit", "nieuw", OVERVIEW, "Tweede graad, dubbele finaliteit. Op het overzicht aangeduid als nieuw."),
    ("Elektromechanische technieken", "stem", "2", "Dubbele finaliteit", "", OVERVIEW, "Tweede graad, dubbele finaliteit, volgens het studieaanbod-overzicht."),
    ("Elektriciteit", "stem", "2", "Arbeidsmarkt", "", OVERVIEW, "Tweede graad, arbeidsmarktfinaliteit, volgens het studieaanbod-overzicht."),
    ("Auto", "stem", "2", "Arbeidsmarkt", "", OVERVIEW, "Tweede graad, arbeidsmarktfinaliteit. De schoolsite vermeldt Auto als context binnen elektriciteit."),
    ("Mechanica", "stem", "2", "Arbeidsmarkt", "", OVERVIEW, "Tweede graad, arbeidsmarktfinaliteit. De schoolsite vermeldt dit als voorbereiding op carrosserie."),
    ("Hout", "stem", "2", "Arbeidsmarkt", "flex", OVERVIEW, "Tweede graad, arbeidsmarktfinaliteit. Op het overzicht gelabeld als FLEX."),
    ("Bedrijfswetenschappen", "business", "3", "Doorstroom", "", OVERVIEW, "Derde graad, doorstroomfinaliteit, volgens het studieaanbod-overzicht."),
    ("Bedrijfsorganisatie", "business", "3", "Dubbele finaliteit", "", OVERVIEW, "Derde graad, dubbele finaliteit, volgens het studieaanbod-overzicht."),
    ("Onthaal, organisatie & sales", "business", "3", "Arbeidsmarkt", "", OVERVIEW, "Derde graad, arbeidsmarktfinaliteit, volgens het studieaanbod-overzicht. Een duaal traject met een gelijkaardige naam staat apart bij Leren & Werken."),
    ("Welzijnswetenschappen", "care", "3", "Doorstroom", "", OVERVIEW, "Derde graad, doorstroomfinaliteit, volgens het studieaanbod-overzicht."),
    ("Welness & Schoonheid", "care", "3", "Dubbele finaliteit", "", OVERVIEW, "Derde graad, dubbele finaliteit. Spelling zoals op het studieaanbod-overzicht."),
    ("Gezondheidszorg", "care", "3", "Dubbele finaliteit", "", OVERVIEW, "Derde graad, dubbele finaliteit, volgens het studieaanbod-overzicht."),
    ("Opvoeding en begeleiding", "care", "3", "Dubbele finaliteit", "nieuw", OVERVIEW, "Derde graad, dubbele finaliteit. Op het overzicht aangeduid als nieuw."),
    ("Haarverzorging", "care", "3", "Arbeidsmarkt", "", OVERVIEW, "Derde graad, arbeidsmarktfinaliteit, volgens het studieaanbod-overzicht. Een duaal traject Haarverzorging staat apart bij Leren & Werken."),
    ("Basiszorg en ondersteuning", "care", "3", "Arbeidsmarkt", "", OVERVIEW, "Derde graad, arbeidsmarktfinaliteit, volgens het studieaanbod-overzicht."),
    ("Crossmedia", "design", "3", "Dubbele finaliteit", "", OVERVIEW, "Derde graad, dubbele finaliteit, volgens het studieaanbod-overzicht."),
    ("Fotografie", "design", "3", "Dubbele finaliteit", "", OVERVIEW, "Derde graad, dubbele finaliteit, volgens het studieaanbod-overzicht."),
    ("Printmedia", "design", "3", "Arbeidsmarkt", "", OVERVIEW, "Derde graad, arbeidsmarktfinaliteit, volgens het studieaanbod-overzicht."),
    ("Decor, etalage & publiciteit", "design", "3", "Arbeidsmarkt", "", OVERVIEW, "Derde graad, arbeidsmarktfinaliteit, volgens het studieaanbod-overzicht."),
    ("Informatica- en communicatiewetenschappen", "it", "3", "Doorstroom", "", ICW_URL, "Derde graad (5e en 6e jaar), doorstroom, domein IT. De schoolsite noemt als inhoud onder meer softwareontwikkeling, computernetwerken, IoT, algoritmen en programmeren, modelleren en simuleren, informatie- en databeheer, datacommunicatie en computer- en netwerkarchitectuur. Lessentabel: 32 uur."),
    ("Applicatie- en databeheer", "it", "3", "Dubbele finaliteit", "", APP_URL, "Derde graad (5e en 6e jaar), dubbele finaliteit, domein IT. Aangewezen vooropleiding volgens de schoolsite: tweede graad grafische technieken of elektromechanische technieken (met extra programmeren). In het 5e jaar komt elektronica-ICT en Internet of Things aan bod, in het 6e jaar een geïntegreerde proef. Stage: 2 weken per jaar. Lessentabel: 32 uur."),
    ("Biotechnologische en chemische STEM-wetenschappen", "stem", "3", "Doorstroom", "nieuw", OVERVIEW, "Derde graad, doorstroomfinaliteit. Op het overzicht aangeduid als nieuw."),
    ("Technologische wetenschappen en engineering", "stem", "3", "Doorstroom", "", OVERVIEW, "Derde graad, doorstroomfinaliteit, volgens het studieaanbod-overzicht."),
    ("Biotechnologische en chemische technieken", "stem", "3", "Dubbele finaliteit", "", OVERVIEW, "Derde graad, dubbele finaliteit, volgens het studieaanbod-overzicht."),
    ("Elektromechanische technieken", "stem", "3", "Dubbele finaliteit", "", OVERVIEW, "Derde graad, dubbele finaliteit, volgens het studieaanbod-overzicht."),
    ("Auto", "stem", "3", "Arbeidsmarkt", "", OVERVIEW, "Derde graad, arbeidsmarktfinaliteit, volgens het studieaanbod-overzicht."),
    ("Binnenschrijnwerk en interieur (Hout)", "stem", "3", "Arbeidsmarkt", "flex", OVERVIEW, "Derde graad, arbeidsmarktfinaliteit. Op het overzicht gelabeld als FLEX."),
    ("Carrosserie", "stem", "3", "Arbeidsmarkt", "flex", OVERVIEW, "Derde graad, arbeidsmarktfinaliteit. Op het overzicht gelabeld als FLEX."),
    ("Elektrische installaties", "stem", "3", "Arbeidsmarkt", "", OVERVIEW, "Derde graad, arbeidsmarktfinaliteit, volgens het studieaanbod-overzicht."),
    ("Fietsinstallaties", "stem", "3", "Arbeidsmarkt", "", OVERVIEW, "Derde graad, arbeidsmarktfinaliteit, volgens het studieaanbod-overzicht."),
    ("Autobus- en autocarchauffeur", "stem", "7", "7e jaar", "nieuw", OVERVIEW, "Zevende jaar, op het overzicht onder STEM geplaatst en aangeduid als nieuw."),
    ("Elektrotechnicus", "stem", "7", "7e jaar", "", OVERVIEW, "Zevende jaar, op het overzicht onder STEM geplaatst. De duale lijst schrijft ook Electrotechnicus. Of dat dezelfde opleiding is, is [te bevestigen]."),
    ("Polyvalent mecanicien personenwagens en lichte bedrijfsvoertuigen", "stem", "7", "7e jaar", "", OVERVIEW, "Zevende jaar, op het overzicht onder STEM geplaatst. Dezelfde naam staat ook bij de duale specialisatiejaren."),
    ("Spuiter carrosserie", "stem", "7", "7e jaar", "", OVERVIEW, "Zevende jaar, op het overzicht onder STEM geplaatst. Dezelfde naam staat ook bij de duale specialisatiejaren."),
    ("Medewerker winkel", "leren", "2", "Duaal", "", DUAAL_URL, "Duaal traject, 2e graad. Vervolg op de schoolsite: Onthaal, Organisatie en Sales Duaal (3e graad) en Commercieel assistent Duaal (7e specialisatiejaar)."),
    ("Medewerker schilder", "leren", "2", "Duaal", "", DUAAL_URL, "Duaal traject, 2e graad. Vervolg op de schoolsite: Decoratie- en schilderwerken Duaal (3e graad) en Fijnschilder Duaal (7e specialisatiejaar)."),
    ("Medewerker keuken", "leren", "2", "Duaal", "", DUAAL_URL, "Duaal traject, 2e graad. Vervolg op de schoolsite: Restaurant en Keuken Duaal (3e graad)."),
    ("Medewerker fastfood", "leren", "2", "Duaal", "", DUAAL_URL, "Duaal traject, 2e graad, volgens het studieaanbod-overzicht."),
    ("Verpakker", "leren", "2", "Duaal", "", DUAAL_URL, "Duaal traject, 2e graad. Vervolg op de schoolsite: Logistiek Duaal (3e graad)."),
    ("Onthaal, Organisatie en Sales", "leren", "3", "Duaal", "", DUAAL_URL, "Duaal traject, 3e graad, na Medewerker winkel Duaal."),
    ("Decoratie- en schilderwerken", "leren", "3", "Duaal", "", DUAAL_URL, "Duaal traject, 3e graad, na Medewerker schilder Duaal."),
    ("Restaurant en Keuken", "leren", "3", "Duaal", "", DUAAL_URL, "Duaal traject, 3e graad, na Medewerker keuken Duaal."),
    ("Haarverzorging", "leren", "3", "Duaal", "", DUAAL_URL, "Duaal traject, 3e graad. Vervolg op de schoolsite: Kapper-Stylist Duaal (7e specialisatiejaar)."),
    ("Logistiek", "leren", "3", "Duaal", "", DUAAL_URL, "Duaal traject, 3e graad, na Verpakker Duaal."),
    ("Commercieel assistent", "leren", "7", "Duaal", "nieuw", DUAAL_URL, "7e specialisatiejaar, duaal, na Onthaal, Organisatie en Sales Duaal. Op het overzicht ook aangeduid als nieuw."),
    ("Kapper-Stylist", "leren", "7", "Duaal", "nieuw", DUAAL_URL, "7e specialisatiejaar, duaal, na Haarverzorging Duaal. Op het overzicht ook aangeduid als nieuw."),
    ("Fijnschilder", "leren", "7", "Duaal", "nieuw", DUAAL_URL, "7e specialisatiejaar, duaal, na Decoratie- en schilderwerken Duaal. Op het overzicht ook aangeduid als nieuw."),
    ("Verzorgende/Zorgkundige", "leren", "7", "Duaal", "nieuw", OVERVIEW, "7e jaar, in de duale lijst op het overzicht en aangeduid als nieuw. Het domein is op die lijst niet apart benoemd, daarom staat de richting hier bij Leren & Werken. Een vaste plek onder Care is [te bevestigen]."),
    ("Electrotechnicus", "leren", "7", "Duaal", "nieuw", DUAAL_URL, "7e specialisatiejaar, duaal. Spelling Electrotechnicus zoals in de duale lijst. Zie ook Elektrotechnicus bij STEM."),
    ("Spuiter carrosserie", "leren", "7", "Duaal", "nieuw", DUAAL_URL, "7e specialisatiejaar, duaal, volgens de duale lijst."),
    ("Polyvalent mecanicien personenwagens en lichte bedrijfsvoertuigen", "leren", "7", "Duaal", "nieuw", DUAAL_URL, "7e specialisatiejaar, duaal, volgens de duale lijst."),
    ("NXT (schakeljaar)", "nxt", "7", "Hoger onderwijs", "nieuw", OVERVIEW, "7e leerjaar gericht op het hoger onderwijs. Op het overzicht aangeduid als nieuw. Dit is geen domeinrichting."),
    ("A-stroom (1A en 2A)", "level1", "1", "Eerste graad", "", A_URL, "Brede algemene vorming. In 1A modules, in 2A een basisoptie van 5 uur. Na een A-attest in 2A blijven de finaliteiten in de tweede graad open, los van de gekozen basisoptie."),
    ("B-stroom (1B en 2B)", "level1", "1", "Eerste graad", "", B_URL, "Praktijkgerichter, met nadruk op basisvaardigheden. In 2B kies je twee basisopties. Doorstroom hangt af van de gevolgde optie en, waar de school dat schrijft, van de toelatingsklassenraad."),
    ("Onthaaljaar OKAN", "wereld", "1", "Onthaal", "", WERELD_URL, "Onthaaltraject voor anderstalige nieuwkomers in Hasselt en Heusden-Zolder. Focus op Nederlands, zelfredzaamheid en doorstroom, met een vervolgschoolcoach."),
]


def e(text):
    return html.escape(str(text), quote=True)


def ext(url, label):
    return (
        f'<a href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(label)}'
        f'<span class="visually-hidden"> (opent in een nieuw venster)</span></a>'
    )


GRADE_LABEL = {
    "1": "Eerste graad",
    "2": "2e graad",
    "3": "3e graad",
    "7": "7e jaar",
}

DOMAIN_NAME = {d[0]: d[1] for d in DOMAINS}
DOMAIN_NAME["nxt"] = "Schakeljaar"


def programs():
    rows = []
    for name, domain, grade, finality, flags, url, blurb in PROGRAMS:
        rows.append(
            {
                "name": name,
                "domain": domain,
                "grade": grade,
                "finality": finality,
                "flags": flags,
                "url": url,
                "blurb": blurb,
            }
        )
    return rows


def search_blob(p):
    return " ".join(
        [
            p["name"],
            p["finality"],
            p["flags"],
            DOMAIN_NAME.get(p["domain"], ""),
            GRADE_LABEL[p["grade"]],
        ]
    )


def stop_html(p):
    tags = p["finality"]
    if "nieuw" in p["flags"]:
        tags += " · nieuw"
    if "flex" in p["flags"]:
        tags += " · flex"
    return f'''<details class="stop" data-stop="{e(search_blob(p))}">
  <summary>{e(p["name"])} <span class="tag">{e(tags)}</span></summary>
  <div class="panel">
    <p>{e(p["blurb"])}</p>
    <p>{ext(p["url"], "Bekijk de bron op levelx.be")}</p>
  </div>
</details>'''


def column(items, grade):
    headed = [p for p in items if p["grade"] == grade]
    title = {"2": "2e graad", "3": "3e graad", "7": "7e jaar"}[grade]
    if not headed:
        body = '<p class="empty-col">Geen richting in deze kolom op het overzicht.</p>'
    else:
        body = "\n".join(stop_html(p) for p in headed)
    return f'<div class="col"><h4>{title}</h4>{body}</div>'


def domain_block(domain_id, items, intro=""):
    css = domain_id if domain_id in DOMAIN_NAME and domain_id != "nxt" else "stem"
    if domain_id == "nxt":
        css_class = "domain-block"
        style = ' style="--domain:#0B4D3B;--tint:#EEF5EF"'
        title = "7e jaar – schakeljaar"
    else:
        css_class = f"domain-block d-{domain_id}"
        style = ""
        title = DOMAIN_NAME[domain_id]
    if domain_id in ("level1", "wereld", "nxt"):
        cols = "\n".join(stop_html(p) for p in items)
    else:
        cols = f'<div class="cols">{column(items, "2")}{column(items, "3")}{column(items, "7")}</div>'
    note = f"<p>{e(intro)}</p>" if intro else ""
    return f'''<article class="{css_class}" data-domain="{domain_id}" id="{domain_id}"{style}>
  <header><h3>{e(title)}</h3></header>
  {note}
  {cols}
</article>'''


def text_list(groups):
    parts = []
    for domain_id, items in groups:
        lis = []
        for p in items:
            extra = ""
            if "nieuw" in p["flags"]:
                extra += ", nieuw op de schoolsite"
            if "flex" in p["flags"]:
                extra += ", FLEX"
            lis.append(
                f'<li data-stop="{e(search_blob(p))}">{e(GRADE_LABEL[p["grade"]])} · {e(p["name"])} · {e(p["finality"])}{e(extra)}</li>'
            )
        title = "7e jaar – schakeljaar" if domain_id == "nxt" else DOMAIN_NAME[domain_id]
        parts.append(
            f'<section class="text-domain" data-domain="{domain_id}"><h3>{e(title)}</h3><ul>{"".join(lis)}</ul></section>'
        )
    return "\n".join(parts)


NAV = [
    ("studieaanbod/", "Studieaanbod", "studieaanbod"),
    ("inschrijven/", "Inschrijven", "inschrijven"),
    ("onze-school/", "Onze school", "school"),
    ("praktisch/", "Praktisch", "praktisch"),
    ("nieuws/", "Nieuws & agenda", "nieuws"),
    ("contact/", "Contact", "contact"),
]


def asset_version():
    digest = hashlib.sha256()
    for name in ("assets/css/styles.css", "assets/js/main.js"):
        digest.update((ROOT / name).read_bytes())
    return digest.hexdigest()[:10]


def chrome(title, description, depth, active, body):
    root = "../" * depth
    version = asset_version()
    nav_links = []
    for href, label, key in NAV:
        current = ' aria-current="page"' if key == active else ""
        nav_links.append(f'<a href="{root}{href}"{current}>{label}</a>')
    return f'''<!DOCTYPE html>
<html lang="nl-BE">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <link rel="icon" href="{root}assets/img/logo.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;family=Space+Grotesk:wght@500;700&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{root}assets/css/styles.css?v={version}">
</head>
<body>
  <a class="skip" href="#inhoud">Spring naar de inhoud</a>
  <div class="top-stack">
    <p class="demo-banner">Demo — dit is geen officiële website van GO! Next Level X. Niet-geverifieerde gegevens staan tussen [te bevestigen].</p>
    <div class="util-bar">
      <div class="wrap">
        <a href="{root}praktisch/#smartschool">Smartschool</a>
        <a href="{root}praktisch/#mijn-level-x">Mijn Level X</a>
        <a href="{root}werken/">Werken bij Level X</a>
      </div>
    </div>
    <header class="site-header">
      <div class="wrap header-row">
        <a class="logo" href="{root}">
          <img src="{root}assets/img/logo.svg" width="64" height="64" alt="Level X, secundair expertenonderwijs">
        </a>
        <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Menu openen">Menu</button>
        <nav id="site-nav" class="site-nav" aria-label="Hoofdmenu">
          {''.join(nav_links)}
          <a class="nav-extra" href="{root}praktisch/#smartschool">Smartschool</a>
          <a class="nav-extra" href="{root}praktisch/#mijn-level-x">Mijn Level X</a>
          <a class="nav-extra" href="{root}werken/">Werken bij Level X</a>
        </nav>
        <a class="btn btn-primary header-cta" href="{root}inschrijven/">Inschrijven</a>
      </div>
    </header>
  </div>
  <main id="inhoud">
    {body}
  </main>
  <div class="rainbow" role="presentation"></div>
  <footer class="site-footer">
    <div class="wrap footer-grid">
      <div>
        <img class="footer-logo" src="{root}assets/img/logo.svg" width="84" height="84" alt="">
        <p>Level X – secundair expertenonderwijs<br>
        Vildersstraat 3, 3500 Hasselt<br>
        <a href="tel:+3211211010">011 21 10 10</a><br>
        <a href="mailto:info@levelx.be">info@levelx.be</a></p>
      </div>
      <div>
        <h2>Studieaanbod</h2>
        <ul>
          <li><a href="{root}eerste-graad/">Level 1</a></li>
          <li><a href="{root}studieaanbod/#business">Business</a> · <a href="{root}studieaanbod/#care">Care</a> · <a href="{root}studieaanbod/#design">Design</a></li>
          <li><a href="{root}studieaanbod/#it">IT</a> · <a href="{root}studieaanbod/#stem">STEM</a></li>
          <li><a href="{root}studieaanbod/#leren">Leren &amp; Werken</a></li>
          <li><a href="{root}studieaanbod/#wereld">Wereldklas</a></li>
        </ul>
      </div>
      <div>
        <h2>Handige links</h2>
        <ul>
          <li><a href="{root}praktisch/#smartschool">Smartschool</a></li>
          <li><a href="{root}praktisch/#mijn-level-x">Mijn Level X</a></li>
          <li>PaperCut <span class="mark">[te bevestigen]</span></li>
          <li>Pasta2GO <span class="mark">[te bevestigen]</span></li>
          <li><a href="{root}praktisch/#reglement">Schoolreglement</a></li>
        </ul>
      </div>
      <div>
        <h2>Volg ons</h2>
        <ul>
          <li>{ext(FB_URL, "Facebook")}</li>
          <li>Instagram <span class="mark">[te bevestigen]</span></li>
        </ul>
        <h2>Werken bij Level X</h2>
        <ul><li><a href="{root}werken/">Vacatures</a></li></ul>
      </div>
    </div>
    <div class="wrap legal">
      <span>© Level X · Demo-website</span>
      <span><a href="{root}privacy/">Privacy</a> · <a href="{root}privacy/#cookies">Cookies</a> · <a href="{root}toegankelijkheid/">Toegankelijkheid</a></span>
    </div>
  </footer>
  <script src="{root}assets/js/main.js?v={version}"></script>
</body>
</html>
'''


def write(rel, html_doc):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html_doc, encoding="utf-8")
    print("wrote", rel)


def tiles(root_prefix):
    cards = []
    for did, name, badge, text, href in DOMAINS:
        cards.append(f'''<a class="tile d-{did}" href="{root_prefix}{href}">
  <span class="badge">{e(badge)}</span>
  <h3>{e(name)}</h3>
  <p>{e(text)}</p>
  <span class="tile-cta">Ontdek {e(name)} →</span>
</a>''')
    return "\n".join(cards)


def page_hero(crumbs, title, lead):
    return f'''<header class="page-hero">
  <div class="wrap">
    <p class="crumbs">{crumbs}</p>
    <h1>{title}</h1>
    <p class="lead on-dark">{lead}</p>
  </div>
</header>'''


def source_line():
    return f'<p class="source">Bron: {ext(SCHOOL_URL, "levelx.be")}, geraadpleegd op 13 oktober 2026. Cijfers, data en teksten die niet op de schoolsite stonden, zijn gemarkeerd.</p>'


def home():
    lines = [
        ("Business", "business"),
        ("Care", "care"),
        ("Design", "design"),
        ("IT", "it"),
        ("STEM", "stem"),
    ]
    line_html = []
    for label, did in lines:
        line_html.append(f'''<div class="line d-{did}"><strong>{label}</strong><div class="track" aria-hidden="true"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div></div>''')
    body = f'''
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow on-dark">Groene campus · Hasselt</p>
      <h1>Kies jouw level.</h1>
      <p class="lead on-dark">Ontdek je talent, word expert. Level X is secundair expertenonderwijs op een groene campus in Hasselt: acht domeinen, één school, leren tussen bomen en innovatie.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="inschrijven/">Inschrijven →</a>
        <a class="btn btn-ghost" href="nieuws/#agenda">Infomomenten</a>
      </div>
    </div>
    <div class="photo-frame">
      <div class="photo-placeholder" role="img" aria-label="Plaatshouder voor een foto van leerlingen aan het werk">[Foto: leerlingen aan het werk]</div>
    </div>
  </div>
</section>
<section class="section" id="domeinen">
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="eyebrow">Ons studieaanbod</p>
        <h2>Welk domein past bij jou?</h2>
      </div>
      <a class="text-link" href="studieaanbod/">Volledig studieaanbod →</a>
    </div>
    <div class="tile-grid">
      {tiles("")}
    </div>
  </div>
</section>
<section class="section paper" id="metro">
  <div class="wrap metro-teaser">
    <div>
      <p class="eyebrow">Metroplan</p>
      <h2>Jouw route door Level X</h2>
      <p class="lead">Van de eerste graad tot het zevende jaar: in het metroplan zie je per domein welke richtingen je kan volgen.</p>
      <a class="btn btn-dark" href="studieaanbod/#metroplan">Bekijk het metroplan</a>
    </div>
    <div class="metro-card">
      <div class="metro-scale"><span></span><span><span>1e graad</span><span>2e graad</span><span>3e graad</span></span></div>
      {''.join(line_html)}
      <p class="fine">Vereenvoudigde weergave. De lijst met richtingen staat op de pagina Studieaanbod.</p>
    </div>
  </div>
</section>
<section class="section section-campus" id="campus">
  <div class="wrap">
    <p class="eyebrow">Groene campus</p>
    <h2>Leren tussen bomen en innovatie</h2>
    <p class="lead">De school ligt op een campus in Hasselt. Hoe groen die precies is — bomen, oppervlakte, buitenruimte — staat niet op levelx.be. De cijfers hieronder komen uit het ontwerp en zijn niet bevestigd.</p>
    <div class="stats">
      <article class="stat"><b>120+</b><span>[te bevestigen]</span></article>
      <article class="stat"><b>2 ha</b><span>[te bevestigen]</span></article>
      <article class="stat"><b>100%</b><span>[te bevestigen]</span></article>
      <article class="stat"><b>15</b><span>[te bevestigen]</span></article>
    </div>
  </div>
</section>
<section class="section paper" id="nieuws">
  <div class="wrap news-grid">
    <div>
      <p class="eyebrow">Nieuws</p>
      <h2>Wat er leeft op school</h2>
      <div class="cards">
        <a class="card" href="nieuws/#klimaatmobiel">
          <div class="card-media" role="img" aria-label="Plaatshouder voor een foto">[Foto]</div>
          <div class="card-body"><p class="eyebrow">Project · [datum]</p><h3>Klimaatmobiel</h3><p>[Korte inleiding van het nieuwsbericht]</p></div>
        </a>
        <a class="card" href="nieuws/#kortfilmfestival">
          <div class="card-media" role="img" aria-label="Plaatshouder voor een foto">[Foto]</div>
          <div class="card-body"><p class="eyebrow">Design · [datum]</p><h3>Kortfilmfestival</h3><p>[Korte inleiding van het nieuwsbericht]</p></div>
        </a>
        <a class="card" href="nieuws/#stemtaf">
          <div class="card-media" role="img" aria-label="Plaatshouder voor een foto">[Foto]</div>
          <div class="card-body"><p class="eyebrow">STEM · [datum]</p><h3>Limburg STEM't af</h3><p>[Korte inleiding van het nieuwsbericht]</p></div>
        </a>
      </div>
    </div>
    <aside id="agenda">
      <p class="eyebrow">Agenda</p>
      <h2>Binnenkort</h2>
      <a class="agenda-item" href="nieuws/#agenda"><span class="date-badge">[dd]<br>[mmm]</span><span><h3>Infomoment 1e graad</h3><p>[datum] · [uur] · Vildersstraat 3</p></span></a>
      <a class="agenda-item" href="nieuws/#agenda"><span class="date-badge">[dd]<br>[mmm]</span><span><h3>Opendeurdag</h3><p>[datum] · [uur]</p></span></a>
      <a class="agenda-item" href="inschrijven/"><span class="date-badge">[dd]<br>[mmm]</span><span><h3>Start inschrijvingen</h3><p>[datum] · online via aanmeldsysteem</p></span></a>
      <a class="agenda-item" href="nieuws/#agenda"><span class="date-badge">[dd]<br>[mmm]</span><span><h3>Infomoment Wereldklas</h3><p>[datum] · [uur]</p></span></a>
      <p><a class="text-link" href="nieuws/#agenda">Volledige agenda →</a></p>
    </aside>
  </div>
</section>
<section class="cta-band">
  <div class="wrap">
    <h2>Klaar voor het volgende level? Schrijf je in of kom de groene campus bekijken.</h2>
    <div class="cta-actions">
      <a class="btn btn-primary" href="inschrijven/">Inschrijven →</a>
      <a class="btn btn-ghost" href="contact/">Afspraak maken</a>
    </div>
  </div>
</section>'''
    write(
        "index.html",
        chrome(
            "Kies jouw level | Level X Hasselt (demo)",
            "Demo-website van GO! Next Level X in Hasselt: studieaanbod, metroplan en inschrijven. Secundair expertenonderwijs.",
            0,
            "",
            body,
        ),
    )


FILTER_DOMAINS = ["level1", "business", "care", "design", "it", "stem", "leren", "wereld"]


def filter_form():
    chips = ['<button type="button" class="chip" data-filter="alle" aria-pressed="true">Alle</button>']
    for did in FILTER_DOMAINS:
        chips.append(
            f'<button type="button" class="chip d-{did}" data-filter="{did}" aria-pressed="false"><span class="swatch" aria-hidden="true"></span>{e(DOMAIN_NAME[did])}</button>'
        )
    return f'''<form class="tools" data-filter-form role="search">
  <div class="search">
    <label for="q">Zoek een richting</label>
    <input id="q" name="q" type="search" placeholder="Bijvoorbeeld fotografie, duaal, STEM" autocomplete="off">
  </div>
  <div class="filters" role="group" aria-label="Filter op domein">
    {''.join(chips)}
  </div>
  <p id="result-count" class="result-count" aria-live="polite"></p>
</form>
<p id="empty-state" class="note" hidden>Geen richtingen voor deze zoekopdracht. Kies Alle domeinen of een ander woord.</p>'''


def grouped(rows):
    order = ["level1", "business", "care", "design", "it", "stem", "leren", "wereld", "nxt"]
    groups = []
    for did in order:
        items = [p for p in rows if p["domain"] == did]
        if items:
            groups.append((did, items))
    return groups


def studieaanbod():
    rows = programs()
    groups = grouped(rows)
    blocks = []
    intros = {
        "level1": "Kies in de eerste graad A-stroom of B-stroom. De basisopties laten je proeven; ze leggen je keuze voor de tweede graad niet vast zoals een definitieve specialisatie.",
        "business": "Economie, organisatie en ondernemen. De namen hieronder staan zo op het studieaanbod-overzicht.",
        "care": "Zorg, welzijn en werken met mensen.",
        "design": "Creatie, vormgeving en beeld. Op het overzicht staat in de tweede graad geen doorstroomrichting bij Design.",
        "it": "In de tweede graad verwijst de schoolsite naar technologische wetenschappen met extra programmeren. De benoemde IT-richtingen starten in de derde graad.",
        "stem": "Wetenschap, techniek en wiskunde. FLEX is een label van de schoolsite.",
        "leren": "Duaal leren is leren op school én op de werkvloer. Op levelx.be: drie dagen per week in een bedrijf en twee dagen op school. Je kan starten als je 16 bent, of 15 en de eerste graad hebt afgerond.",
        "wereld": "Wereldklas is een onthaaljaar, geen richting van de tweede of derde graad.",
        "nxt": "",
    }
    for did, items in groups:
        if did == "level1":
            continue
        blocks.append(domain_block(did, items, intros.get(did, "")))
    level_items = [p for p in rows if p["domain"] == "level1"]
    body = f'''
{page_hero('<a href="../">Home</a> · Studieaanbod', 'Overzicht van alle richtingen', 'Zoek of filter op domein. Het metroplan en de tekstlijst gebruiken dezelfde gegevens van levelx.be.')}
<div class="content">
  <div class="wrap">
    {filter_form()}
    <section aria-labelledby="level1-titel">
      <p class="eyebrow">1e graad</p>
      <h2 id="level1-titel">Level 1 – basisvorming, kies je stroom</h2>
      {domain_block("level1", level_items, intros["level1"])}
      <p><a class="btn btn-line" href="../eerste-graad/">Naar de eerste graad</a></p>
    </section>
    <section id="metroplan" aria-labelledby="metro-titel">
      <p class="eyebrow">Metroplan</p>
      <h2 id="metro-titel">Van de 2e graad tot het 7e jaar</h2>
      <p class="lead">Elke lijn is een domein. Open een richting voor de finaliteit en de bron. Met het toetsenbord: tab naar een richting en druk op Enter of spatie.</p>
      {''.join(blocks)}
    </section>
    <section id="tekstlijst" aria-labelledby="tekst-titel">
      <h2 id="tekst-titel">Metroplan als tekstlijst</h2>
      <p>Dezelfde richtingen, zonder het visuele plan. Deze lijst blijft bruikbaar als je geen afbeeldingen of kleur ziet.</p>
      {text_list(groups)}
    </section>
    <section>
      <h2>Specialiseer je of bereid je voor op hoger onderwijs</h2>
      <div class="trio">
        <a class="info-card" href="#nxt"><h3>7NXT – schakeljaar</h3><p>7e leerjaar gericht op het hoger onderwijs. Op de schoolsite aangeduid als nieuw.</p></a>
        <a class="info-card" href="#leren"><h3>Leren &amp; Werken / duaal</h3><p>Drie dagen op de werkvloer, twee dagen op school. Trajecten volgens het overzicht.</p></a>
        <a class="info-card" href="#wereld"><h3>Wereldklas</h3><p>Onthaalonderwijs OKAN in Hasselt en Heusden-Zolder.</p></a>
      </div>
    </section>
    <section class="cta-band" style="border-radius:20px;margin-top:2rem">
      <div class="wrap">
        <h2>Twijfel je nog? Kom langs op een infomoment.</h2>
        <div class="cta-actions">
          <a class="btn btn-primary" href="../nieuws/#agenda">Infomomenten</a>
          <a class="btn btn-ghost" href="../contact/">Contact</a>
        </div>
      </div>
    </section>
    {source_line()}
  </div>
</div>'''
    write(
        "studieaanbod/index.html",
        chrome(
            "Studieaanbod | Level X Hasselt (demo)",
            "Overzicht van de richtingen van Level X: eerste tot derde graad, zevende jaar, duaal leren en Wereldklas.",
            1,
            "studieaanbod",
            body,
        ),
    )


A_ROWS = [
    ("Basisvorming", "27", "25"),
    ("Levensbeschouwing", "2", "2"),
    ("Lichamelijke opvoeding", "2", "2"),
    ("Nederlands", "4", "5"),
    ("Engels", "2", "2"),
    ("Frans", "3", "3"),
    ("Geschiedenis inclusief burgerschap", "2", "2"),
    ("Wiskunde", "4", "4"),
    ("Economie", "1", "–"),
    ("Natuurwetenschappen, ruimtelijk bewustzijn en techniek", "5", "5"),
    ("Toegepaste informatica", "1", "–"),
    ("Cultuur", "1", "–"),
    ("Basisoptie (keuze)", "–", "5"),
    ("Business (Economie en organisatie)", "–", "5"),
    ("Care (Maatschappij en welzijn)", "–", "5"),
    ("STEM-IT (STEM-wetenschappen)", "–", "5"),
    ("Design (STEM-technieken)", "–", "5"),
    ("Next Level", "5", "2"),
    ("Modules", "4", "–"),
    ("GoLeLe", "1", "2"),
    ("Totaal", "32", "32"),
]

B_ROWS = [
    ("Basisvorming", "27", "19"),
    ("Levensbeschouwing", "2", "2"),
    ("Lichamelijke opvoeding", "2", "2"),
    ("Project Algemene Vakken", "12", "11"),
    ("Engels", "2", "2"),
    ("Frans", "1", "1"),
    ("Techniek", "5", "–"),
    ("Cultuur", "2", "–"),
    ("Toegepaste informatica", "1", "1"),
    ("Basisoptie (keuze uit 2)", "–", "10"),
    ("Business (Economie en organisatie)", "–", "5"),
    ("Care (Maatschappij en welzijn)", "–", "5"),
    ("STEM (STEM-technieken)", "–", "5"),
    ("Design (Kunst en creatie)", "–", "5"),
    ("Next Level", "5", "3"),
    ("Modules", "4", "–"),
    ("GoLeLe", "1", "3"),
    ("Totaal", "32", "32"),
]


def lesson_table(caption, rows):
    body = []
    for name, a, b in rows:
        if name == "Totaal":
            label = f'<th scope="row">{e(name)}</th>'
        else:
            label = f"<td>{e(name)}</td>"
        body.append(f"<tr>{label}<td>{e(a)}</td><td>{e(b)}</td></tr>")
    # fix invalid: th scope row is fine
    return f'''<table>
  <caption>{e(caption)}</caption>
  <thead><tr><th scope="col">Vak</th><th scope="col">1e jaar</th><th scope="col">2e jaar</th></tr></thead>
  <tbody>{''.join(body)}</tbody>
</table>'''


def eerste_graad():
    body = f'''
{page_hero('<a href="../">Home</a> · <a href="../studieaanbod/">Studieaanbod</a>', 'Eerste graad', 'Level 1 is de brug tussen de basisschool en een richting. Je proeft van het aanbod van de scholen van GO! Next.')}
<div class="content">
  <div class="wrap prose">
    <p>De school ligt op een scholencampus in Hasselt. De studiekeuze wordt uitgesteld tot het eerste jaar van de tweede graad. De school verwijst voor de overstap naar hoger onderwijs naar de nabijheid van hogescholen en Universiteit Hasselt, en naar stageplaatsen en bedrijven in de buurt.</p>
    <p>Coördinator eerste graad: <a href="mailto:level1@levelx.be">level1@levelx.be</a>.</p>
    <div class="stream-grid">
      <article class="info-card" id="a-stroom">
        <h3>A-stroom</h3>
        <p>In 1A verken je leerstrategieën en vakgebieden. In 2A proef je via een basisoptie. Na een A-attest in 2A kan je naar alle studierichtingen in het derde jaar, los van die basisoptie.</p>
        <p>{ext(A_URL, "Officiële pagina A-stroom")}</p>
      </article>
      <article class="info-card" id="b-stroom">
        <h3>B-stroom</h3>
        <p>In de B-stroom leer je vooral door te doen. In 1B werk je aan basisvaardigheden. In 2B kies je twee basisopties. Een getuigschrift 2B opent wegen in de tweede graad; doorstroom naar doorstroom- of dubbele finaliteit heeft voorwaarden.</p>
        <p>{ext(B_URL, "Officiële pagina B-stroom")}</p>
      </article>
    </div>
    <h2>Modules in het eerste jaar</h2>
    <h3>1A</h3>
    <ul>
      <li>Care (Lichaamsverzorging) – kennismaking met verzorgingstechnieken.</li>
      <li>Care (Personenzorg) – zorg en welzijn, sociale vaardigheden en basiszorg.</li>
      <li>Design – creatieve ontwikkeling en ontwerptechnieken.</li>
      <li>Business (Economie) – economie en ondernemerschap.</li>
      <li>IT – digitale vaardigheden en technologie.</li>
      <li>STEM – probleemoplossend denken en wetenschappelijke vaardigheden.</li>
    </ul>
    <h3>1B</h3>
    <ul>
      <li>Care – lichaamsverzorgingstechnieken.</li>
      <li>Care – zorg en welzijn.</li>
      <li>Design – ontwerptechnieken.</li>
      <li>Business – economie en ondernemerschap.</li>
      <li>STEM – technologie, mechanische technieken en constructie.</li>
    </ul>
    <h2>Basisopties in het tweede jaar</h2>
    <p>In 2A kies je één basisoptie van 5 uur: Business, Care, Design of STEM-IT. In 2B kies je twee basisopties van 5 uur: Business, Care, Design of STEM. De uren in de tabellen hieronder zijn de uren van een gekozen optie, niet een som van alle opties samen.</p>
    <h2>Lessentabellen</h2>
    <p>Uren zoals gepubliceerd op levelx.be. In de A-stroom zijn er examens in december en juni. In de B-stroom evalueert de school met permanente evaluatie en is er na het tweede leerjaar een attestering. Elke leerperiode start met een beginsituatie, onder meer tijdens ontmoetingsdagen en een sleep-over, en sluit af met een rapport.</p>
    {lesson_table("Lessentabel eerste graad A-stroom (uren per week)", A_ROWS)}
    {lesson_table("Lessentabel eerste graad B-stroom (uren per week)", B_ROWS)}
    <h2>Aanpak</h2>
    <p>De school werkt in de eerste graad met de ADI-lesmethode (Activerende Directe Instructie): instructie in kleine stappen, meteen oefenen, en differentiëren. Naast de vakken is er het vak GoLeLe en projectwerk. Thema’s die de school noemt: welkomstweek, gezondheid, duurzaamheid, veiligheid en een antipestproject.</p>
    <h2>Op school</h2>
    <ul>
      <li>Eigen plek op de campus. In de B-stroom beschrijft de school een verdiep met lokalen, een polyvalente ruimte en een speelplaats.</li>
      <li>Middagactiviteiten.</li>
      <li>Studiehulpklas, elke middagpauze, en extra studiebegeleiding in de examenperiode.</li>
      <li>Huiskamerklas de K@pstok, voor leerlingen, ouders en leraren.</li>
      <li>Leerlingenraad Think 2, met denktanks.</li>
      <li>Themadagen. De B-stroompagina noemt ontmoetingsdagen, een halloweentocht, een winterfeest, een valentijnfeest en excursies.</li>
    </ul>
    <h2>Na de eerste graad</h2>
    <p>In de tweede graad kies je een finaliteit:</p>
    <ul>
      <li>Doorstroom (D): theoretischer, gericht op hoger onderwijs.</li>
      <li>Dubbele finaliteit (D/A): theorie en praktijk, daarna studeren of werken.</li>
      <li>Arbeidsmarkt (A): praktijk en werkplekleren, gericht op werk na de derde graad.</li>
    </ul>
    <p>Vanuit 2B is arbeidsmarktfinaliteit de rechtstreekse weg. Doorstroom of dubbele finaliteit kan als je de opstroomoptie volgde, of een combinatie met die optie, of met een gunstige beslissing van de toelatingsklassenraad. Die voorwaarden staan zo op de B-stroompagina.</p>
    <p><a class="btn btn-dark" href="../tweede-graad/">Richtingen in de tweede graad</a></p>
    {source_line()}
  </div>
</div>'''
    write(
        "eerste-graad/index.html",
        chrome(
            "Eerste graad | Level X Hasselt (demo)",
            "Level 1 op Level X: A-stroom en B-stroom, modules, basisopties en lessentabellen.",
            1,
            "studieaanbod",
            body,
        ),
    )


def grade_page(rel, grade, title, desc, intro_html, active_note):
    rows = [p for p in programs() if p["grade"] == grade or (grade == "3" and p["grade"] == "7")]
    # For derde graad show grade 3 in the main list and grade 7 in a second section
    if grade == "3":
        main_rows = [p for p in programs() if p["grade"] == "3"]
        extra_rows = [p for p in programs() if p["grade"] == "7"]
    else:
        main_rows = [p for p in programs() if p["grade"] == grade]
        extra_rows = []
    order = ["business", "care", "design", "it", "stem", "leren"]
    sections = []
    for did in order:
        items = [p for p in main_rows if p["domain"] == did]
        if not items:
            continue
        blocks = "\n".join(
            f'''<article class="info-card" id="{e(did)}-{e(p["name"].lower().replace(" ", "-")[:24])}">
  <h3>{e(p["name"])}</h3>
  <p><span class="tag">{e(p["finality"])}</span>{' <span class="tag">nieuw</span>' if 'nieuw' in p['flags'] else ''}{' <span class="tag">flex</span>' if 'flex' in p['flags'] else ''}</p>
  <p>{e(p["blurb"])}</p>
  <p>{ext(p["url"], "Bron op levelx.be")}</p>
</article>'''
            for p in items
        )
        sections.append(f'<h2 id="{did}">{e(DOMAIN_NAME[did])}</h2><div class="stream-grid">{blocks}</div>')
    extra = ""
    if extra_rows:
        extra_cards = "\n".join(
            f'''<article class="info-card"><h3>{e(p["name"])}</h3><p>{e(DOMAIN_NAME.get(p["domain"], p["domain"]))} · {e(p["finality"])}</p><p>{e(p["blurb"])}</p></article>'''
            for p in extra_rows
        )
        extra = f'<h2>Zevende jaar en schakeljaar</h2><p>Deze opleidingen staan op het overzicht bij het zevende jaar of de duale specialisatiejaren. Ze horen niet allemaal bij dezelfde finaliteit als de derde graad.</p><div class="stream-grid">{extra_cards}</div>'
    body = f'''
{page_hero('<a href="../">Home</a> · <a href="../studieaanbod/">Studieaanbod</a>', title, active_note)}
<div class="content"><div class="wrap prose">
  {intro_html}
  {''.join(sections)}
  {extra}
  <p><a class="btn btn-dark" href="../studieaanbod/#metroplan">Open het metroplan</a></p>
  {source_line()}
</div></div>'''
    write(rel, chrome(f"{title} | Level X Hasselt (demo)", desc, 1, "studieaanbod", body))


def tweede():
    grade_page(
        "tweede-graad/index.html",
        "2",
        "Tweede graad",
        "Richtingen van de tweede graad op Level X, per domein en finaliteit.",
        f'''<p>In het derde leerjaar kies je een studierichting in een finaliteit. De namen hieronder komen van het {ext(OVERVIEW, "studieaanbod-overzicht")}.</p>
        <ul>
          <li>Doorstroom: theoretischer, gericht op hoger onderwijs.</li>
          <li>Dubbele finaliteit: theorie en praktijk.</li>
          <li>Arbeidsmarkt: praktijk en werkplekleren.</li>
        </ul>
        <p>IT heeft op dat overzicht in de tweede graad geen eigen richtingnaam. De school verwijst naar technologische wetenschappen met extra programmeren.</p>''',
        "Derde en vierde leerjaar. Finaliteit en domein zoals op levelx.be.",
    )


def derde():
    grade_page(
        "derde-graad/index.html",
        "3",
        "Derde graad",
        "Richtingen van de derde graad en het zevende jaar op Level X.",
        f'''<p>Vijfde en zesde leerjaar, plus het zevende jaar waar de school dat publiceert. Namen volgens het {ext(OVERVIEW, "studieaanbod-overzicht")}.</p>
        <p>Voor Informatica- en communicatiewetenschappen en Applicatie- en databeheer is er een eigen pagina op levelx.be, met lessentabel en leerlingenprofiel. Die details staan bij de richting hieronder, niet herhaald als een volledige tabel.</p>''',
        "Vijfde en zesde leerjaar, en het aanbod van het zevende jaar.",
    )


def simple_page(rel, key, title, desc, crumbs, h1, inner):
    body = f'''{page_hero(crumbs, h1, desc)}
<div class="content"><div class="wrap prose">{inner}{source_line()}</div></div>'''
    write(rel, chrome(f"{title} | Level X Hasselt (demo)", desc, 1, key, body))


def other_pages():
    simple_page(
        "inschrijven/index.html",
        "inschrijven",
        "Inschrijven",
        "Aanmelden voor 1A en 1B, en waar je de actuele vrije plaatsen nakijkt.",
        '<a href="../">Home</a>',
        "Inschrijven",
        f'''<p>Info inschrijvingen: <a href="tel:+3211211010">011 21 10 10</a>. De officiële uitleg staat op {ext(INSCH_URL, "Je kind inschrijven")}.</p>
        <h2>Aanmelden voor 1A en 1B</h2>
        <p>Voor het eerste leerjaar (1A en 1B), ook voor voorrangsgroepen, gebruikt de school een aanmeldsysteem. Zo staat het op de inschrijvingspagina, bijgewerkt op 23 september 2026:</p>
        <ul>
          <li>Aanmeldperiode: 31 maart tot en met 24 april 2026.</li>
          <li>Een ticket verzilveren op school: van 20 mei tot 16 juni 2026.</li>
        </ul>
        <p>Tijdens de zomervakantie gelden andere openingsuren. Die uren staan niet op de contactpagina uitgeschreven; kijk op de inschrijvingspagina. <span class="mark">[te bevestigen]</span> welke uren dan precies gelden.</p>
        <h2>Vrije plaatsen</h2>
        <p>De school publiceert een statusoverzicht per richting, met vermeldingen zoals volzet. Dat overzicht verandert. Deze demo kopieert die status niet, omdat een momentopname snel fout is. Kijk op de officiële pagina.</p>
        <p>Vragen over het aanmelden via de stad: Dienst Flankerend Onderwijsbeleid, <span class="mark">[e-mailadres op de schoolsite, hier niet overgenomen omdat het in de bron afgeschermd was]</span>, 011 23 90 62 tijdens de kantooruren.</p>
        <p><a class="btn btn-primary" href="{e(INSCH_URL)}">Naar de officiële inschrijvingspagina</a></p>''',
    )
    simple_page(
        "onze-school/index.html",
        "school",
        "Onze school",
        "GO! Next Level X in Hasselt: campus, begeleiding en projecten die de school zelf noemt.",
        '<a href="../">Home</a>',
        "Onze school",
        f'''<p>Level X is secundair expertenonderwijs van scholengroep GO! Next, campus Hasselt, Vildersstraat 3, 3500 Hasselt. De eerste graad beschrijft de school als deel van een scholencampus waar leerlingen het aanbod van de GO! Next-scholen leren kennen.</p>
        <h2>Begeleiding</h2>
        <ul>
          <li>Coördinator eerste graad: <a href="mailto:level1@levelx.be">level1@levelx.be</a>.</li>
          <li>Studiehulpklas tijdens de middagpauze.</li>
          <li>Huiskamerklas de K@pstok.</li>
          <li>Leerlingenraad Think 2.</li>
          <li>In de Wereldklas: een vervolgschoolcoach. De school noemt Kenneth Driesen als coördinator vervolgschoolcoaching. Zijn e-mailadres stond afgeschermd op de pagina en is hier <span class="mark">[te bevestigen]</span>.</li>
        </ul>
        <h2>Projecten</h2>
        <p>Deze namen staan in het menu van levelx.be. Een beschrijving per project is op die menupunten niet in deze demo overgenomen: <span class="mark">[te bevestigen]</span>.</p>
        <ul>
          <li>Klimaatmobiel</li>
          <li>Kortfilmfestival</li>
          <li>Limburg STEM't af</li>
          <li>STEM-koffer</li>
          <li>X-LAN</li>
          <li>Struikelstenen</li>
          <li>K@pstok</li>
        </ul>
        <h2>Visie</h2>
        <p>De pagina Ons DNA op de officiële site is hier niet overgenomen. <span class="mark">[te bevestigen]</span> als je een korte missietekst wil die de school zelf ondertekent.</p>
        <p>Internaat en internationalisering staan in het menu van de officiële site. Details: <span class="mark">[te bevestigen]</span>.</p>''',
    )
    simple_page(
        "praktisch/index.html",
        "praktisch",
        "Praktisch",
        "Smartschool, bereikbaarheid en wat nog bevestigd moet worden.",
        '<a href="../">Home</a>',
        "Praktisch",
        f'''<h2 id="smartschool">Smartschool</h2>
        <p>Ouders volgen activiteiten, resultaten (skore) en gedrag via Smartschool, in de browser of via de app. Je kan laten mailen wanneer er iets nieuws is. Vragen: <a href="mailto:smartschool@levelx.be">smartschool@levelx.be</a>. Bron: {ext(OUDERS_URL, "Informatie voor ouders")}.</p>
        <p>Het loginadres van Smartschool is <span class="mark">[te bevestigen]</span>. Deze demo linkt daarom niet naar een gegokt portaal.</p>
        <h2 id="mijn-level-x">Mijn Level X</h2>
        <p>De officiële site noemt Mijn Level X als snelle link. De URL is <span class="mark">[te bevestigen]</span>.</p>
        <h2 id="uren">Schooluren</h2>
        <p>Telefonisch is de school bereikbaar van maandag tot vrijdag, van 8 uur tot 16.30 uur. Het lesrooster is <span class="mark">[te bevestigen]</span>.</p>
        <h2 id="reglement">Schoolreglement</h2>
        <p>Het reglement staat op de officiële site. Een rechtstreekse URL is in deze demo <span class="mark">[te bevestigen]</span>. Laptopafspraken staan wel op {ext("https://www.levelx.be/schoollaptop", "Schoollaptop")}: een eigen toestel mag, als het minstens voldoet aan het basistoestel van partner Signpost en werkt met Smartschool en Office 365. Vragen: <a href="mailto:ict@levelx.be">ict@levelx.be</a>.</p>
        <h2>Andere diensten</h2>
        <p>PaperCut en Pasta2GO staan als handige links op de officiële site. URL’s: <span class="mark">[te bevestigen]</span>.</p>''',
    )
    simple_page(
        "nieuws/index.html",
        "nieuws",
        "Nieuws en agenda",
        "Projecten van de school en afspraken waarvan de datum nog niet bevestigd is.",
        '<a href="../">Home</a>',
        "Nieuws en agenda",
        '''<p>De officiële site had op 13 oktober 2026 geen nieuwsfeed die we hier konden overnemen. Onderstaande namen zijn projecten uit het menu. Datums en aankondigingen zijn bewust leeg.</p>
        <article class="info-card" id="klimaatmobiel"><h3>Klimaatmobiel</h3><p class="eyebrow">Project · [datum]</p><p>[Korte inleiding van het nieuwsbericht] <span class="mark">[te bevestigen]</span></p></article>
        <article class="info-card" id="kortfilmfestival"><h3>Kortfilmfestival</h3><p class="eyebrow">Design · [datum]</p><p>[Korte inleiding van het nieuwsbericht] <span class="mark">[te bevestigen]</span></p></article>
        <article class="info-card" id="stemtaf"><h3>Limburg STEM't af</h3><p class="eyebrow">STEM · [datum]</p><p>[Korte inleiding van het nieuwsbericht] <span class="mark">[te bevestigen]</span></p></article>
        <h2 id="agenda">Agenda</h2>
        <ul>
          <li>Infomoment 1e graad — [datum] · [uur] · Vildersstraat 3</li>
          <li>Opendeurdag — [datum] · [uur]</li>
          <li>Start inschrijvingen — voor 1A/1B staat de aanmeldperiode van 2026 op de <a href="../inschrijven/">inschrijvingspagina</a></li>
          <li>Infomoment Wereldklas — [datum] · [uur]</li>
        </ul>
        <p>Oudere pagina’s op levelx.be noemden opendeurdagen op 15 maart en 10 mei zonder jaartal. Die data zijn niet herhaald, omdat niet duidelijk is of ze nog kloppen.</p>''',
    )
    simple_page(
        "contact/index.html",
        "contact",
        "Contact",
        "Adres, telefoon en CLB van GO! Next Level X.",
        '<a href="../">Home</a>',
        "Contact",
        f'''<h2>GO! Next Level X</h2>
        <ul class="contact-list">
          <li>Vildersstraat 3 en 28, 3500 Hasselt</li>
          <li><a href="tel:+3211211010">011 21 10 10</a></li>
          <li><a href="mailto:info@levelx.be">info@levelx.be</a></li>
          <li>Telefonisch bereikbaar van maandag tot vrijdag, van 8 uur tot 16.30 uur.</li>
        </ul>
        <p>De footer van deze demo gebruikt Vildersstraat 3, zoals op de campustekst. De contactpagina schrijft “Vildersstraat 3 en 28”.</p>
        <p><a href="https://www.google.com/maps/search/?api=1&amp;query=Vildersstraat+3+3500+Hasselt">Route in Google Maps<span class="visually-hidden"> (opent in een nieuw venster)</span></a></p>
        <h2>Wereldklas</h2>
        <ul>
          <li>Campus Hasselt: Vildersstraat 3, 3500 Hasselt. Aanspreekpunt: Ianto Elen, 011 21 10 10. E-mail: <span class="mark">[te bevestigen]</span>.</li>
          <li>Campus Heusden-Zolder: Kortstraat 19, 3550 Heusden-Zolder. Campusverantwoordelijke: Tina Peetermans, 011 42 53 28.</li>
        </ul>
        <p>{ext(WERELD_URL, "Pagina Wereldklas")}</p>
        <h2>CLB</h2>
        <ul>
          <li>Vestigingsplaats secundair en buitengewoon secundair onderwijs</li>
          <li>Gazometerstraat 4A, 3500 Hasselt</li>
          <li><a href="tel:+3211221738">011 22 17 38</a></li>
          <li><a href="mailto:directie@clbgohasselt.be">directie@clbgohasselt.be</a></li>
        </ul>
        <p>{ext(CONTACT_URL, "Officiële contactpagina")}</p>
        <h2>Afspraak</h2>
        <p>Een online afsprakenmodule is <span class="mark">[te bevestigen]</span>. Bel 011 21 10 10 of mail info@levelx.be.</p>''',
    )
    simple_page(
        "werken/index.html",
        "",
        "Werken bij Level X",
        "Vacatures: de exacte pagina is nog niet bevestigd.",
        '<a href="../">Home</a>',
        "Werken bij Level X",
        f'''<p>De officiële site heeft een onderdeel Jobs, met spontane sollicitatie en een VDAB-vacature. De rechtstreekse URL is <span class="mark">[te bevestigen]</span>.</p>
        <p>Tot dan: {ext(SCHOOL_URL, "levelx.be")} of <a href="mailto:info@levelx.be">info@levelx.be</a>, telefoon 011 21 10 10.</p>''',
    )
    simple_page(
        "toegankelijkheid/index.html",
        "",
        "Toegankelijkheid",
        "Wat deze demo doet voor toetsenbord, taal en contrast.",
        '<a href="../">Home</a>',
        "Toegankelijkheid",
        '''<ul>
          <li>Taal van de pagina: nl-BE.</li>
          <li>Skiplink naar de inhoud, semantische koppen, één h1 per pagina.</li>
          <li>Menu knop met aria-expanded. Sluiten kan met Escape.</li>
          <li>Zoeken en filteren op het studieaanbod werkt met het toetsenbord. Het aantal resultaten staat in een live region.</li>
          <li>Elke richting is een disclosure (details/summary), ook zonder extra script. Daaronder staat het metroplan als tekstlijst.</li>
          <li>De grote vlakken zijn wit, zachtgroen (#EEF5EF / #E3F0E6) of diepgroen (#0B4D3B). Antraciet (#1F2421) is voor tekst. Wit en #E3F0E6 op #0B4D3B halen WCAG AA. De focusrand is diepgroen op lichte vlakken en amber op diepgroene knoppen en in de footer.</li>
          <li>Op de badge van Business (#E8584C) staat zwarte tekst, omdat antraciet daar op 4,45:1 blijft en nét onder AA voor kleine tekst zit.</li>
          <li>Logo heeft een tekstalternatief. Fotoplekken zijn benoemde plaatshouders, geen decoratieve lege beelden.</li>
          <li>Beweging is uit als je in het systeem verminderde beweging vraagt.</li>
        </ul>
        <p>Een volledige audit is niet gebeurd. <span class="mark">[te bevestigen]</span> na een test met screenreader op de echte inhoud.</p>''',
    )
    simple_page(
        "privacy/index.html",
        "",
        "Privacy",
        "Deze demo plaatst zelf geen cookies en stuurt geen formulier naar een server.",
        '<a href="../">Home</a>',
        "Privacy",
        '''<p>De demo is statische HTML. Er is geen account, geen formulier dat gegevens bewaart, en geen eigen cookie.</p>
        <h2 id="cookies">Cookies en lettertypen</h2>
        <p>De pagina laadt Space Grotesk en Inter via Google Fonts. Daarbij kan je browser contact maken met Google. Er is geen cookiebanner, omdat de demo zelf geen volgcookies zet. Wie dat verzoek wil vermijden, kan de lettertypen later lokaal hosten.</p>
        <p>Externe links naar levelx.be, Facebook en Google Maps vallen onder het beleid van die sites.</p>''',
    )


def not_found():
    body = '''<header class="page-hero"><div class="wrap"><h1>Pagina niet gevonden</h1><p class="lead on-dark">Deze demo heeft geen pagina op dit adres.</p><p><a class="btn btn-primary" href="./">Naar de start</a></p></div></header>'''
    write(
        "404.html",
        chrome("Pagina niet gevonden | Level X demo", "Deze pagina bestaat niet in de demo.", 0, "", body),
    )


def main():
    home()
    studieaanbod()
    eerste_graad()
    tweede()
    derde()
    other_pages()
    not_found()
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    print("done")


if __name__ == "__main__":
    main()
