#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_report_html.py

Vytvorí pekný, interaktívny (frontend-ready) HTML report z:
 - data/rozhodnutia_with_aav.csv (preferované)
 - alebo data/rozhodnutia.csv (ak AAV chýba, report sa pokúsi inferovať)
 - a z audit/log.jsonl (vezme posledný záznam pre merkle_root a timestamp)

Výstup: data/report.html (cesta zadefinovaná nižšie)

Spustenie:
    python3 generate_report_html.py
"""

from __future__ import annotations
import csv
import json
import os
import sys
import html as htmllib
import statistics
from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any

BASE = os.path.abspath(os.path.dirname(__file__))
DATA_WITH_AAV = os.path.join(BASE, "data", "rozhodnutia_with_aav.csv")
DATA_RAW = os.path.join(BASE, "data", "rozhodnutia.csv")
AUDIT_LOG = os.path.join(BASE, "audit", "log.jsonl")
OUT_HTML = os.path.join(BASE, "report.html")

# --- Helper functions -----------------------------------------------------

def read_csv(path: str) -> Tuple[List[Dict[str, str]], List[str]]:
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]
    return rows, reader.fieldnames if reader.fieldnames else []

def last_audit_entry(audit_path: str) -> Optional[Dict[str, Any]]:
    if not os.path.exists(audit_path):
        return None
    last = None
    with open(audit_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                last = json.loads(line)
            except Exception:
                # ignore malformed lines
                continue
    return last

def try_get_aav(row: Dict[str, str]) -> Optional[float]:
    for k in row.keys():
        if k.strip().lower() == "aav" or k.strip().lower().endswith("aav"):
            try:
                return float(str(row[k]).replace(',', '.'))
            except Exception:
                return None
    return None

def status_color(status: Optional[str]) -> str:
    s = (status or "").upper()
    if "ACCEPT" in s:
        return "#2ecc71"
    if "CONDITIONAL" in s or "WARN" in s:
        return "#f39c12"
    if "REJECT" in s or "DENY" in s:
        return "#e74c3c"
    return "#95a5a6"

def make_sparkline_svg(values: List[float], w: int = 480, h: int = 60) -> str:
    if not values:
        return ""
    mn = min(values)
    mx = max(values)
    rng = mx - mn if mx != mn else 1.0
    pts = []
    step = w / max(1, (len(values) - 1))
    for i, v in enumerate(values):
        x = i * step
        y = h - ((v - mn) / rng) * h
        pts.append(f"{x:.2f},{y:.2f}")
    path = " ".join(pts)
    svg = (
        f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
        f'<polyline points="{path}" fill="none" stroke="#9ad0f5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        f'</svg>'
    )
    return svg

# Axiomy heuristika (pre prípad, že CSV nemá AAV stĺpec)
AXIOM_KEYWORDS = {
    "INT": ["zámer (int)", "zamer (int)", "zámer", "zamer", "int"],
    "LEX": ["existencia (lex)", "existencia", "lex"],
    "WIS": ["múdrosť (wis)", "múdrosť", "mudrost", "wis"],
    "REL": ["vzájomnosť (rel)", "vzájomnosť", "vzajomnost", "rel"],
    "VER": ["pravda (ver)", "pravda", "ver"],
    "LIB": ["sloboda (lib)", "sloboda", "lib"],
    "UNI": ["jednota (uni)", "jednota", "uni"],
    "CRE": ["tvorba (cre)", "tvorba", "cre"],
}

# --- Core generator ------------------------------------------------------

def generate_html(rows: List[Dict[str, str]], fieldnames: List[str], audit_last: Optional[Dict[str, Any]]) -> str:
    now = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    # Extract AAV series (prefer explicit AAV column)
    aavs = []
    for r in rows:
        a = try_get_aav(r)
        if a is not None and isinstance(a, float):
            aavs.append(a)
    # If no explicit AAV, try to infer averages from axiom columns
    if not aavs:
        # build normalized header map
        headers = [h.strip() for h in fieldnames] if fieldnames else (list(rows[0].keys()) if rows else [])
        norm = {h.lower(): h for h in headers}
        # find mapping from AXIOM_KEYWORDS
        found = {}
        for code, aliases in AXIOM_KEYWORDS.items():
            found[code] = None
            for a in aliases:
                if a in norm:
                    found[code] = norm[a]
                    break
        # compute inferred AAV per row as mean of available axiom columns
        for r in rows:
            vals = []
            for code, col in found.items():
                if col:
                    try:
                        v = float(str(r.get(col, "")).replace(',', '.'))
                        vals.append(v)
                    except Exception:
                        continue
            if vals:
                aavs.append(sum(vals) / len(vals))
    # Stats
    aavs_clean = [v for v in aavs if isinstance(v, (int, float))]
    count = len(rows)
    avg = f"{statistics.mean(aavs_clean):.6f}" if aavs_clean else "n/a"
    mn = f"{min(aavs_clean):.6f}" if aavs_clean else "n/a"
    mx = f"{max(aavs_clean):.6f}" if aavs_clean else "n/a"
    last_merkle = audit_last.get("merkle_root") if audit_last else ""
    audit_ts = audit_last.get("timestamp") if audit_last else ""

    # visible columns
    visible_cols = fieldnames[:] if fieldnames else (list(rows[0].keys()) if rows else [])
    if "AAV" not in visible_cols and not any(c.strip().lower().endswith("aav") for c in visible_cols):
        visible_cols.append("AAV")

    # build table rows
    table_rows_html = ""
    for r in rows:
        aav = try_get_aav(r)
        aav_val = f"{aav:.6f}" if aav is not None else ""
        bar_w = max(0, min(100, (aav or 0) * 100))
        status = r.get("Status", r.get("status", ""))
        color = status_color(status)
        cells = []
        for c in visible_cols:
            val = r.get(c, "")
            if c.strip().lower().endswith("aav"):
                cell_html = (
                    f'<div style="display:flex;gap:8px;align-items:center;">'
                    f'<div style="min-width:70px;font-weight:700">{htmllib.escape(aav_val)}</div>'
                    f'<div style="flex:1;background:#2b2b2b;border-radius:6px;height:12px;overflow:hidden">'
                    f'<div style="width:{bar_w}%;height:100%;background:{color}"></div>'
                    f'</div></div>'
                )
            else:
                cell_html = htmllib.escape(str(val))
            cells.append(f"<td>{cell_html}</td>")
        table_rows_html += "<tr>" + "".join(cells) + "</tr>\n"

    spark = make_sparkline_svg(aavs_clean, w=480, h=60) if aavs_clean else ""

    # HTML template (kept simple, dark theme)
    html_content = f"""<!doctype html>
