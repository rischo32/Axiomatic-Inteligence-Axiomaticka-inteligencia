---

# 2) `ISSUE_TEMPLATE.md` (umiestnenie: `.github/ISSUE_TEMPLATE/ISSUE_TEMPLATE.md` alebo `ISSUE_TEMPLATE.md`)

```markdown
<!--
Vyber typ issue: BUG alebo FEATURE. Vyplň čo najkonkrétnejšie.
-->

# Typ
- [ ] BUG
- [ ] FEATURE
- [ ] DOCUMENTATION
- [ ] SECURITY (kontaktuj security@tvoj-email najprv)

---

## Stručný názov
Krátky a výstižný titulok (max 80 znakov)

## Popis
Popíš problém alebo požiadavku jedným-dvoma vetami.

## Krok(y) na reprodukciu (pre bug)
1. Popis kroku 1
2. Popis kroku 2
3. Spustenie príkazu, očakávaný výstup vs. skutočný výstup

### Očakávané správanie
Čo malo nastať.

### Skutočné správanie
Čo sa stalo namiesto toho (prilož logy / stack trace).

### Prostredie
- OS: (napr. Ubuntu 22.04)
- Python: (napr. 3.10.12)
- Verzia repozitára / commit: (hash)
- Iné relevantné knižnice: (pip freeze prípadne requirements.txt)

### Prílohy
- Logy (vložiť ako súbor)
- Screenshoty

## Návrh riešenia (pre feature)
- Konkrétny návrh: čo sa má pridať, API, návrh dátovej štruktúry.
- Dôvod a prínos.
- Alternatívy, ak existujú.

---

Ďakujeme. Ak ide o bezpečnostný problém, pozri sekciu SECURITY v CONTRIBUTING.
