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

Zodpovednosť

Podpisom tejto zmeny potvrdzujem, že príspevok dodržiava licenčné pravidlá projektu.

---

# 4) CI workflow — `.github/workflows/ci.yml` (umiestnenie: `.github/workflows/ci.yml`)

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test-and-lint:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.10, 3.11]
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Cache pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Install pre-commit (for hooks)
        run: |
          pip install pre-commit
          pre-commit --version

      - name: Run pre-commit hooks
        run: pre-commit run --all-files

      - name: Lint (flake8)
        run: |
          flake8 .

      - name: Check formatting (black)
        run: |
          black --check .

      - name: Run tests
        run: |
          pytest -q
