# scripts/aav_calc.py
import json
import numpy as np
import pandas as pd
import argparse

def compute_aav(weights, scores, biases=None, reciprocities=None):
    weights = np.array(weights, dtype=float)
    scores = np.array(scores, dtype=float)
    if biases is None:
        biases = np.ones(len(scores))
    if reciprocities is None:
        reciprocities = np.ones(len(scores))
    numerator = np.sum(weights * scores * biases * reciprocities)
    denominator = np.sum(weights)
    return float(numerator/denominator)

def load_weights(path):
    with open(path,'r',encoding='utf-8') as f:
        return json.load(f)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--weights', required=True, help='JSON file with weights (dict)')
    p.add_argument('--scores', required=True, help='CSV with decision rows (see data/rozhodnutia.csv)')
    args = p.parse_args()

    w = load_weights(args.weights)
    df = pd.read_csv(args.scores)
    # Assumes columns: Zámer (INT),Existencia (LEX),Múdrosť (WIS),Vzájomnosť (REL),Pravda (VER),Sloboda (LIB),Jednota (UNI),Tvorba (CRE)
    cols = ['Zámer (INT)','Existencia (LEX)','Múdrosť (WIS)','Vzájomnosť (REL)','Pravda (VER)','Sloboda (LIB)','Jednota (UNI)','Tvorba (CRE)']
    outputs = []
    for _, row in df.iterrows():
        scores = [row[c] for c in cols]
        weights = [w[k] for k in ['INT','LEX','WIS','REL','VER','LIB','UNI','CRE']]
        aav = compute_aav(weights, scores)
        outputs.append(aav)
    df['AAV'] = outputs
    out = args.scores.replace('.csv','_with_aav.csv')
    df.to_csv(out, index=False)
    print("Saved:", out)

if __name__ == '__main__':
    main()
