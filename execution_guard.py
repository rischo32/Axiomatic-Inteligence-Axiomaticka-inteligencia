# execution_guard.py
"""
Execution Guard stub: validate decision_record through validators.
This is a starter implementation — replace signature checks and validators with real ones.
"""
from compute_aav import compute_aav
from ai_pipeline import process_decision

MIN_AAV = 0.65
MIN_FINAL = 0.60
SIM_FAIL_RATE_MAX = 0.25
SEK_MAX = 0.30

def verify_signatures(decision):
    # Placeholder: in production verify ed25519 / ecdsa signatures
    return "signatures" in decision and len(decision["signatures"])>0

def axiom_validator(decision, weights):
    aav = compute_aav(weights, decision.get("scores", []))
    ok = aav >= MIN_AAV
    return {"name":"axiom","ok":ok,"blocking":True,"score":aav,"reason":f"AAV={aav:.3f}"}

def simulation_validator(decision):
    # Placeholder heuristic for simulation failure rate
    fail_rate = 0.12
    ok = fail_rate <= SIM_FAIL_RATE_MAX
    return {"name":"simulation","ok":ok,"blocking":True,"score":1-fail_rate,"reason":f"fail_rate={fail_rate:.2f}"}

def sek_validator(decision):
    # Placeholder SEK estimate
    sek = 0.15
    ok = sek <= SEK_MAX
    return {"name":"sek","ok":ok,"blocking":True,"score":1-sek,"reason":f"sek={sek:.3f}"}

def ai_risk_validator(decision, model=None, calibrator=None, weights=None):
    out, _, _ = process_decision(decision, model=model, calibrator=calibrator, weights=weights)
    final = out.get("final_score", 0.0)
    ai_cal = out.get("ai_calibrated", 0.0)
    ok = final >= MIN_FINAL and ai_cal >= 0.2
    return {"name":"ai_risk","ok":ok,"blocking":True,"score":final,"reason":f"ai={ai_cal:.3f}, final={final:.3f}"}

def aggregate_results(results):
    from datetime import datetime
    return {"timestamp":datetime.utcnow().isoformat()+"Z","results":results,"overall_ok":all(r["ok"] for r in results)}

def execution_guard(decision, model=None, calibrator=None, weights=None):
    if not verify_signatures(decision):
        return {"executed":False,"reason":"INVALID_SIGNATURES"}
    validators = [
        axiom_validator(decision, weights or [1.0]*8),
        ai_risk_validator(decision, model=model, calibrator=calibrator, weights=weights),
        simulation_validator(decision),
        sek_validator(decision),
    ]
    blocked = any((not v["ok"]) and v.get("blocking",False) for v in validators)
    report = aggregate_results(validators)
    if blocked:
        # store block record, anchor later
        return {"executed":False,"reason":"BLOCKED_BY_VALIDATOR","report":report}
    tx = {"txid":"demo-tx-123"}
    return {"executed":True,"tx":tx,"report":report}

if __name__ == "__main__":
    demo = {
        "id":"demo-001",
        "scores":[0.82,0.78,0.9,0.7,0.85,0.8,0.88,0.9],
        "reason":"Demo decision",
        "signatures":[{"actor_id":"ccc1","sig":"stub"}],
        "meta":{}
    }
    res = execution_guard(demo)
    print(res)
