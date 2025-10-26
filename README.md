# Axiomatic Intelligence — GitHub repozitár
Repozitár implementuje Axiomatickú Inteligenciu (verzia 4.0) — ontologicko-etický rámec + skripty pre výpočty AAV, Bayes/gradient aktualizácie a Merkle anchoring. Dokumentácia a CSV šablóny sú založené na "Axiomatic Intelligence 4.0" (Richard Fonfára, 2025). 3

## Quickstart
1. git clone <this-repo>
2. python -m venv venv && source venv/bin/activate
3. pip install -r requirements.txt
4. python scripts/aav_calc.py --weights config/weights.json --scores data/rozhodnutia.csv

## Obsah
- scripts/: základné skripty (aav_calc, bayes_update, gd_update, merkle_anchor). 4
- data/: CSV šablóny pre axiomy a rozhodnutia. 5
- docs/: governance, REP7 protokol, hard-gate definície. 6

## Licencia
Tento projekt používa CC BY-SA 4.0 s doplnkovými podmienkami uvedenými v dokumente. (Pozri LICENSE.md). 7
