# Axiomatická Inteligencia (Axiomatic Intelligence)

Ontologicko-etický rámec pre ľudí a AI systémy založený na siedmich princípoch: Existencia – Múdrosť – Vzájomnosť – Pravda – Sloboda – Jednota – Tvorba.

## Popis
Tento projekt implementuje systém Axiomatickej Inteligencie (verzia 4.0), vrátane metrík, váh, agregátorov, Python skriptov na výpočty a CSV šablón. Cieľom je poskytnúť etický kompas pre rozhodovanie v AI, organizáciách a osobnom živote.

### Kľúčové komponenty
- **Princípy a axiomy**: Definované v `docs/axiomy.md`.
- **Metriky a indexy**: Popísané v `docs/metriky.md`.
- **Python skripty**: V priečinku `src/` na výpočet AAV, Bayesovské aktualizácie, gradient descent a Merkle anchoring.
- **CSV šablóny**: V priečinku `data/` na axiómy a rozhodnutia.
- **Governance**: Core Custodian Council (CCC) a protokoly v `docs/governance.md`.
- **Licencia**: Založená na CC BY-SA 4.0 s obmedzeniami core princípov (viď LICENSE).

## Inštalácia
1. Nainštaluj závislosti: `pip install numpy scipy hashlib json`.
2. Spusti skripty, napr. `python src/aav_calc.py`.

## Príklady použitia
- Výpočet AAV: Nahraj dáta do `data/rozhodnutia.csv` a spusti `src/aav_calc.py`.
- Aktualizácia váh: Použi `src/bayes_update.py` alebo `src/gd_update.py`.

## Autor
Richard Fonfára, 2025. Vytvorené s pomocou AI nástrojov (ChatGPT, Copilot, DeepSeek, Grok).

Licencia: CC BY-SA 4.0 s obmedzeniami (viď LICENSE).
