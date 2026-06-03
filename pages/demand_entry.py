import streamlit as st

st.title("📝 Water Supply Demand Collection Desk")
st.subheader("Field Dispatch Input Form")
st.write("Modify the current crop, municipal pipelines, and target reach allocations below. Changes save instantly to the global matrix.")

d = st.session_state.demands

f_col1, f_col2, f_col3 = st.columns(3)

with f_col1:
    st.markdown("### 🔹 Pool Block 1 (Khari CR Subsystem)")
    d["in_daskroi"] = st.number_input("223.670 NMC HR (Daskroi) Demand (cfs)", value=d["in_daskroi"], min_value=0.0, step=1.0)
    d["in_amc1"] = st.number_input("226.670 HR - Pipeline (AMC-1) (cfs)", value=d["in_amc1"], min_value=0.0, step=1.0)
    d["in_amc2"] = st.number_input("228.360 HR - Pipeline (AMC-2) (cfs)", value=d["in_amc2"], min_value=0.0, step=1.0)
    d["in_sab_esc"] = st.number_input("229.340 Sabarmati Escape (cfs)", value=d["in_sab_esc"], min_value=0.0, step=1.0)
    d["in_pool1"] = st.number_input("Pool-1 Loss/Gain (+/- cfs)", value=d["in_pool1"], min_value=None, step=1.0)
    
with f_col2:
    st.markdown("### 🔹 Pool Block 2 (Karai CR Subsystem)")
    d["in_gwssb"] = st.number_input("230.500 HR - Pipeline (GWSSB) (cfs)", value=d["in_gwssb"], min_value=0.0, step=1.0)
    d["in_gift"] = st.number_input("230.500 HR - Pipeline (GIFT City) (cfs)", value=d["in_gift"], min_value=0.0, step=1.0)
    d["in_syphonic"] = st.number_input("244.755 HR - Syphonic Pipeline (cfs)", value=d["in_syphonic"], min_value=0.0, step=1.0)
    d["in_dholka"] = st.number_input("246.447 HR (Dholka Branch) (cfs)", value=d["in_dholka"], min_value=0.0, step=1.0)
    d["in_pool2"] = st.number_input("Pool-2 Loss/Gain (+/- cfs)", value=d["in_pool2"], min_value=None, step=1.0)
    
with f_col3:
    st.markdown("### 🔹 Pool Block 3 (Jaspur CR Subsystem)")
    d["in_east_esc"] = st.number_input("255.742 Eastern Drain Escape (cfs)", value=d["in_east_esc"], min_value=0.0, step=1.0)
    d["in_piyaj"] = st.number_input("256.220 Piyaj Dharoi Pipeline (cfs)", value=d["in_piyaj"], min_value=0.0, step=1.0)
    d["in_sanand"] = st.number_input("258.849 HR (Sanand Branch) (cfs)", value=d["in_sanand"], min_value=0.0, step=1.0)
    d["in_saurashtra"] = st.number_input("263.309 HR (Saurashtra Branch) (+/- cfs)", value=d["in_saurashtra"], min_value=None, step=1.0)
    d["in_karannagar"] = st.number_input("263.574 CR (Karannagar CR) (+/- cfs)", value=d["in_karannagar"], min_value=None, step=1.0)
    d["in_pool3"] = st.number_input("Pool-3 Loss/Gain (+/- cfs)", value=d["in_pool3"], min_value=None, step=1.0)

st.session_state.demands = d
st.success("✅ Shared canal operation demands updated! Navigate to the 'Live Flow Accounting Matrix' in the sidebar to review hydraulics.")
