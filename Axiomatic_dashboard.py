# axiomatic_dashboard.py
# Full live dashboard for Axiomatic Intelligence (AxiomU) system
# Streamlit app: compute AAV (AAV = weighted composite), Bayes/GD updates, CSV import/export, radar (octagon) vizualizácia.
#
# Requirements:
#   pip install streamlit numpy pandas scipy matplotlib
#
# Run:
#   streamlit run axiomatic_dashboard.py

import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import beta
import matplotlib.pyplot as plt
from io import StringIO
import time
from typing import List

# --- Konfigurácia a definície ---
PRINCIPLES = [
    "Zámer (INT)",
    "Existencia (LEX)",
    "Múdrosť (WIS)",
    "Vzájomnosť (REL)",
    "Pravda (VER)",
    "Sloboda (LIB)",
    "Jednota (UNI)",
    "Tvorba (CRE)",
]

# Defaultné váhy podľa tvojho dokumentu (INT, LEX, WIS, REL, VER, LIB, UNI, CRE)
DEFAULT_WEIGHTS = [1.00, 0.95, 0.90, 0.85, 0.90, 0.80, 0.85, 0.95]
# Prahové hodnoty (T0..T7) z dokumentu
THRESHOLDS = [0.8, 0.75, 0.7, 0.65, 0.85, 0.7, 0.75, 0.8]

# --- Výpočtové funkcie ---
def compute_aav(weights: List[float], scores: List[float], biases=None, reciprocities=None) -> float:
    """
    AAV = vážený priemer (váha * skóre * bias * reciprocity) / sum(váh)
    biases alebo reciprocities môžu byť vektorom 1.0, ak nevyužívaš korekcie.
    """
    w = np.array(weights, dtype=float)
    s = np.array(scores, dtype=float)
    if biases is None:
        biases = np.ones_like(s)
    if reciprocities is None:
        reciprocities = np.ones_like(s)
    numerator = np.sum(w * s * np.array(biases) * np.array(reciprocities))
    denominator = np.sum(w) if np.sum(w) != 0 else 1.0
    return float(numerator / denominator)

def bayes_update_weight(prior_a: float, prior_b: float, new_data_success: int, new_data_trials: int) -> float:
    """
    Bayesovský update pre Beta prior. Vracia očakávanú hodnotu posterioru (mean).
    prior_a, prior_b >= 0; new_data_success <= new_data_trials.
    """
    pa = float(prior_a) + max(0, int(new_data_success))
    pb = float(prior_b) + max(0, int(new_data_trials - new_data_success))
    # beta.mean môže v niektorých verziách vyžadovať pa+pb>0; beta.mean(pa,pb) funguje.
    return float(beta.mean(pa, pb))

def gradient_descent_update(weights: List[float], gradients: List[float], learning_rate: float = 0.01) -> List[float]:
    """Jednoduchý GD krok (vracia nové váhy)."""
    w = np.array(weights, dtype=float)
    g = np.array(gradients, dtype=float)
    new_w = w - learning_rate * g
    # zabezpečíme, aby váhy zostali v rozumnom intervale [0, 2]
    new_w = np.clip(new_w, 0.0, 2.0)
    return new_w.tolist()

def get_status(aav: float):
    """Status klasifikácia podľa SAP prahov z dokumentu."""
    if aav >= 0.8:
        return "ACCEPT", "#2ca02c"
    elif aav >= 0.6:
        return "CONDITIONAL", "#ff9800"
    else:
        return "REJECT", "#d62828"

# --- Vizualizácia: radar chart (octagon) ---
def draw_radar_chart(values: List[float], labels: List[str]):
    # values: zoznam dĺžky 8, normalizované 0..1
    N = len(labels)
    # urobíme polygon uzavretý (prvý bod opakujeme)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]
    vals = values + values[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, vals, linewidth=2)
    ax.fill(angles, vals, alpha=0.15)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=9)
    ax.set_ylim(0, 1)
    ax.set_title("AxiomU — Radar (8 princípov)", y=1.08)
    # posledné drobné vylepšenia
    ax.grid(True)
    return fig

# --- Streamlit UI ---
st.set_page_config(page_title="AxiomU Dashboard", layout="wide")
st.title("Axiomatic Intelligence Dashboard (AxiomU v4.0)")
st.markdown(
    "Interaktívny dashboard pre Axiomatickú Inteligenciu. Zadávaj skóre (0..1), vypočítaj AAV, aktualizuj váhy "
    "Bayesovsky alebo GD, importuj/exportuj CSV."
)

# Sidebar nastavenia
st.sidebar.header("Nastavenia")
use_default_weights = st.sidebar.checkbox("Použiť defaultné váhy (od dokumentu)", value=True)
if use_default_weights:
    weights = DEFAULT_WEIGHTS.copy()
else:
    # unikátne kľúče pre každý slider aby Streamlit nerobil konflikt
    weights = []
    for i, p in enumerate(PRINCIPLES):
        k = f"w_{i}"
        weights.append(st.sidebar.slider(p + " — váha", 0.0, 2.0, float(DEFAULT_WEIGHTS[i]), step=0.01, key=k))

st.sidebar.markdown("---")
st.sidebar.markdown("Prahové hodnoty (štandardné):")
for p, t in zip(PRINCIPLES, THRESHOLDS):
    st.sidebar.write(f"{p}: {t:.2f}")

