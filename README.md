# Axiomatic Intelligence — Axiom Engine (Supplementary Files)

Tento repozitár obsahuje podporne súbory pre článok a technický dodatok k Axiomatickej inteligencii (v4.0).
Obsahuje príklady skriptov, markdown manuály, licenciu AEPL-1.0 a jednoduché nástroje pre anchoring a validáciu.

Súbory:
- `manual_article.md` — Hlavný článok / manuál (upravený, publikovateľný).
- `manual_addendum.md` — Technický dodatok: AI-assisted scoring & Execution Guard.
- `ai_pipeline.py` — Pipeline pre AI scoring (featurize, embed, scorer, calibrator, logging).
- `compute_aav.py` — Výpočet AAV (Aggregated Axiom Value).
- `train_calibration.py` — Tréning kalibrátora (isotonic / platt).
- `execution_guard.py` — Execution Guard stub (validátory a blokovanie exekúcie).
- `anchor.py` — Jednoduchý Merkle root helper.
- `AEPL-1.0.md` — Licencia AEPL-1.0 (Axiomatic Ethical Public License).
- `requirements.txt` — Základné Python závislosti.
- `.gitignore` — odporúčané ignorovanie lokálnych súborov.

Poznámka: súbory sú pripravené ako štartovací bod. Pred produkčným nasadením vykonaj code review, security audit a naplno otestuj v shadow-mode.
