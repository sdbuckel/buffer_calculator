import streamlit as st
import math

# 1. Database
BUFFER_DATA = {
    "Acetic Acid / Acetate": {"pka": 4.76, "acid_mw": 60.05, "salt_mw": 82.03},
    "Ammonia / Ammonium": {"pka": 9.25, "acid_mw": 17.03, "salt_mw": 53.49},
    "TRIS": {"pka": 8.06, "acid_mw": 121.14, "salt_mw": 157.60},
}

st.title("🧪 Smart Buffer Prep Tool")

# --- SIDEBAR ---
st.sidebar.header("1. Buffer Choice")
system = st.sidebar.selectbox("System:", list(BUFFER_DATA.keys()))
pka = BUFFER_DATA[system]["pka"]

st.sidebar.header("2. Prep Method")
method = st.sidebar.radio(
    "How are you making it?",
    ["Use Conjugate Pair (Acid + Salt)", "Partial Neutralization (Acid + Strong Base)"]
)

target_ph = st.sidebar.slider("Target pH:", pka-1.5, pka+1.5, pka)
total_conc = st.sidebar.number_input("Total Buffer Concentration (M):", value=0.1)
vol_ml = st.sidebar.number_input("Total Volume (mL):", value=500)

# --- MATH LOGIC ---
# Using Henderson-Hasselbalch: pH = pka + log(Base/Acid)
# 10^(pH - pka) = Base/Acid
ratio = 10**(target_ph - pka)

# Total_Conc = [Acid] + [Base]
# [Base] = ratio * [Acid] -> Total_Conc = [Acid] * (1 + ratio)
acid_molar = total_conc / (1 + ratio)
base_molar = total_conc - acid_molar
vol_l = vol_ml / 1000

# --- RESULTS ---
st.subheader(f"Recipe for {vol_ml}mL of {system} at pH {target_ph:.2f}")

if method == "Use Conjugate Pair (Acid + Salt)":
    acid_g = acid_molar * vol_l * BUFFER_DATA[system]["acid_mw"]
    salt_g = base_molar * vol_l * BUFFER_DATA[system]["salt_mw"]
    
    st.success(f"**Step 1:** Weigh out **{salt_g:.3f} g** of the Salt.")
    st.success(f"**Step 2:** Add **{acid_g:.3f} g** (or equivalent volume) of the Acid.")
    st.info("**Step 3:** Bring to final volume with DI Water.")

else:
    # Partial Neutralization: Start with all Acid, add Strong Base to convert some to Conjugate Base
    # Moles of Strong Base needed = Moles of Conjugate Base desired
    base_moles_needed = base_molar * vol_l
    st.warning("⚠️ This method requires a calibrated pH meter.")
    st.success(f"**Step 1:** Add **{total_conc * vol_l * BUFFER_DATA[system]['acid_mw']:.3f} g** of Acid to a beaker.")
    st.success(f"**Step 2:** Slowly titrate with 1M NaOH until the pH meter reads **{target_ph:.2f}**.")
    st.info(f"*(Note: You will approximately need {(base_moles_needed * 1000):.1f} mL of 1M NaOH)*")