<html lang="sk">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Axiomatic Intelligence — Report</title>
<style>
:root{{--bg:#0f1720;--card:#111827;--muted:#94a3b8;--accent:#9ad0f5;--glass:rgba(255,255,255,0.03)}}
body{{margin:0;font-family:system-ui, -apple-system, "Segoe UI", Roboto,"Helvetica Neue",Arial; background:var(--bg); color:#e6eef8}}
.container{{max-width:1100px;margin:18px auto;padding:18px}}
.header{{display:flex;justify-content:space-between;align-items:center;gap:12px}}
.card{{background:var(--card);padding:14px;border-radius:12px;box-shadow:0 6px 18px rgba(0,0,0,0.6)}}
.h1{{font-size:20px;margin:0;color:#fff}}
.meta{{color:var(--muted);font-size:13px}}
.grid{{display:grid;grid-template-columns:1fr 320px;gap:14px;margin-top:14px}}
.summary{{display:flex;flex-direction:column;gap:10px}}
.metrics{{display:flex;gap:12px}}
.metric{{background:var(--glass);padding:10px;border-radius:8px;min-width:120px;text-align:center}}
.metric .val{{font-weight:800;font-size:18px;color:#fff}}
.table-wrap{{margin-top:14px;overflow:auto;border-radius:8px;box-shadow:0 6px 20px rgba(0,0,0,0.6)}}
table{{width:100%;border-collapse:collapse}}
th,td{{padding:8px 10px;text-align:left;border-bottom:1px solid rgba(255,255,255,0.03);font-size:13px}}
th{{color:var(--muted);font-weight:600;font-size:12px}}
.badge{{padding:6px 8px;border-radius:999px;font-weight:700;font-size:12px}}
.footer{{margin-top:18px;color:var(--muted);font-size:13px;display:flex;justify-content:space-between;align-items:center}}
.small{{font-size:12px;color:var(--muted)}}
.code{{font-family:monospace;background:rgba(255,255,255,0.02);padding:6px;border-radius:6px}}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div>
      <div class="h1 card">Axiomatic Intelligence — Report</div>
      <div class="meta">Vygenerované: {htmllib.escape(now)} &nbsp;•&nbsp; Počet záznamov: {count}</div>
    </div>
    <div class="card" style="min-width:320px;text-align:right">
      <div class="small">Posledný Merkle root</div>
      <div class="code" style="margin-top:6px;word-break:break-all">{htmllib.escape(last_merkle or '—')}</div>
      <div class="small" style="margin-top:6px">Audit timestamp: {htmllib.escape(audit_ts or '—')}</div>
    </div>
  </div>

  <div class="grid">
    <div class="card summary">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <div>
          <div style="color:var(--muted);font-size:13px">Štatistiky AAV</div>
          <div style="font-size:20px;font-weight:800;color:#fff">{htmllib.escape(str(avg))} <span style="font-size:12px;color:var(--muted)">avg</span></div>
        </div>
        <div style="text-align:right">
          <div class="small">min: {mn}</div>
          <div class="small">max: {mx}</div>
        </div>
      </div>

      <div style="margin-top:8px">{spark}</div>

      <div class="metrics" style="margin-top:12px">
        <div class="metric card"><div class="small">Záznamy</div><div class="val">{count}</div></div>
        <div class="metric card"><div class="small">Avg AAV</div><div class="val">{htmllib.escape(str(avg))}</div></div>
        <div class="metric card"><div class="small">Merkle</div><div class="val" style="font-size:14px">{(last_merkle[:8]+'...') if last_merkle else '—'}</div></div>
      </div>

      <div style="margin-top:12px">
        <div class="small" style="margin-bottom:6px">Legenda stĺpca AAV</div>
        <div style="display:flex;gap:8px;align-items:center">
          <div style="width:80px">ACCEPT ≥0.80</div><div style="height:12px;background:#2ecc71;border-radius:6px;flex:1"></div>
        </div>
        <div style="display:flex;gap:8px;align-items:center;margin-top:6px">
          <div style="width:80px">CONDITIONAL</div><div style="height:12px;background:#f39c12;border-radius:6px;flex:1"></div>
        </div>
        <div style="display:flex;gap:8px;align-items:center;margin-top:6px">
          <div style="width:80px">REJECT</div><div style="height:12px;background:#e74c3c;border-radius:6px;flex:1"></div>
        </div>
      </div>

    </div>

    <div class="card" style="overflow:auto">
      <div style="font-weight:700;margin-bottom:8px">Posledné rozhodnutia</div>
      <div class="table-wrap">
        <table>
          <thead><tr>{''.join(f'<th>{htmllib.escape(c)}</th>' for c in visible_cols)}</tr></thead>
          <tbody>
          {table_rows_html}
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <div class="footer">
    <div class="small">Report vygeneroval lokálny skript — kontrola integrity pomocou Merkle rootu.</div>
    <div>
      <a href="data/rozhodnutia_with_aav.csv" style="color:var(--accent);text-decoration:none">Stiahnuť CSV</a>
      &nbsp;·&nbsp;
      <a href="audit/log.jsonl" style="color:var(--accent);text-decoration:none">Zobraziť audit log</a>
    </div>
  </div>
</div>
</body>
</html>
"""
    return html_content

# --- main ----------------------------------------------------------------

def main():
    # pick data file (prefer explicit AAV)
    data_file = DATA_WITH_AAV if os.path.exists(DATA_WITH_AAV) else (DATA_RAW if os.path.exists(DATA_RAW) else None)
    if not data_file:
        print("Nenájdené data/rozhodnutia_with_aav.csv ani data/rozhodnutia.csv. Umiestni ich do data/ a skúšaj znova.", file=sys.stderr)
        return

    rows, fieldnames = read_csv(data_file)
    if not rows:
        print("Data súbor je prázdny.", file=sys.stderr)
        return

    audit_last = last_audit_entry(AUDIT_LOG)
    html_text = generate_html(rows, fieldnames, audit_last)

    os.makedirs(os.path.dirname(OUT_HTML), exist_ok=True)
    with open(OUT_HTML, "w", encoding='utf-8') as f:
        f.write(html_text)

    print("Report vygenerovaný:", OUT_HTML)
    print("Otvoriť v telefóne (Termux): termux-open", OUT_HTML)

if __name__ == "__main__":
    main()
