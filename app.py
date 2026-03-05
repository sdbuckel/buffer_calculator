import streamlit as st
import math

# 1. Comprehensive Buffer Database
# Format: { Name: [pKa, Molecular Weight of Acid/Protonated form, Molecular Weight of Salt/Base form] }
BUFFER_DATA = {
    "Acetic Acid / Acetate": [4.76, 60.05, 82.03],
    "Ammonia / Ammonium": [9.25, 53.49, 17.03], # Ammonium Chloride / NH3
    "CAPS": [10.40, 221.32, 243.30],
    "Citrate (pKa 1)": [3.13, 192.12, 214.11],
    "Citrate (pKa 2)": [4.76, 192.12, 214.11],
    "Citrate (pKa 3)": [6.40, 192.12, 214.11],
    "Formic Acid / Formate": [3.75, 46.03, 68.01],
    "HEPES": [7.50, 238.30, 260.28],
    "MES": [6.10, 195.20, 217.18],
    "Phosphate (pKa 2)": [7.21, 119.98, 141.96], # NaH2PO4 / Na2HPO4
    "TRIS": [8.06, 157.60, 121.14], # Tris-HCl / Tris Base
}

st.set_page_config(page_title="Pro Buffer Lab", page_icon="🧪")
st.title("🧪 Professional Buffer Lab Calculator")

# --- SIDEBAR: CONFIGURATION ---
st.sidebar.header("1. Chemistry Selection")
system = st.sidebar.selectbox("Buffer System:", sorted(list(BUFFER_DATA.keys())))
pka, mw_acid, mw_base = BUFFER_DATA[system]

st.sidebar.markdown(f"**Selected pKa:** {pka}")

st.sidebar.header("2. Method & Targets")
method = st.sidebar.radio(
    "Preparation Strategy:",
    ["Conjugate Pair (Acid + Base Salt)", "Titration (Start with Acid + NaOH)", "Titration (Start with Base + HCl)"]
)

target_ph = st.sidebar.slider("Target pH:", pka-1.5, pka+1.5, float(pka))
total_conc = st.sidebar.number_input("Total Buffer Molarity (M):", value=0.1, step=0.01)
vol_ml = st.sidebar.number_input("Final Volume (mL):", value=500, step=50)

# --- THE CALCULATIONS ---
vol_l = vol_ml / 1000
# Henderson-Hasselbalch: [Base]/[Acid] = 10^(pH - pKa)
ratio = 10**(target_ph - pka)

# Solve for individual molarities: [Acid] = Total / (1 + ratio)
acid_molar = total_conc / (1 + ratio)
base_molar = total_conc - acid_molar

# --- MAIN DISPLAY ---
st.subheader(f"Recipe: {system}")
st.write(f"Targets: **{total_conc} M** at **pH {target_ph:.2f}**")

col1, col2 = st.columns(2)

if method == "Conjugate Pair (Acid + Base Salt)":
    mass_acid = acid_molar * vol_l * mw_acid
    mass_base = base_molar * vol_l * mw_base
    
    col1.metric("Weigh Acid/Salt 1", f"{mass_acid:.3f} g")
    col2.metric("Weigh Base/Salt 2", f"{mass_base:.3f} g")
    
    st.info(f"**Instructions:** Dissolve both components in ~80% of the water (**{vol_ml*0.8:.0f} mL**), verify pH, then top up to **{vol_ml} mL**.")

elif method == "Titration (Start with Acid + NaOH)":
    mass_start = total_conc * vol_l * mw_acid
    col1.metric(f"Initial {system} Acid", f"{mass_start:.3f} g")
    
    st.success(f"**Step 1:** Dissolve **{mass_start:.3f} g** of the acid form in water.")
    st.success(f"**Step 2:** Titrate with **NaOH** until pH reachs **{target_ph:.2f}**.")
    st.caption(f"Estimated 1M NaOH required: ~{(base_molar * vol_l * 1000):.1f} mL")

else: # Start with Base + HCl
    mass_start = total_conc * vol_l * mw_base
    col1.metric(f"Initial {system} Base", f"{mass_start:.3f} g")
    
    st.success(f"**Step 1:** Dissolve **{mass_start:.3f} g** of the base form in water.")
    st.success(f"**Step 2:** Titrate with **HCl** until pH reachs **{target_ph:.2f}**.")
    st.caption(f"Estimated 1M HCl required: ~{(acid_molar * vol_l * 1000):.1f} mL")

# Buffer Capacity Warning

if abs(target_ph - pka) > 1.0:
    st.warning("⚠️ **Warning:** Your target pH is more than 1 unit away from the pKa. Buffer capacity will be very low.")
