# CONTRIBUTING — Axiomatic Intelligence (Hexagramon)

Ďakujeme, že chceš prispieť. Tento dokument popisuje jasné pravidlá, workflow a očakávania pri prispievaní do repozitára. Povedzme veci na rovinu: prispievanie musí byť predvídateľné, zodpovedné a auditovateľné.

## Základné princípy
- Prispievame s úmyslom zachovať a rozvíjať život a vedomie (Axiom 0).  
- Pri každom pridaní kódu alebo dokumentu očakávame rešpekt k pravde, reprodukovateľnosť a testovateľnosť.  
- Transparentnosť je povinná — každý krok musí byť zrozumiteľný pre audítora.

## Ako začať (rýchlo)
1. Forkni repozitár.
2. `git clone` svoj fork.
3. Vytvor feature branch: `feature/<krátky-popis>` alebo bugfix branch: `bugfix/<krátky-popis>`.
4. Vyvíjaj lokálne, bež testy a linting.
5. Otvor PR do hlavnej vetvy (default branch: `main`).

## Naming konvencie vetiev
- Funkcie: `feature/<krátky-hyphen-case-popis>`
- Opravy: `bugfix/<krátky-popis>`
- Hotfix: `hotfix/<popis>`
- Dokumentácia: `docs/<popis>`
- Experimenty: `exp/<popis>` (neslúži na dlhodobé ukladanie — používať obozretne)

## Commit message štýl
Používame imperatívny, stručný štýl:
Príklady:
- `aav: add basic aggregator and tests`
- `docs(readme): add quickstart example`

Sign-off:
- Pri produktoch s právnymi alebo auditnými požiadavkami pridaj `Signed-off-by: <meno> <email>` v prípade potreby (DCO).

## Pull request workflow
- Otvor PR, priraď aspoň jednu relevantnú osobu (core custodian alebo maintainer).
- PR musí obsahovať:
  - Popis zmeny a dôvod.
  - Link na súvisiace issue (ak existuje).
  - Výsledky testov alebo screenshoty chýb (pre UI).
  - Záznamy o bezpečnostnom posúdení, ak zmena ovplyvňuje bezpečnosť.
- Minimálne 1 schválenie od maintainer-u pred merge (preferované 2, ak ide o významnú zmenu).
- Merge len cez `merge pull request` s čistou históriou (squash/merge podľa dohody).

## Testy a kvalita kódu
- Každý feature musí mať unit testy pokrývajúce kritické cesty.
- Integračné testy pre zložitejšie moduly.
- Používame `pytest`. Spusti testy: `pytest`
- Kód: formátuj pomocou `black` a kontroluj pomocou `flake8`.
- Pre lokálnu kontrolu:
  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  pre-commit install
  pre-commit run --all-files
  pytest -q
