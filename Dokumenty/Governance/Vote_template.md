# Záznam hlasovania (Vote Record)

**Vote ID:** vote-YYYYMMDD-XXXX  
**Názov návrhu:** <krátky názov>  
**Typ zmeny:** Minor / Material / Core / Emergency  
**Dátum otvorenia:** YYYY-MM-DD HH:MM (UTC)  
**Dátum uzavretia:** YYYY-MM-DD HH:MM (UTC)  
**Quorum:** <počet očakávaných členov> (min required)  
**Zúčastnení (mená/ID):**
- <member1> (present/absent)
- <member2>

**Návrh (full text):**
<kompletný text návrhu>

**Options / Ballot:**
- FOR — accept (optional remediation plan)
- AGAINST — reject
- ABSTAIN — neutral
- CONDITIONAL — accept if conditions (must specify)

**Výsledok (tabuľka):**
| Member ID | Vote | Signature (commit hash / GPG) |
|-----------|------|-------------------------------|
| member1   | FOR  | <commit_hash_or_sig>          |

**Final decision:** ACCEPT / REJECT / CONDITIONAL (detaily)  
**Commit hash / Merkle root (post-commit anchoring):** <commit_hash> / <merkle_root>  
**Related artifacts:** link to report, tests, CI logs.

**Notes & remediation plan (if accepted with conditions):**
- ...
