# Popis zmien
(Stručne zhrň, čo PR rieši - jeden až tri odstavce.)

## Typ zmeny
- [ ] Bugfix
- [ ] Feature
- [ ] Documentation
- [ ] Tests
- [ ] Refactor
- [ ] CI / Workflow

## Súvisiace issue
- Closes: #<issue-number> (ak relevantné)

## Zmeny (čo je zahrnuté)
- Bod 1: (popis)
- Bod 2: (popis)
- Skripty / nové súbory:
  - `src/...`
  - `docs/...`

## Ako to lokálne otestovať
1. Vytvoriť virtuálne prostredie:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
2. Spustiť testy:

pytest -q


3. Spustiť linting:

pre-commit run --all-files



Checklist pred merge

[ ] PR má jasný popis a dôvod

[ ] Pridané/aktualizované testy (ak relevantné)

[ ] Všetky testy prechádzajú (pytest)

[ ] Kód formátovaný (black) a bez lint errorov (flake8)

[ ] Aktualizované dokumenty (README / docs)

[ ] CHANGELOG.md doplnený (krátky zápis)

[ ] Bezpečnostné dôsledky zvážené (ak relevantné)

[ ] Commity podpísané alebo obsahujú Signed-off-by (ak to organizácia vyžaduje)


Reviewer notes

Zvláštne body, ktorým treba venovať pozornosť:

(napríklad: bezpečnostné limity, zmeny v API, migrácie dát)
