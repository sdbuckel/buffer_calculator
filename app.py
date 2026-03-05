import streamlit as st
import math

# 1. Expanded Buffer Data (Added Molar Masses for common salts)
BUFFER_DATA = {
    "Acetic Acid / Sodium Acetate": {"pka": 4.76, "salt_mw": 82.03},
    "Ammonium Chloride / Ammonia": {"pka": 9.25, "salt_mw": 53.49},
    "Phosphate (monobasic/dibasic)": {"pka": 7.21, "salt_mw": 141.96}, # Na2HPO4
    "TRIS / TRIS-HCl": {"pka": 8.06, "salt_mw": 157.60},
    "Custom": {"pka": 7.00, "salt_mw": 100.00}
}

st.title("🧪 Buffer Prep & Lab Calculator")

# --- SIDEBAR: INPUTS ---
st.sidebar.header("1. Chemistry Setup")
system_choice = st.sidebar.selectbox("Buffer System:", list(BUFFER_DATA.keys()))

# Set pKa and Molar Mass
pka = st.sidebar.number_input("pKa:", value=BUFFER_DATA[system_choice]["pka"])
mw = st.sidebar.number_input("Molar Mass of Salt (g/mol):", value=BUFFER_DATA[system_choice]["salt_mw"])

st.sidebar.header("2. Concentration Targets")
acid_conc = st.sidebar.number_input("Desired [Acid] (M):", value=0.1, step=0.01)
base_conc = st.sidebar.number_input("Desired [Base] (M):", value=0.1, step=0.01)

st.sidebar.header("3. Lab Scale")
volume_ml = st.sidebar.number_input("Total Volume to prepare (mL):", value=500, step=50)

# --- CALCULATIONS ---
# 1. pH Calculation
ph = pka + math.log10(base_conc / acid_conc)

# 2. Mass Calculation (Mass = Molarity * Volume_L * Molar_Mass)
volume_l = volume_ml / 1000
mass_needed = base_conc * volume_l * mw

# --- MAIN DISPLAY ---
st.subheader("Preparation Summary")

col1, col2, col3 = st.columns(3)
col1.metric("Final pH", f"{ph:.2f}")
col2.metric("Salt to Weigh", f"{mass_needed:.3f} g")
col3.metric("Total Volume", f"{volume_ml} mL")

st.info(f"""
**Lab Instructions:**
1. Weigh out **{mass_needed:.3f} g** of the conjugate base salt.
2. Add the required volume of stock acid to reach **{acid_conc} M** in the final solution.
3. Add deionized water until the total volume reaches **{volume_ml} mL**.
""")

# Visualizing the scale
st.progress(min(mass_needed / 50, 1.0)) # Visual bar for scale
