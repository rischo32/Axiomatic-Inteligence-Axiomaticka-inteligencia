# Auditný checklist — REP7 / zmeny váh / core changes

**Meta**
- Audit ID: audit-YYYYMMDD-XXXX
- Dátum: YYYY-MM-DD
- Auditor: <meno/ID>

**Kontrola dát a provenance**
- [ ] CSV/JSONL dátové súbory existujú v `data/` a majú správne hlavičky.
- [ ] Zdroje dát uvedené (source links, snapshots) a overiteľné.
- [ ] Merkle leaf pre každý záznam vygenerovaný a uložený.

**Kontrola kódu**
- [ ] Test-suite prešiel (pytest) + výsledky uložené.
- [ ] Sensitivity analysis (Monte Carlo) spustená ak zmena váhy > ±5%.
- [ ] Gradient/Bayes aktualizácie sú zdokumentované a reproducibilné.

**Kontrola governance procesu**
- [ ] Nominácie a hlasovanie boli riadne zverejnené.
- [ ] Quorum bol dosiahnutý (ak bolo potrebné).
- [ ] Všetky podpisy a commit hash sú priložené.

**Bezpečnosť**
- [ ] Privátne kľúče použité legitímne (multisig), evidence of signing (2-of-3).
- [ ] Žiadne hardcoded credentials v kóde.

**Výstup auditu**
- [ ] Výsledný report v `docs/reports/` s odporúčaním: ACCEPT/CONDITIONAL/ROLLBACK.
- [ ] Ak ROLLBACK: implementačný plán a timeline.

**Podpis audítora:** <signature / commit_hash>
