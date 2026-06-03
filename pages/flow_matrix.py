import streamlit as st
import pandas as pd
import math
from datetime import datetime

st.title("📊 Narmada Main Canal - Live Flow Accounting Matrix")
st.subheader("Simultaneous Pool Hydraulics & Multi-Gate Regulation Control Room")

# --- HISTORICAL SNAPSHOT SYSTEM ---
if "log_book" not in st.session_state:
    st.session_state.log_book = pd.DataFrame(
        columns=["Timestamp", "Total Head Inflow (cfs)", "Total Canal Diversion (cfs)", "Tailwater Spill Balance (cfs)"]
    )

# --- READ PERSISTENT MEMORY VALUES ---
d = st.session_state.demands

# --- SIDEBAR LOCAL OVERRIDES ---
st.sidebar.markdown("## 💰 Main Canal Inflow Header")
system_opening_inflow = st.sidebar.number_input("Global Pool Inflow Balance (cfs)", value=13410.0, step=50.0)
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ Primary Pool Control Gauges")
sabarmati_cr_depth = st.sidebar.number_input("Sabarmati CR Gauge Depth (m)", value=6.40, step=0.05, format="%.3f")
jaspur_cr_depth = st.sidebar.number_input("Jaspur CR Gauge Depth (m)", value=6.70, step=0.05, format="%.3f")
karannagar_cr_depth = st.sidebar.number_input("Karannagar CR Gauge Depth (m)", value=6.85, step=0.05, format="%.3f")
st.sidebar.markdown("---")
st.sidebar.markdown("### 🏁 Downstream Boundary Condition")
next_cr_277_depth = st.sidebar.number_input("Next CR (Ch. 277.880) U/S Depth (m)", value=5.50, step=0.05, format="%.3f")

# --- DOWNSTREAM TO UPSTREAM CASCADING SUMMATION LOGIC ---
calc_jaspur_cr_demand = d["in_east_esc"] + d["in_piyaj"] + d["in_sanand"] + d["in_saurashtra"] + d["in_karannagar"] + d["in_pool3"]
calc_karai_cr_demand = d["in_gwssb"] + d["in_gift"] + d["in_syphonic"] + d["in_dholka"] + d["in_pool2"] + calc_jaspur_cr_demand
calc_khari_cr_demand = d["in_daskroi"] + d["in_amc1"] + d["in_amc2"] + d["in_sab_esc"] + d["in_pool1"] + calc_karai_cr_demand

