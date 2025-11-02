# ai_pipeline.py
"""
AI scoring pipeline:
- featurize decision_record
- embed text (optional: sentence-transformers)
- run scorer (sklearn model / dummy)
- calibrate (Isotonic/Platt) if calibrator provided
- combine with AAV and return final decision
- log canonical JSON (for Merkle anchoring later)
"""
import os
import json
import hashlib
from datetime import datetime
import numpy as np
from sklearn.linear_model import LogisticRegression
from joblib import load

# Try to import sentence-transformers; fallback to simple stub
try:
    from sentence_transformers import SentenceTransformer
    EMB_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
except Exception:
    EMB_MODEL = None

from compute_aav import compute_aav

def canonical_json(obj):
    return json.dumps(obj, separators=(",", ":"), sort_keys=True, ensure_ascii=False)

def simple_text_embedding(text, dim=64):
    if EMB_MODEL:
        return EMB_MODEL.encode(text).astype(float)
    arr = np.zeros(dim, dtype=float)
    for i, ch in enumerate(text.encode('utf8')[:dim]):
        arr[i % dim] += (ch % 127) / 127.0
    return arr

def featurize(decision_record, weights):
    aav = compute_aav(weights, decision_record.get("scores", []))
    sap = float(np.mean(decision_record.get("scores", []))) if decision_record.get("scores") else aav
    text = decision_record.get("reason", "")[:4000]
    emb = simple_text_embedding(text)
    numeric = np.array([aav, sap, decision_record.get("delta_aav", 0.0)])
    features = np.concatenate([numeric, emb])
    meta = {"aav": aav, "sap": sap}
    return features, meta

def load_model(path):
    if path and os.path.exists(path):
        return load(path)
    model = LogisticRegression()
    return model

def ai_predict(model, features):
    try:
        probs = model.predict_proba(features.reshape(1, -1))[0,1]
        return float(probs)
    except Exception:
        v = float(np.tanh(np.mean(features)) * 0.5 + 0.5)
        return v

def calibrate_score(calibrator, raw_score):
    try:
        return float(calibrator.transform([raw_score])[0])
    except Exception:
        return raw_score

def combine_scores(aav, ai_score, alpha=0.7):
    return float(alpha * aav + (1.0 - alpha) * ai_score)

def log_decision(logdir, record):
    os.makedirs(logdir, exist_ok=True)
    ts = datetime.utcnow().isoformat() + "Z"
    record["_logged_at"] = ts
    j = canonical_json(record)
    h = hashlib.sha256(j.encode("utf-8")).hexdigest()
    fname = os.path.join(logdir, f"{ts.replace(':','_')}_{h[:8]}.json")
    with open(fname, "w", encoding="utf-8") as f:
        f.write(j)
    return fname, h

def process_decision(decision_record, model=None, calibrator=None, weights=None, alpha=0.7, logdir="./logs"):
    weights = weights or [1.0]*8
    features, meta = featurize(decision_record, weights)
    ai_raw = ai_predict(model, features)
    ai_cal = calibrate_score(calibrator, ai_raw)
    final = combine_scores(meta["aav"], ai_cal, alpha=alpha)
    if final < 0.5:
        action = "REJECT"
    elif final < 0.7:
        action = "REVIEW"
    else:
        action = "ACCEPT"
    out = {
        "decision_id": decision_record.get("id"),
        "aav": meta["aav"],
        "ai_raw": ai_raw,
        "ai_calibrated": ai_cal,
        "final_score": final,
        "action": action,
        "reason": decision_record.get("reason", ""),
        "scores": decision_record.get("scores", []),
        "meta": decision_record.get("meta", {}),
    }
    fname, h = log_decision(logdir, out)
    return out, fname, h

if __name__ == "__main__":
    demo = {
        "id": "demo-001",
        "scores": [0.82,0.78,0.9,0.7,0.85,0.8,0.88,0.9],
        "reason": "Decision demo: allocate resources to X; risk: moderate environmental impact.",
        "delta_aav": -0.01,
        "meta": {"actor":"system_demo"}
    }
    model = None
    calibrator = None
    out, fname, h = process_decision(demo, model=model, calibrator=calibrator)
    print("Result:", out["action"], "score:", out["final_score"])
    print("Log file:", fname, "hash:", h)
