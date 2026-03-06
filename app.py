import streamlit as st
import math

# 1. Database with Citrate as a special case (list of pKas)
BUFFER_DATA = {
    "Acetic Acid / Acetate": {"pka": 4.76, "mw_acid": 60.05, "mw_base": 82.03},
    "Ammonia / Ammonium": {"pka": 9.25, "mw_acid": 53.49, "mw_base": 17.03},
    "CAPS": {"pka": 10.40, "mw_acid": 221.32, "mw_base": 243.30},
    "Citrate (Triprotic)": {"pka": [3.13, 4.76, 6.40], "mw_acid": 192.12, "mw_base": 214.11},
    "Formic Acid / Formate": {"pka": 3.75, "mw_acid": 46.03, "mw_base": 68.01},
    "HEPES": {"pka": 7.50, "mw_acid": 238.30, "mw_base": 260.28},
    "MES": {"pka": 6.10, "mw_acid": 195.20, "mw_base": 217.18},
    "Phosphate (pKa 2)": {"pka": 7.21, "mw_acid": 119.98, "mw_base": 141.96},
    "TRIS": {"pka": 8.06, "mw_acid": 157.60, "mw_base": 121.14},
}

st.set_page_config(page_title="Buffer Calculator", page_icon="🧪")
st.title("🧪 Buffer Calculator")

# --- SIDEBAR ---
st.sidebar.header("1. Buffer Choice")
system = st.sidebar.selectbox("Buffer System:", sorted(list(BUFFER_DATA.keys())))

# Handle Citrate pKa selection automatically
raw_pka = BUFFER_DATA[system]["pka"]
mw_acid = BUFFER_DATA[system]["mw_acid"]
mw_base = BUFFER_DATA[system]["mw_base"]

st.sidebar.header("2. Method & Targets")
method = st.sidebar.radio(
    "Preparation Strategy:",
    ["Conjugate Pair (Acid + Base Salt)", "Titration (Start with Acid + NaOH)", "Titration (Start with Base + HCl)"]
)

# Set slider range based on pKa (or middle pKa for Citrate)
slider_ref = raw_pka[1] if isinstance(raw_pka, list) else raw_pka
target_ph = st.sidebar.slider("Target pH:", 2.0, 12.0, float(slider_ref))

# Logic to pick the best pKa for Citrate
if isinstance(raw_pka, list):
    pka = min(raw_pka, key=lambda x: abs(x - target_ph))
    st.sidebar.info(f"Using $pK_{{a}}$ {pka} (closest to target pH)")
else:
    pka = raw_pka

# Concentration in mM
total_conc_mm = st.sidebar.number_input("Total Buffer Concentration (mM):", value=50.0, step=10.0)
vol_ml = st.sidebar.number_input("Final Volume (mL):", value=500, step=50)

# --- THE MATH ---
total_molar = total_conc_mm / 1000  # Convert mM to M
vol_l = vol_ml / 1000
ratio = 10**(target_ph - pka)

acid_molar = total_molar / (1 + ratio)
base_molar = total_molar - acid_molar

# --- MAIN DISPLAY ---
st.subheader(f"Recipe: {system}")
st.write(f"Targeting **{total_conc_mm} mM** at **pH {target_ph:.2f}**")

col1, col2 = st.columns(2)

if method == "Conjugate Pair (Acid + Base Salt)":
    mass_acid = acid_molar * vol_l * mw_acid
    mass_base = base_molar * vol_l * mw_base
    col1.metric("Acid/Salt 1", f"{mass_acid:.4f} g")
    col2.metric("Base/Salt 2", f"{mass_base:.4f} g")
    st.info(f"**Instructions:** Dissolve both in ~80% volume, check pH, then top up to {vol_ml}mL.")

elif method == "Titration (Start with Acid + NaOH)":
    mass_start = total_molar * vol_l * mw_acid
    col1.metric(f"Initial {system} Acid", f"{mass_start:.4f} g")
    st.success(f"**Step 1:** Dissolve **{mass_start:.4f} g** of acid form.")
    st.success(f"**Step 2:** Titrate with NaOH to pH **{target_ph}**.")
    st.caption(f"Est. 1M NaOH: ~{(base_molar * vol_l * 1000):.1f} mL")

else: # Base + HCl
    mass_start = total_molar * vol_l * mw_base
    col1.metric(f"Initial {system} Base", f"{mass_start:.4f} g")
    st.success(f"**Step 1:** Dissolve **{mass_start:.4f} g** of base form.")
    st.success(f"**Step 2:** Titrate with HCl to pH **{target_ph}**.")
    st.caption(f"Est. 1M HCl: ~{(acid_molar * vol_l * 1000):.1f} mL")

# Buffer Capacity Warning Diagram

if abs(target_ph - pka) > 1.0:
    st.warning("⚠️ **Low Buffer Capacity:** Target pH is far from pKa.")