# --- CONSOLIDATED STRUCTURE PROFILE SCHEMA ---
STRUCTURE_CONFIGS = [
    {"id": 1, "ch": "220.907", "struct": "CR", "offtake": "Khari CR (Automated Sum)", "type": "Radial", "width": 9.0, "us_cbl": 58.900, "ds_cbl": 58.900, "crest": 58.900, "gates": 5, "demand": calc_khari_cr_demand, "cd": 0.600, "depth_formula": lambda: sabarmati_cr_depth, "is_ds_controlled": False, "ds_val": 4.50},
    {"id": 2, "ch": "223.670", "struct": "NMC HR", "offtake": "Daskroi Branch Canal", "type": "Radial", "width": 2.8, "us_cbl": 58.755, "ds_cbl": 63.18, "crest": 63.44, "gates": 2, "demand": d["in_daskroi"], "cd": 0.600, "depth_formula": lambda: sabarmati_cr_depth - 0.4, "is_ds_controlled": False, "ds_val": 0.0},
    {"id": 3, "ch": "226.670", "struct": "HR - Pipeline", "offtake": "AMC-1", "type": "Vertical", "width": 2.6, "us_cbl": 58.512, "ds_cbl": 58.512, "crest": 58.512, "gates": 2, "demand": d["in_amc1"], "cd": 0.600, "depth_formula": lambda: sabarmati_cr_depth - 0.2, "is_ds_controlled": False, "ds_val": 0.0},
    {"id": 4, "ch": "228.360", "struct": "HR - Pipeline", "offtake": "AMC-2", "type": "Vertical", "width": 2.6, "us_cbl": 58.512, "ds_cbl": 58.512, "crest": 58.512, "gates": 2, "demand": d["in_amc2"], "cd": 0.600, "depth_formula": lambda: sabarmati_cr_depth - 0.1, "is_ds_controlled": False, "ds_val": 0.0},
    {"id": 5, "ch": "229.340", "struct": "Escape", "offtake": "Sabarmati Escape", "type": "Radial", "width": 5.0, "us_cbl": 58.512, "ds_cbl": 58.512, "crest": 58.512, "gates": 2, "demand": d["in_sab_esc"], "cd": 0.600, "depth_formula": lambda: sabarmati_cr_depth - 0.4, "is_ds_controlled": False, "ds_val": 0.0},
    {"id": 6, "ch": "Pool-1", "struct": "Loss Factor", "offtake": "Pool-1 Segment Loss/Gain", "type": "Static", "width": 0.0, "us_cbl": 0.0, "ds_cbl": 0.0, "crest": 0.0, "gates": 0, "demand": d["in_pool1"], "cd": 0.0, "depth_formula": lambda: 0.0, "is_ds_controlled": False, "ds_val": 0.0},
    
    {"id": 7, "ch": "229.907", "struct": "CR", "offtake": "Karai CR (Automated Sum)", "type": "Radial", "width": 7.5, "us_cbl": 57.500, "ds_cbl": 57.500, "crest": 57.500, "gates": 4, "demand": calc_karai_cr_demand, "cd": 0.600, "depth_formula": lambda: jaspur_cr_depth, "is_ds_controlled": False, "ds_val": 4.80},
    {"id": 8, "ch": "230.500", "struct": "HR - Pipeline", "offtake": "GWSSB Pipeline", "type": "Vertical", "width": 1.8, "us_cbl": 57.460, "ds_cbl": 57.460, "crest": 57.460, "gates": 4, "demand": d["in_gwssb"], "cd": 0.600, "depth_formula": lambda: jaspur_cr_depth - 1.1, "is_ds_controlled": False, "ds_val": 0.0},
    {"id": 9, "ch": "230.500", "struct": "HR - Pipeline", "offtake": "GIFT City Pipeline", "type": "Vertical", "width": 1.8, "us_cbl": 57.460, "ds_cbl": 57.460, "crest": 57.460, "gates": 4, "demand": d["in_gift"], "cd": 0.600, "depth_formula": lambda: jaspur_cr_depth - 1.1, "is_ds_controlled": False, "ds_val": 0.0},
    {"id": 10, "ch": "244.755", "struct": "HR", "offtake": "Syphonic Pipeline", "type": "Vertical", "width": 2.0, "us_cbl": 56.500, "ds_cbl": 56.500, "crest": 56.500, "gates": 2, "demand": d["in_syphonic"], "cd": 0.600, "depth_formula": lambda: jaspur_cr_depth - 0.5, "is_ds_controlled": False, "ds_val": 0.0},
    {"id": 11, "ch": "246.447", "struct": "HR", "offtake": "Dholka Branch Canal HR", "type": "Radial", "width": 5.0, "us_cbl": 56.261, "ds_cbl": 56.261, "crest": 56.261, "gates": 3, "demand": d["in_dholka"], "cd": 0.611, "depth_formula": lambda: jaspur_cr_depth, "is_ds_controlled": False, "ds_val": 3.880},
    {"id": 12, "ch": "Pool-2", "struct": "Loss Factor", "offtake": "Pool-2 Segment Loss/Gain", "type": "Static", "width": 0.0, "us_cbl": 0.0, "ds_cbl": 0.0, "crest": 0.0, "gates": 0, "demand": d["in_pool2"], "cd": 0.0, "depth_formula": lambda: 0.0, "is_ds_controlled": False, "ds_val": 0.0},
    
    {"id": 13, "ch": "246.582", "struct": "CR", "offtake": "Jaspur CR Pool (Automated Sum)", "type": "Radial", "width": 9.0, "us_cbl": 56.177, "ds_cbl": 56.177, "crest": 56.177, "gates": 9, "demand": calc_jaspur_cr_demand, "cd": 0.600, "depth_formula": lambda: jaspur_cr_depth, "is_ds_controlled": False, "ds_val": 5.020},
    {"id": 14, "ch": "255.742", "struct": "Escape", "offtake": "Eastern Drain Escape", "type": "Radial", "width": 4.5, "us_cbl": 55.100, "ds_cbl": 55.100, "crest": 55.100, "gates": 2, "demand": d["in_east_esc"], "cd": 0.600, "depth_formula": lambda: karannagar_cr_depth - 0.5, "is_ds_controlled": False, "ds_val": 0.0},
    {"id": 15, "ch": "256.220", "struct": "HR - Pipeline", "offtake": "Piyaj Dharoi Pipeline", "type": "Vertical", "width": 1.0, "us_cbl": 55.400, "ds_cbl": 55.400, "crest": 55.400, "gates": 1, "demand": d["in_piyaj"], "cd": 0.600, "depth_formula": lambda: karannagar_cr_depth - 0.5, "is_ds_controlled": False, "ds_val": 0.0},
    {"id": 16, "ch": "258.849", "struct": "HR", "offtake": "Sanand Branch Canal HR", "type": "Radial", "width": 3.5, "us_cbl": 55.100, "ds_cbl": 55.100, "crest": 55.100, "gates": 1, "demand": d["in_sanand"], "cd": 0.600, "depth_formula": lambda: karannagar_cr_depth - 0.35, "is_ds_controlled": False, "ds_val": 0.0},
    {"id": 17, "ch": "263.309", "struct": "HR", "offtake": "Saurashtra Branch Canal HR", "type": "Radial", "width": 6.0, "us_cbl": 54.988, "ds_cbl": 55.296, "crest": 56.47, "gates": 5, "demand": d["in_saurashtra"], "cd": 0.600, "depth_formula": lambda: karannagar_cr_depth - 1.5, "is_ds_controlled": False, "ds_val": 1.520},
    {"id": 18, "ch": "Pool-3", "struct": "Loss Factor", "offtake": "Pool-3 Segment Loss/Gain", "type": "Static", "width": 0.0, "us_cbl": 0.0, "ds_cbl": 0.0, "crest": 0.0, "gates": 0, "demand": d["in_pool3"], "cd": 0.0, "depth_formula": lambda: 0.0, "is_ds_controlled": False, "ds_val": 0.0},
    {"id": 19, "ch": "263.574", "struct": "CR", "offtake": "Karannagar CR", "type": "Radial", "width": 6.0, "us_cbl": 54.894, "ds_cbl": 54.894, "crest": 54.894, "gates": 5, "demand": d["in_karannagar"], "cd": 0.600, "depth_formula": lambda: karannagar_cr_depth, "is_ds_controlled": True, "ds_val": 0.0}
]

