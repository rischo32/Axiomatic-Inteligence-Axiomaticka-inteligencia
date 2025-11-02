# Technický dodatok k Axiomatickej inteligencii — AI asistent a Execution Guard

**Autor:** Richard  
**Verzia:** 4.0 — dodatok (2025)

## Stručné zhrnutie
Tento dokument rozširuje Axiomatickú inteligenciu o dve prevádzkové vrstvy:
1. **AI asistent** — featurizácia, embedding, ľahký scorer, kalibrácia a explainability pre výpočet ai_score a podporu rozhodovania.
2. **Execution Guard** — nezávislý validačný modul, ktorý blokuje vykonanie návrhov (aj tých od CCC), ak niektorý BLOCKING validator označí návrh za neakceptovateľný.

Zásada: systém môže odporučiť, nie rozhodovať ľudsky škodlivo. Ak Execution Guard zablokuje návrh, exekúcia sa neuskutoční bez explicitnej opravy a re-submission.

## AI asistent — architektúra a vstupy
- **Ingest**: canonical JSON decision_record (podpísaný).
- **Featurizer**: AAV, SAP, delta trend, embeddings(reason), external indicators.
- **Encoder**: sentence/paragraph embeddings (self-hosted / all-MiniLM).
- **Scorer**: logistická regresia alebo malé MLP -> ai_score ∈ [0,1].
- **Calibrator**: isotonic / Platt scaling.
- **Explainer**: SHAP-lite top-k features, plus LLM-based short explanation ako doplnok.

### Kombinovanie skórov
```
final_score = alpha * AAV + (1 - alpha) * ai_score
```
Alpha môže byť konštantné (0.7) alebo adaptívne podľa konfidencie AI.

## Execution Guard — validátory (príklady)
- **Axiomatic validator (BLOCKING)** — MIN_AAV, hard-gates (INT, LEX).
- **AI risk validator (BLOCKING/ADVISORY)** — final_score, ai_score a explainability.
- **Simulation validator (BLOCKING)** — counterfactual simulácie, fail_rate threshold.
- **SEK validator (BLOCKING)** — estimate external reparations cost.
- **Compliance validator (BLOCKING)** — právne/regulačné obmedzenia.
- **Anomaly detector (ADVISORY)** — flagovanie neobvyklých rozhodnutí.

Prednastavené príkladné prahy:
- MIN_AAV_FOR_EXECUTION = 0.65
- MIN_FINAL_SCORE = 0.60
- AI_BLOCK_THRESHOLD = 0.40
- SEK_MAX_ALLOWED = 0.30
- SIM_FAIL_RATE_MAX = 0.25
- CCC_OVERRIDE_SUPERMAJ = 0.90 + delay 72h

## Proces exekúcie (skrátene)
1. Decision_record vytvorí actor (CCC alebo iný) a podpíše ho.
2. Vstup ide do AI pipeline -> ai_score, explainability.
3. Výstupy idú do Execution Guard -> run validators.
4. Ak všetko OK -> exekúcia (atomic tx) -> log -> Merkle anchoring.
5. Ak blok -> block_record, anchoring, notifikácia + návrh nápravy.

## Audit a anchoring
- Canonical JSON každého kroku.
- SHA-256 hash per record uložený v logdir.
- Batch Merkle root anchoring on-chain (len root).
- Store model & calibrator hashes for provenance.

## Shadow-mode a pilot
- Nasadiť Execution Guard v režime log-only (shadow) 1–3 mesiace.
- Pilot 3 mesiace offline scoring + manuálna verifikácia.
- Red-team a externý audit.

## Záver
Tento dodatok definuje bezpečnostné a technické prvky, ktoré znižujú riziko vykonania škodlivých rozhodnutí. Implementovať s dôrazom na provenance, testovanie a transparentnú komunikáciu.
