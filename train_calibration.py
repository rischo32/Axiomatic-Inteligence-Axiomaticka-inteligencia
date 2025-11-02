# train_calibration.py
import argparse
import pandas as pd
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression
from joblib import dump
import numpy as np

def train_isotonic(preds, labels, outpath):
    iso = IsotonicRegression(out_of_bounds="clip")
    iso.fit(preds, labels)
    dump(iso, outpath)
    return iso

def train_platt(preds, labels, outpath):
    lr = LogisticRegression()
    lr.fit(preds.reshape(-1,1), labels)
    dump(lr, outpath)
    return lr

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", required=True)
    p.add_argument("--method", choices=["isotonic","platt"], default="isotonic")
    p.add_argument("--out", required=True)
    args = p.parse_args()
    df = pd.read_csv(args.csv)
    preds = df["pred_raw"].values
    labels = df["label"].values
    if args.method == "isotonic":
        model = train_isotonic(preds, labels, args.out)
    else:
        model = train_platt(preds, labels, args.out)
    print("Saved calibrator to", args.out)

if __name__ == "__main__":
    main()
