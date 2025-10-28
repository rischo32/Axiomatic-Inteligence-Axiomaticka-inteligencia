> Tento repozitár je nástrojom...

> Pre jednotlivca, korporacie, AI/AGI az po celu civilizaciu, ak nie len jednu... 

> Nie je to mapa,je to KOMPAS...
>
> Nerobí rozhodnutia za teba — len meria, zaznamenáva, ukazuje spravny smer a núti k zodpovednosti... 


---

Čo to je

Axiomatic Intelligence je implementácia axiomatického rámca (Hexagramon / Axiom Engine v1.0–4.0) — súbor nástrojov, dokumentov a šablón na:

kvantifikáciu axiomatických skóre a ich agregáciu (AAV),

auditovateľné záznamy rozhodnutí (append-only JSONL + Merkle anchoring),

automatizované spúšťanie auditu a governance procesu (REP7),

správu governance (Core Custodian Council — CCC) a šablóny pre hlasovanie, nominácie a audity.


Toto nie je experiment — je to kostra, ktorú musíš chrániť.


---

Obsah repozitára (presná štruktúra)

axiomatic-intelligence/
├─ README.md
├─ LICENSE.md
├─ requirements.txt
├─ config/weights.json
├─ .github/workflows/ci.yml
├─ docs/
│  ├─ governance.md
│  ├─ REP7_protocol.md
│  └─ reports/
├─ data/
│  ├─ axiomy.csv
│  └─ rozhodnutia.csv
├─ scripts/
│  ├─ aav_calc.py
│  ├─ bayes_update.py
│  ├─ gd_update.py
│  └─ merkle_anchor.py
├─ src/axiomatic/
│  ├─ engine.py
│  └─ utils.py
├─ tests/
│  └─ test_aav.py
└─ audit/
   └─ log.jsonl


---

Rýchly štart — inštalácia a spustenie

1. Klonuj repozitár:



git clone git@github.com:yourusername/axiomatic-intelligence.git
cd axiomatic-intelligence

2. Vytvor a aktivuj virtuálne prostredie:



python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows PowerShell
venv\Scripts\Activate.ps1
pip install -r requirements.txt

3. Príklad nastavenia váh (config/weights.json):



{
  "INT": 1.00,
  "LEX": 0.95,
  "WIS": 0.90,
  "REL": 0.85,
  "VER": 0.90,
  "LIB": 0.80,
  "UNI": 0.85,
  "CRE": 0.95
}

4. Spusti výpočet AAV:



python scripts/aav_calc.py --weights config/weights.json --scores data/rozhodnutia.csv
# Výstup: data/rozhodnutia_with_aav.csv (pridá stĺpec 'AAV')

5. Vytvor lokálny Merkle root (demo):



python scripts/merkle_anchor.py
# Vypíše Merkle Root pre sample záznamy


---

Formát dát — presne

data/rozhodnutia.csv (hlavička a príklad riadka):

ID Rozhodnutia,Dátum,Zámer (INT),Existencia (LEX),Múdrosť (WIS),Vzájomnosť (REL),Pravda (VER),Sloboda (LIB),Jednota (UNI),Tvorba (CRE),Status
1,2025-10-22,0.85,0.78,0.92,0.70,0.95,0.82,0.88,0.91,ACCEPT

audit/log.jsonl — každý riadok (JSON):

{
  "timestamp":"2025-10-26T12:00:00Z",
  "actor":"m001",
  "action":"update_weights",
  "payload_hash":"sha256:...",
  "commit_hash":"git_sha1...",
  "merkle_leaf":"sha256:..."
}


---

Kľúčové pravidlá a metriky

AAV (Agregátor Axiom Váh) = vážený priemer skóre axiomov podľa prednastavených váh. Používaj ho ako rozhodovací indikátor, nie ako jediný verdikt.

REP7 trigger: ΔAAV ≥ 0.15 medzi dvoma snapshotmi (30/90/365 dní) → automatický audit a governance proces.

Hard-gates: Základné axiomy (najmä LEX — Rešpekt k životu, VER — Pravda) sa nemenia bez procesu Core change (vyšší prah konsenzu).

Quorum / prahy hlasovania: definované v docs/governance.md (minor/material/core changes — 50%/66%/75% podľa typu zmien).

Append-only log: každá zmena musí mať payload_hash a merkle_leaf; merkle_root publikovaný v commite alebo anchore na externom médiu.



---

Governance (kde hľadať pravidlá)

V docs/governance.md sú:

definície rolí (CCC, OM, Observers, Emergency Steward),

procesy nominácií a volieb,

šablóny hlasovaní, protokol záznamov a audit checklisty.


REP7 detailne rozpracovaný v docs/REP7_protocol.md.


---

CI a testovanie

.github/workflows/ci.yml spúšťa:

inštaláciu závislostí,

pytest (testy v tests/),

voliteľne generovanie Merkle root pre zmeny v data/ (nastaviteľné).


Testy musia kontrolovať konzistentnosť compute_aav, reprodukovateľnosť Bayes/GD aktualizácií a integritu Merkle funkcionality.


---

Anchoring (praktické pravidlá)

1. Vytvor Merkle root z batchu nových záznamov.


2. Commitni zmeny s mesajou obsahujúcou merkle_root: <root>.


3. Ak on-chain anchoring: použij multisig (min. 2-of-3). Gas fees sú trvalé — testuj na testnete.


4. Zapíš transakčný hash do audit/log.jsonl.

---

Bezpečnosť — existuje len jedno pravidlo: nechrániš — strácaš

Nikdy neumiestňuj privátne kľúče do repozitára.

Použi multisig pre každé anchoring gesto (2-of-3 alebo silnejší).

Ukladaj kľúče v bezpečnom store (HSM / HashiCorp Vault / hardware token).

Zrkadli audit log aspoň na 2 nezávislé úložiská (napr. IPFS + S3).



---

Licencia a právne upozornenia

Navrhovaná licencia: CC BY-SA 4.0 (uveď autora/zdroj). Tento nástroj nie je náhradou právnej alebo regulačnej konzultácie. Pri spracovaní osobných údajov konaj v súlade s GDPR a miestnymi zákonmi.


---

Odporúčané ďalšie kroky

Zapnúť CI krok na automatickú generáciu merkle_root a uloženie ako artifact.

Vytvoriť testovaciu multisig peněženku na testnete pre overenie anchoring procesu.

Implementovať jednoduchý dashboard (statický React/Tailwind) pre vizualizáciu AAV trendov a REP7 udalostí.

Naplánovať pravidelné audity (30/90/365 dní) s nezávislými Observers.

---

Zodpovednosť — jasne

Tento systém navrhuje a uľahčuje rozhodovanie s etickým jadrom. 
Zodpovednosť za konečné rozhodnutia a ich následky nesie ľudský orgán (CCC, OM, alebo právne zodpovedná osoba). 
AAV je metrika — nie autorita.

---
