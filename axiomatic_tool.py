#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
axiomatic_tool.py

Univerzálny nástroj pre Axiomatic Intelligence:
- compute-aav: vypočíta AAV pre CSV súbor rozhodnutí
- bayes-update: jednoduchá Bayesova aktualizácia váhového parametra
- gd-update: gradient descent update pre váhy
- merkle-root: vygeneruje Merkle root zo súboru záznamov (JSONL / CSV)
- audit-append: pridá auditný záznam do audit/log.jsonl

Použitie:
    python axiomatic_tool.py compute-aav --weights config/weights.json --scores data/rozhodnutia.csv
    python axiomatic_tool.py merkle-root --input data/rozhodnutia.csv
    python axiomatic_tool.py bayes-update --prior 1 1 --success 8 --trials 10
"""

import argparse
import json
import os
from hashlib import sha256
from datetime import datetime
import csv
import sys

# 3rd party
import numpy as np
import pandas as pd
from scipy.stats import beta

# -------------------------
#  Utility / Core functions
# -------------------------

def safe_float(x):
    """Bezpečne skonvertuje na float; ak neúspech -> ValueError."""
    try:
        return float(x)
    except Exception as e:
        raise ValueError(f"Cannot convert to float: {x}") from e

def compute_aav_from_lists(weights, scores, biases=None, reciprocities=None):
    """
    Vážený priemer (AAV).
    weights, scores: sekvencie rovnakého poradia a dĺžky.
    biases, reciprocities: voliteľné, default 1.
    Vracia float.
    """
    if len(weights) != len(scores):
        raise ValueError("weights and scores must have same length")
    w = np.array([safe_float(x) for x in weights], dtype=float)
    s = np.array([safe_float(x) for x in scores], dtype=float)

    if biases is None:
        b = np.ones_like(s)
    else:
        b = np.array([safe_float(x) for x in biases], dtype=float)
        if b.shape != s.shape:
            raise ValueError("biases must match scores length")

    if reciprocities is None:
        r = np.ones_like(s)
    else:
        r = np.array([safe_float(x) for x in reciprocities], dtype=float)
        if r.shape != s.shape:
            raise ValueError("reciprocities must match scores length")

    numerator = np.sum(w * s * b * r)
    denominator = np.sum(w)
    if denominator == 0:
        raise ZeroDivisionError("Sum of weights is zero")
    return float(numerator / denominator)

def load_weights_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # expected keys like INT, LEX, WIS, REL, VER, LIB, UNI, CRE
    return data

def read_scores_csv(path, expected_cols=None):
    df = pd.read_csv(path)
    if expected_cols:
        missing = [c for c in expected_cols if c not in df.columns]
        if missing:
            raise ValueError(f"Missing expected columns in CSV: {missing}")
    return df

# -------------------------
#  Updates: Bayes & GD
# -------------------------

def bayes_update_weight(prior_a, prior_b, new_success, new_trials):
    """
    Jednoduchá Bayesova aktualizácia pre Beta rozdelenie.
    Vracia strednú hodnotu posteriéru (beta.mean).
    """
    prior_a = safe_float(prior_a)
    prior_b = safe_float(prior_b)
    new_success = int(new_success)
    new_trials = int(new_trials)
    if not (0 <= new_success <= new_trials):
        raise ValueError("new_success must be between 0 and new_trials")
    post_a = prior_a + new_success
    post_b = prior_b + (new_trials - new_success)
    return float(beta.mean(post_a, post_b))

def gradient_descent_update(weights, gradients, lr=0.01):
    """
    Simple gradient descent update: new = w - lr * grad
    weights, gradients: lists of same length
    returns list
    """
    if len(weights) != len(gradients):
        raise ValueError("weights and gradients must be same length")
    w = np.array([safe_float(x) for x in weights], dtype=float)
    g = np.array([safe_float(x) for x in gradients], dtype=float)
    new = w - lr * g
    return [float(x) for x in new]

# -------------------------
#  Merkle / Hash helpers
# -------------------------

def sha256_hex(s: str) -> str:
    return sha256(s.encode('utf-8')).hexdigest()

def merkle_root_from_hashes(hashes):
    """
    Rekurzívne vypočíta Merkle root.
    hashes: list of hex strings.
    Ak je počet nepárny, duplikuje posledný.
    """
    if not hashes:
        return ''
    cur = list(hashes)
    while len(cur) > 1:
        nxt = []
        for i in range(0, len(cur), 2):
            h1 = cur[i]
            h2 = cur[i+1] if i+1 < len(cur) else cur[i]
            nxt.append(sha256_hex(h1 + h2))
        cur = nxt
    return cur[0]

def merkle_root_from_csv_rows(path, row_to_string=None, max_rows=None):
    """
    Vytvor Merkle root zo CSV riadkov.
    row_to_string: funkcia, ktorá z riadka (dict) vráti reťazec; default = JSON-like repr cez CSV order.
    """
    hashes = []
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader):
            if max_rows and idx >= max_rows:
                break
            if row_to_string:
                s = row_to_string(row)
            else:
                # deterministická serializácia: zoradené podľa kľúča
                keys = sorted(row.keys())
                parts = []
                for k in keys:
                    parts.append(f"{k}={row[k]}")
                s = "|".join(parts)
            hashes.append(sha256_hex(s))
    return merkle_root_from_hashes(hashes)

# -------------------------
#  Audit log helper
# -------------------------

def append_audit_log(logpath, actor, action, payload, commit_hash=None, merkle_leaf=None):
    os.makedirs(os.path.dirname(logpath), exist_ok=True)
    entry = {
        "timestamp": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "actor": actor,
        "action": action,
        "payload_hash": sha256_hex(json.dumps(payload, sort_keys=True)),
        "commit_hash": commit_hash or "",
        "merkle_leaf": merkle_leaf or ""
    }
    # append as JSONL
    with open(logpath, "a", encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry

# -------------------------
#  CLI command implementations
# -------------------------

def cmd_compute_aav(args):
    # načítaj váhy
    w = load_weights_json(args.weights)
    # očakávané stĺpce (prispôsobiteľné)
    cols = args.columns.split(",") if args.columns else [
        'Zámer (INT)','Existencia (LEX)','Múdrosť (WIS)','Vzájomnosť (REL)',
        'Pravda (VER)','Sloboda (LIB)','Jednota (UNI)','Tvorba (CRE)'
    ]
    df = read_scores_csv(args.scores, expected_cols=cols)
    # zostav váhový zoznam v rovnakom poradí
    key_map = {
        'Zámer (INT)': 'INT',
        'Existencia (LEX)': 'LEX',
        'Múdrosť (WIS)': 'WIS',
        'Vzájomnosť (REL)': 'REL',
        'Pravda (VER)': 'VER',
        'Sloboda (LIB)': 'LIB',
        'Jednota (UNI)': 'UNI',
        'Tvorba (CRE)': 'CRE'
    }
    weights_list = [w.get(key_map.get(c, c), 1.0) for c in cols]

    aavs = []
    for _, row in df.iterrows():
        scores = [row[c] for c in cols]
        aav = compute_aav_from_lists(weights_list, scores)
        aavs.append(aav)
    df['AAV'] = aavs
    out_path = args.output or args.scores.replace('.csv', '_with_aav.csv')
    df.to_csv(out_path, index=False)
    print(f"[OK] Uloženo: {out_path}")

    # append audit log entry (payload = summary)
    payload = {
        "input_file": args.scores,
        "rows": len(df),
        "weights_used": weights_list,
        "output_file": out_path
    }
    entry = append_audit_log(args.audit or "audit/log.jsonl", args.actor or "cli_user", "compute_aav", payload)
    print("Audit záznam:", entry)

def cmd_bayes_update(args):
    updated = bayes_update_weight(args.prior_a, args.prior_b, args.success, args.trials)
    print(f"[OK] Bayes updated mean: {updated:.6f}")
    # optionally save to file
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump({"posterior_mean": updated}, f, ensure_ascii=False, indent=2)
        print(f"Saved to {args.output}")

def cmd_gd_update(args):
    # load weights and gradients from JSON arrays (simple)
    weights = json.loads(args.weights)
    gradients = json.loads(args.gradients)
    new = gradient_descent_update(weights, gradients, lr=args.lr)
    print("[OK] New weights:", new)
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump({"new_weights": new}, f, ensure_ascii=False, indent=2)
        print(f"Saved to {args.output}")

def cmd_merkle_root(args):
    if args.input.lower().endswith('.csv'):
        root = merkle_root_from_csv_rows(args.input, max_rows=args.max_rows)
        print("[OK] Merkle root:", root)
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump({"merkle_root": root}, f, ensure_ascii=False, indent=2)
            print(f"Saved to {args.output}")
    else:
        print("Podporované vstupy: CSV (pre jednoduchý demo mód).")

def cmd_audit_append(args):
    # payload z JSON súboru alebo string
    if args.payload_file:
        with open(args.payload_file, 'r', encoding='utf-8') as f:
            payload = json.load(f)
    elif args.payload:
        payload = {"note": args.payload}
    else:
        payload = {"note": "manual append"}

    entry = append_audit_log(args.audit or "audit/log.jsonl", args.actor or "cli_user", args.action or "manual", payload, commit_hash=args.commit, merkle_leaf=args.merkle)
    print("[OK] Audit appended:", entry)

# -------------------------
#  CLI parser
# -------------------------

def build_parser():
    p = argparse.ArgumentParser(prog="axiomatic_tool", description="Nástroj pre Axiomatic Intelligence — AAV, updates, Merkle, audit")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("compute-aav", help="Vypočíta AAV pre CSV súbor rozhodnutí.")
    sp.add_argument("--weights", required=True, help="cesta ku config/weights.json")
    sp.add_argument("--scores", required=True, help="CSV s rozhodnutiami")
    sp.add_argument("--columns", required=False, help="voliteľný zoznam stĺpcov oddelených čiarkou v CSV (poradie musí sedieť)")
    sp.add_argument("--output", required=False, help="výstupný CSV súbor")
    sp.add_argument("--audit", required=False, help="audit log path (default: audit/log.jsonl)")
    sp.add_argument("--actor", required=False, help="actor id pre audit (default: cli_user)")
    sp.set_defaults(func=cmd_compute_aav)

    sp = sub.add_parser("bayes-update", help="Bayes aktualizácia pre Beta (vracia posterior mean).")
    sp.add_argument("--prior", nargs=2, type=float, dest="prior", required=False, help="prior a b (alternatívne --prior-a a --prior-b)", metavar=("A","B"))
    sp.add_argument("--prior-a", type=float, default=None)
    sp.add_argument("--prior-b", type=float, default=None)
    sp.add_argument("--success", type=int, required=True)
    sp.add_argument("--trials", type=int, required=True)
    sp.add_argument("--output", required=False, help="uložiť výsledok JSON")
    def _parse_priors(ns):
        if ns.prior:
            ns.prior_a, ns.prior_b = ns.prior
        elif ns.prior_a is None or ns.prior_b is None:
            ns.prior_a, ns.prior_b = 1.0, 1.0
    sp.set_defaults(func=lambda args: (setattr(args, 'prior_a', (args.prior[0] if args.prior else args.prior_a)), setattr(args, 'prior_b', (args.prior[1] if args.prior else args.prior_b)), cmd_bayes_update(args)))

    sp = sub.add_parser("gd-update", help="Gradient descent update pre vektory váh.")
    sp.add_argument("--weights", required=True, help="JSON array váh (napr. '[1.0,0.95]')")
    sp.add_argument("--gradients", required=True, help="JSON array gradientov (napr. '[0.1,-0.05]')")
    sp.add_argument("--lr", type=float, default=0.01, help="learning rate")
    sp.add_argument("--output", required=False, help="uložiť výsledok JSON")
    sp.set_defaults(func=cmd_gd_update)

    sp = sub.add_parser("merkle-root", help="Vygeneruje Merkle root z CSV (demo).")
    sp.add_argument("--input", required=True, help="vstupný CSV súbor")
    sp.add_argument("--output", required=False, help="uložiť merkle root JSON")
    sp.add_argument("--max-rows", type=int, default=None, help="max počet riadkov (demo)")
    sp.set_defaults(func=cmd_merkle_root)

    sp = sub.add_parser("audit-append", help="Pridá záznam do audit/log.jsonl")
    sp.add_argument("--audit", required=False, help="cesta k audit logu (default: audit/log.jsonl)")
    sp.add_argument("--actor", required=False, help="actor id")
    sp.add_argument("--action", required=False, help="action name")
    sp.add_argument("--payload-file", required=False, help="JSON súbor s payload")
    sp.add_argument("--payload", required=False, help="malý text payload")
    sp.add_argument("--commit", required=False, help="commit hash (voliteľné)")
    sp.add_argument("--merkle", required=False, help="merkle leaf hash (voliteľné)")
    sp.set_defaults(func=cmd_audit_append)

    return p

def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
        print("Chyba:", str(e), file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
