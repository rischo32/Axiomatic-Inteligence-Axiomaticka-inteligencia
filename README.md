# Axiomatic Intelligence (Axiomatická Inteligencia)

Ontologicko-etický rámec pre ľudí a AI systémy založený na siedmich princípoch: Zámer – Existencia – Múdrosť – Vzájomnosť – Pravda – Sloboda – Jednota – Tvorba.

## Popis
Tento projekt implementuje systém Axiomatickej Inteligencie (verzia 4.0, október 2025), vrátane metrík, indexov (HIS-7), governance (Core Custodian Council), Python skriptov na výpočty (AAV, Bayesovské aktualizácie, gradient descent, Merkle anchoring), CSV šablón a blockchain integrácie. Cieľom je poskytnúť etický kompas pre rozhodovanie v AI, organizáciách a osobnom živote. Systém je cyklicko-evolučný s revíziou (REP7) a adaptáciou váh.

### Quickstart
1. `git clone https://github.com/Rischo32/Axiomatic-Inteligence-Axiomaticka-inteligencia.git`
2. `cd Axiomatic-Inteligence-Axiomaticka-inteligencia`
3. `pip install -r requirements.txt`
4. `python src/aav_calc.py --input data/rozhodnutia.csv`

#### Kľúčové komponenty
- **Princípy a axiomy**: Definované v `docs/axiomy.md` (vrátane heptagramu, verzie Ž a rozšírenia na 32 axiómov).
- **Metriky a indexy**: Popísané v `docs/metriky.md` (napr. INT, LEX, WIS... s prahovými hodnotami T_n).
- **Python skripty**: V priečinku `src/` na výpočet AAV/HEXA7, aktualizácie váh a anchoring.
- **CSV šablóny**: V priečinku `data/` na axiomy, rozhodnutia a metriky.
- **Governance**: Core Custodian Council (CCC) a protokoly v `docs/governance.md`.
- **Licencia**: Založená na CC BY-SA 4.0 s obmedzeniami core princípov (viď LICENSE).

## Inštalácia
1. Nainštaluj závislosti: `pip install numpy pandas scipy hashlib json`.
2. Spusti skripty, napr. `python src/aav_calc.py`.

## Príklady použitia
- Výpočet AAV/HEXA7: Nahraj dáta do `data/rozhodnutia.csv` a spusti `src/aav_calc.py`.
- Aktualizácia váh: Použi `src/bayes_update.py` alebo `src/gd_update.py`.
- Merkle anchoring: Spusti `src/merkle_anchor.py` pre integritu logov.

## Autor
Richard Fonfára, 2025. Vytvorené s pomocou AI nástrojov (ChatGPT, Copilot, DeepSeek, Grok).

Licencia: CC BY-SA 4.0 s obmedzeniami (viď LICENSE).