g = 9.81
current_cascade_balance = system_opening_inflow
total_canal_diversion = 0.0
tabular_summary_log = []

for row_data in STRUCTURE_CONFIGS:
    computed_us_depth = max(0.0, row_data["depth_formula"]())
    computed_ds_depth = next_cr_277_depth if row_data["is_ds_controlled"] else row_data["ds_val"]
    M16_us = row_data["us_cbl"] + computed_us_depth
    P16_ds = row_data["ds_cbl"] + computed_ds_depth
    
    if row_data["type"] == "Static":
        row_computed_discharge = row_data["demand"]
        post_row_remaining_balance = round(current_cascade_balance - row_computed_discharge, 2)
        current_cascade_balance = post_row_remaining_balance
        total_canal_diversion += row_computed_discharge
        st.warning(f"📉 **Pool Loss/Gain Factor Accounted:** Downstream allocation altered by **{row_computed_discharge} cfs**.")
        st.markdown("---")
        tabular_summary_log.append({
            "Row ID": row_data["id"], "Chainage (km)": row_data["ch"], "Regulator Reach Target": row_data["offtake"],
            "U/S RL (m)": 0.0, "D/S RL (m)": 0.0, "Total Supply Outflow (cfs)": row_computed_discharge,
            "Target Scheduled Demand (cfs)": row_data["demand"], "Available Residual Balance (cfs)": post_row_remaining_balance
        })
        continue

    with st.container():
        col_meta, col_levels, col_params, col_gates = st.columns([2.0, 1.8, 1.8, 4.4])
        with col_meta:
            st.markdown(f"**Row {row_data['id']} • Ch. {row_data['ch']} km**")
            st.write(f"⚙️ {row_data['struct']} — *{row_data['offtake']}*")
            st.caption(f"Type: {row_data['type']} | Width: {row_data['width']}m")
        with col_levels:
            st.write(f"📥 Pool In: **{current_cascade_balance:.2f} cfs**")
            st.write(f"🔼 U/S RL: `{M16_us:.3f} m`")
            st.write(f"🔽 D/S RL: `{P16_ds:.3f} m`")
        with col_params:
            row_cd = st.number_input(f"Cd", value=row_data["cd"], step=0.01, format="%.3f", key=f"tbl_cd_{row_data['id']}")
            row_demand = st.number_input(f"Demand (cfs)", value=row_data["demand"], step=5.0, key=f"tbl_dm_{row_data['id']}", disabled=True)
        with col_gates:
            st.write("🔧 Gate Structure Stroke Settings (m):")
            bay_cols = st.columns(min(row_data["gates"], 5))
            gate_openings_register = []
            for gate_index in range(row_data["gates"]):
                sub_column_idx = gate_index % 5
                with bay_cols[sub_column_idx]:
                    gate_preset = 0.55 if gate_index < 2 and row_data["id"] in [1, 2, 7, 13, 17, 19] else 0.00
                    active_go = st.number_input(f"G-{gate_index+1}", min_value=0.00, max_value=7.00, value=gate_preset, step=0.05, format="%.2f", key=f"tbl_gt_{row_data['id']}_{gate_index}")
                    gate_openings_register.append(active_go)

        row_computed_discharge = 0.0
        for gate_bay_no, Q16 in enumerate(gate_openings_register):
            if Q16 <= 0.001:
                gate_outflow_cfs = 0.0
            elif Q16 >= (M16_us - row_data["crest"]):
                head_over_crest = M16_us - row_data["crest"]
                if head_over_crest > 0:
                    discharge_cms = (2.0 / 3.0) * row_cd * row_data["width"] * math.sqrt(2 * g) * (head_over_crest ** 1.5)
                    gate_outflow_cfs = discharge_cms * 35.315
                else:
                    gate_outflow_cfs = 0.0
            else:
                if P16_ds < row_data["crest"]:
                    head_over_crest = M16_us - row_data["crest"]
                    orifice_term = (2.0 / 3.0) * row_cd * row_data["width"] * math.sqrt(2 * g) * ((head_over_crest ** 1.5) - ((head_over_crest - Q16) ** 1.5))
                    gate_outflow_cfs = orifice_term * 35.315
                else:
                    X_delta_h = M16_us - P16_ds
                    head_over_crest = M16_us - row_data["crest"]
                    if (head_over_crest - Q16) < X_delta_h:
                        part1 = (2.0 / 3.0) * row_cd * row_data["width"] * math.sqrt(2 * g) * ((X_delta_h ** 1.5) - ((head_over_crest - Q16) ** 1.5))
                        submerged_depth_hd = P16_ds - row_data["crest"]
                        part2 = row_cd * row_data["width"] * submerged_depth_hd * math.sqrt(2 * g * X_delta_h)
                        gate_outflow_cfs = (part1 + part2) * 35.315
                    else:
                        submerged_ans = row_cd * row_data["width"] * Q16 * math.sqrt(2 * g * X_delta_h)
                        gate_outflow_cfs = submerged_ans * 35.315
            row_computed_discharge += max(0.0, gate_outflow_cfs)

        row_computed_discharge = round(row_computed_discharge, 2)
        post_row_remaining_balance = round(current_cascade_balance - row_computed_discharge, 2)
        row_performance_imbalance = round(row_computed_discharge - row_demand, 2)
        current_cascade_balance = post_row_remaining_balance
        total_canal_diversion += row_computed_discharge
        
        st.write(f"🚀 Outflow (AS): **{row_computed_discharge} cfs** | Target: `{row_demand} cfs` | Delta Imbalance: `{row_performance_imbalance} cfs` | 🔄 Post-Structure Pool: **{post_row_remaining_balance} cfs**")
        st.markdown("---")
        tabular_summary_log.append({
            "Row ID": row_data["id"], "Chainage (km)": row_data["ch"], "Regulator Reach Target": f"{row_data['struct']} ({row_data['offtake']})",
            "U/S RL (m)": round(M16_us, 3), "D/S RL (m)": round(P16_ds, 3), "Total Supply Outflow (cfs)": row_computed_discharge,
            "Target Scheduled Demand (cfs)": row_demand, "Available Residual Balance (cfs)": post_row_remaining_balance
        })

# --- GLOBAL SUMMARY METRICS ---
st.markdown("### 📊 Combined System Operations Summary Log")
m1, m2, m3 = st.columns(3)
m1.metric("📥 Main System Head Inflow", f"{system_opening_inflow} cfs")
m2.metric("🚒 Combined Diversion Outflow", f"{round(total_canal_diversion, 2)} cfs")
m3.metric("🏁 Terminal Spill Discharge Balance", f"{round(current_cascade_balance, 2)} cfs")

st.markdown("### 📋 Unified Flow Accounting Grid Ledger")
st.dataframe(pd.DataFrame(tabular_summary_log), use_container_width=True)