# Hlavný vstup skóre
st.header("Zadajte skóre pre princípy (0.0 — 1.0)")
scores = []
cols = st.columns(2)
for i, p in enumerate(PRINCIPLES):
    # slider per principle with unique key
    key = f"s_{i}_{int(time.time())}"  # čas v key zabráni kolízii pri reload
    with cols[i % 2]:
        scores.append(st.slider(p, min_value=0.0, max_value=1.0, value=0.5, step=0.01, key=f"s_{i}"))

# Výpočet AAV a status
st.header("Výpočet AAV a status")
if st.button("Vypočítať AAV a zobraziť status"):
    aav = compute_aav(weights, scores)
    status, color = get_status(aav)
    st.subheader(f"AAV (Kompozitný index): {aav:.4f}")
    st.markdown(f"**Status:** <span style='color:{color};font-weight:700'>{status}</span>", unsafe_allow_html=True)

    st.subheader("Individuálne indexy vs. prahové hodnoty")
    for i, p in enumerate(PRINCIPLES):
        thresh = THRESHOLDS[i]
        val = scores[i]
        ok = val >= thresh
        emoji = "✅" if ok else "❌"
        st.write(f"{p}: {val:.2f} {'>=' if ok else '<'} {thresh:.2f} {emoji}")

# Vizualizácia radar/octagon
st.header("Vizualizácia: Radar (Oktagon)")
fig = draw_radar_chart(scores, PRINCIPLES)
st.pyplot(fig)

# Aktualizácie váh
st.header("Aktualizácia váh (Bayes alebo Gradient Descent)")
update_method = st.selectbox("Vyber metódu aktualizácie", ("Bayesovská", "Gradient Descent"))

if update_method == "Bayesovská":
    st.markdown("Bayes update: Beta(prior_a, prior_b) -> posterior mean")
    prior_a = st.number_input("Prior a", min_value=0.0, value=1.0, step=0.1)
    prior_b = st.number_input("Prior b", min_value=0.0, value=1.0, step=0.1)
    success = int(st.number_input("Nové úspechy (integer)", min_value=0, value=8, step=1))
    trials = int(st.number_input("Nové pokusy (integer)", min_value=1, value=10, step=1))
    if st.button("Aktualizovať Bayesovsky"):
        new_w = bayes_update_weight(prior_a, prior_b, success, trials)
        st.success(f"Nová váha (posterior mean): {new_w:.4f}")
        st.info("Poznámka: Bayes update vráti JEDNU váhu. Aplikuj ho selektívne na vybrané axiomy.")

elif update_method == "Gradient Descent":
    st.markdown("Gradient Descent: uprav váhy podľa gradientov")
    lr = st.number_input("Learning rate", min_value=0.0001, value=0.01, step=0.0001, format="%.4f")
    st.markdown("Zadaj gradienty pre každý princíp (môžu byť pozitívne alebo negatívne).")
    gradients = []
    gcols = st.columns(2)
    for i, p in enumerate(PRINCIPLES):
        gradients.append(gcols[i % 2].number_input(f"Grad {p}", value=0.0, step=0.01, key=f"g_{i}"))
    if st.button("Aplikovať Gradient Descent"):
        new_weights = gradient_descent_update(weights, gradients, learning_rate=lr)
        st.write("Nové váhy (po kroku GD):")
        for i, nw in enumerate(new_weights):
            st.write(f"{PRINCIPLES[i]}: {nw:.4f}")

# CSV import / export
st.header("CSV Import / Export rozhodnutí")
uploaded_file = st.file_uploader("Nahraj CSV (stĺpce: ID,Dátum, + 8 princípov ...)", type=["csv"])
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.subheader("Náhľad nahratého CSV")
        st.dataframe(df)
        # Example: compute AAV pre každý riadok ak sú stĺpce menom princípov
        if all(p in df.columns for p in PRINCIPLES):
            st.subheader("Pridám stĺpec Kompozit_AAV a Status pre každý riadok")
            df["Kompozit_AAV"] = df.apply(lambda r: compute_aav(DEFAULT_WEIGHTS, [float(r[p]) for p in PRINCIPLES]), axis=1)
            df["Status"] = df["Kompozit_AAV"].apply(lambda v: get_status(v)[0])
            st.dataframe(df)
            # umožniť stiahnutie
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("Stiahnuť upravené CSV", data=csv, file_name="axiomU_results.csv", mime="text/csv")
    except Exception as e:
        st.error(f"Chyba pri čítaní CSV: {e}")

st.markdown("Ak chceš šablónu CSV, zaškrtni nižšie.")
if st.checkbox("Stiahnuť CSV šablónu"):
    template = StringIO()
    header = ["ID Rozhodnutia", "Dátum"] + PRINCIPLES + ["Kompozit_AAV", "Status"]
    df_template = pd.DataFrame([[
        1,
        "2025-10-27",
        0.85, 0.78, 0.92, 0.70, 0.95, 0.82, 0.88, 0.91,
        "", ""
    ]], columns=header)
    st.download_button("Stiahnuť šablónu (CSV)", df_template.to_csv(index=False), "axiomU_template.csv", mime="text/csv")

st.markdown("---")
st.markdown("Spustenie lokálne: `streamlit run axiomatic_dashboard.py`")
st.markdown("Bezpečnostná poznámka: toto je demo. Pred nasadením pridaj autentifikáciu, validáciu vstupov a audit.log.")
