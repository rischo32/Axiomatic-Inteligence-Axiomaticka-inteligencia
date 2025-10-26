# Governance - Core Custodian Council (CCC)

## Účel
Tento dokument definuje governance model pre Axiomatic Intelligence — rozhodovacie orgány, procesy zmeny axiomov a váh, REP7 protokol, hard-gates a auditnú zodpovednosť. Cieľ: zabezpečiť transparentnú, reprodukovateľnú a vynútiteľnú správu jadra (Hexagramon / Axiom Engine v1.0).

## Základné princípy
1. **Pravda (VER)** — každé rozhodnutie musí byť zdokumentované, s provenance dát.  
2. **Rešpekt k životu (LEX)** — zmeny smerujú k ochrane a obnove živého.  
3. **Auditovateľnosť** — všetky aktualizácie váh, skóre a REP7 výsledkov musia byť zapečatené (JSONL + Merkle root).  
4. **Minimalizmus zmeny (hard-gate)** — zmeny core axiomu vyžadujú nadpolovičnú alebo vyššiu mieru konsenzu podľa typu zmeny (viď sekcia „Konsenzus“).

## Orgány a role
- **Core Custodian Council (CCC)**  
  - Zodpovednosť: schvaľovanie zmien axiomatického jadra (váhy, definície axiomov, hard-gates).  
  - Počet: flexibilný, preferované 5–11 členov.  
  - Mandát: 90 dní, po uplynutí mandát pokračuje volením alebo potvrdením.  
- **Operational Maintainer (OM)**  
  - Zodpovednosť: implementácia technických zmien, CI, deployment, správne spustenie REP7.  
  - Mandát: prevádzková rezerva — trvalý.  
- **Observers / Auditor Pool (OP)**  
  - Zodpovednosť: priebežné audity, nezávislé validácie, reporty. Môžu byť externí.  
- **Emergency Steward (ES)**  
  - Zodpovednosť: dočasné oprávnenie konať pri kritickom incidente (max 72 hodín), musí byť následne potvrdené CCC.

## Konsenzus a hlasovanie
- **Typy zmien**:
  - *Minor change* — implementačné úpravy, dokumentačné zmeny. Konsenzus: 50%+1 prítomných hlasov (quorum 40% členstva).
  - *Material change* — úprava váh (≤ ±10%), REP7 parametre: 66% hlasov, quorum 60%.
  - *Core change* — zmena axiomu, meniace filozofiu systému: 75% hlasov, quorum 75%, verejné oznámenie 14 dní pred hlasovaním.
  - *Emergency rollback / patch* — aktivuje ES, následná retrospektíva a ratifikácia CCC do 7 dní.
- **Formát hlasovania**: zápis hlasovania v `votes/YYYY-MM-DD_voteID.md` a CSV `votes/votes_log.csv` (štandardizované polia nižšie).
- **Quorum**: počet aktívnych členov prítomných pri hlasovaní; ak nie je dosiahnutý quorum, hlasovanie sa odkladá.

## REP7 protokol (trigger a proces)
- **Trigger**: ΔAAV ≥ 0.15 medzi dvoma následnými snapshotmi (30/90/365 d.).  
- **Kroky**:
  1. Automatický alert zaslaný OM + Observers (log + Merkle root snapshot formy).  
  2. OM pripraví dôkladný report (data provenance, príčiny, model changes) do `docs/reports/rep7_<date>.md`.  
  3. CCC zvolá nadzvukové (emergency) zasadnutie v priebehu 72 hodín.  
  4. Návrhy: *Accept with remediation*, *Conditional rollback*, *Full rollback*. Každý návrh musí obsahovať plán nápravy a časový plán.  
  5. Hlasovanie: pre material/core rozhodnutia platia vyššie prahy.  
  6. Po schválení sa vykoná audit a publikujú sa verejné záznamy (Merkle root + JSONL + commit hash).

## Audit & záznamy
- **Formát**: všetky zmeny zapisovať do append-only JSONL v `audit/log.jsonl` (pole: timestamp, actor, action, payload_hash, commit_hash, merkle_leaf_hash).  
- **Uchovávanie**: min. 365 dní online + nezávislé mirrorovanie (IPFS/GitHub release).  
- **Kontrolné body** (minimálne): data provenance, test-suite výsledky, Merkle anchoring, podpisy (at least 2 signatures: OM + CCC lead).

## Hard-gates (nesporné pravidlá)
- Nemožno zmeniť základné znenie axióm LEX a VER bez Core change procesu.  
- Všetky zmeny váh > ±15% musia byť sprevádzané Monte Carlo sensitivity reportom.  
- Ak REP7 odporučí „full rollback“, implementácia má prednosť pred novými zmenami do ukončenia REP7.

## Bezpečnosť a správa kľúčov
- Privátne kľúče OM a ES sú uchovávané v HSM alebo bezpečnom vaulte (HashiCorp, GPG s dvojitým podpisom).  
- Nikto jednotlivo nesmie vykonať anchoring transakciu bez ďalšieho podpisu (minimálne 2-of-3 multisig pre blockchain anchoring).

## Proces nominácie a voľby (shrnuté)
- Nominácie otvárané každý štvrťrok. Formulár: `docs/governance/nominations/nomination_FORM.md` (šablóna nižšie).  
- Nominácie sú anonymizované a verifikované Observers pred zverejnením.  
- Voľby prebiehajú prostredníctvom zapísaného hlasovania (CSV + podpísaný commit). Výsledky sa uložia s Merkle root.

## Prílohy
- `governance/nomination_FORM.md` (šablóna)
- `governance/vote_template.md` a `votes/votes_log.csv`
- `governance/audit_checklist.md`
- `governance/meeting_minutes_TEMPLATE.md`
