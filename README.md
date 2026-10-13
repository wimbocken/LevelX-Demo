# Level X — demo (Richting A, Next Level)

Statische demo van een website voor **GO! Next Level X** (secundair expertenonderwijs, Hasselt), in het Nederlands (nl-BE). Dit is geen officiële site. De inhoud komt van [levelx.be](https://www.levelx.be/) (geraadpleegd op 13 oktober 2026). Wat daar niet te controleren was, staat als `[te bevestigen]` of `[datum]`.

## Pagina’s

- Home
- Studieaanbod, met zoeken, filter per domein, metroplan en dezelfde lijst als tekst
- Eerste graad, tweede graad, derde graad
- Inschrijven, Onze school, Praktisch, Nieuws en agenda, Contact
- Werken bij Level X, privacy, toegankelijkheid

Open `docs/index.html` of start een lokale server:

```bash
python3 -m http.server 8765 --directory docs
```

Daarna: http://127.0.0.1:8765/

## Opnieuw genereren

De HTML in `docs/` wordt gemaakt door `scripts/build.py` (logo, CSS en JS staan los).

```bash
python3 scripts/build.py
```

## GitHub Pages

Kies **één** manier. Niet allebei tegelijk.

### A. GitHub Actions (workflow in deze repo)

1. Merge deze branch naar `main`.
2. Ga in de GitHub-repo naar **Settings → Pages**.
3. Bij **Build and deployment** zet je **Source** op **GitHub Actions**.
4. De workflow `.github/workflows/pages.yml` publiceert de map `docs/` bij elke push naar `main`.
5. De site staat daarna op `https://<gebruiker>.github.io/LevelX-Demo/`.

### B. Zonder Actions, rechtstreeks uit de branch

1. Merge naar `main`.
2. **Settings → Pages → Build and deployment → Source: Deploy from a branch**.
3. Branch: `main`, map: `/docs`.
4. Sla op. GitHub negeert Jekyll dankzij `docs/.nojekyll`.

Alle links zijn relatief, zodat de site werkt als project-site (`/LevelX-Demo/`) en lokaal.
