import streamlit as st

# Enforce uniform wide layout across all sub-pages
st.set_page_config(page_title="Narmada Main Canal Control Room", layout="wide")

# --- INITIALIZE CORE SHARED DEMAND STATES ---
# This dictionary ensures data persists when swapping between pages
if "demands" not in st.session_state:
    st.session_state.demands = {
        "in_daskroi": 304.0, "in_amc1": 16.0, "in_amc2": 16.0, "in_sab_esc": 0.0, "in_pool1": 15.0,
        "in_gwssb": 45.0, "in_gift": 10.0, "in_syphonic": 25.0, "in_dholka": 150.36, "in_pool2": 20.0,
        "in_east_esc": 0.0, "in_piyaj": 132.0, "in_sanand": 190.0, "in_saurashtra": 950.0, "in_karannagar": 800.0, "in_pool3": 25.0
    }

# --- DEFINE ROUTING PAGES ---
# Pointing directly to the modular sub-page scripts
demand_page = st.Page("pages/demand_entry.py", title="📝 Demand Collection Desk", icon="📝", default=True)
matrix_page = st.Page("pages/flow_matrix.py", title="📊 Live Flow Accounting Matrix", icon="📊")

# --- INITIALIZE SIDEBAR NAVIGATION ---
st.sidebar.markdown("### 🏢 SSNNL Operational Navigation")
pg = st.navigation([demand_page, matrix_page])
pg.run()
