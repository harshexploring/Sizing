
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from Models.Heat_Map_Analysis import run_heatmap_analysis_model

# Custom Navbar
st.title("Ultratech Sizing Model")


st.markdown("""
    <style>
    .stButton>button {
        width: 100%;  /* Make buttons fill the column */
        padding: 10px;
        font-size: 16px;
        border-radius: 5px;
        border: none;
    }
    .stButton>button:hover {
        opacity: 0.85;
    }
    .selected-btn {
        background-color: red !important;
        color: white !important;
    }
    .default-btn {
        background-color: #1f77b4 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = None

# Define button click functions
def heatmap_analysis():
    st.session_state.button_clicked = "heatmap"

def individual_bess_analysis():
    st.session_state.button_clicked = "bess_analysis"

# Sidebar file uploads
bess_input_file = st.sidebar.file_uploader("Upload the slotwise demand, generation file", type=["xlsx", "xls"], key="1")
monthly_details_file = st.sidebar.file_uploader("Upload the monthly details file", type=["xlsx", "xls"], key="2")

if bess_input_file and monthly_details_file:

    bess_input_df = pd.read_excel(bess_input_file)
    monthly_details_df = pd.read_excel(monthly_details_file)
    monthly_details_df.set_index("Month", inplace=True)

    # Buttons to select the model
    col1, col2 = st.columns(2)

    with col1:
        btn_style = "selected-btn" if st.session_state.button_clicked == "heatmap" else "default-btn"
        if st.button("Heat Map Analysis", key="heatmap_button", on_click=heatmap_analysis):
            pass
        st.markdown(f'<script>document.querySelector("[key=heatmap_button] button").className = "{btn_style}";</script>', unsafe_allow_html=True)

    with col2:
        btn_style = "selected-btn" if st.session_state.button_clicked == "bess_analysis" else "default-btn"
        if st.button("Individual Bess Analysis", key="bess_button", on_click=individual_bess_analysis):
            pass
        st.markdown(f'<script>document.querySelector("[key=bess_button] button").className = "{btn_style}";</script>', unsafe_allow_html=True)

    # Display the selected section
    if st.session_state.button_clicked == "heatmap":

        st.write("### Please fill in the inputs for the Heat Map Analysis")


        hours = st.text_input("Enter the BESS Hours",value=4)
        start = st.number_input("Enter the start range",value=5)
        end = st.number_input("Enter the end range", value=106)
        step = st.number_input("Enter the step range",value=10)

        hours = int(hours)
        start = int(start)
        end = int(end)  
        step = int(step)

        # Run Model button
        if st.button("Run Model"):
            heat_map_df = run_heatmap_analysis_model(hours, start, end, step, bess_input_df, monthly_details_df)
            st.dataframe(heat_map_df)
            fig, ax = plt.subplots(figsize=(7, 3))  # Adjust width and height
            ax.plot(heat_map_df.index, heat_map_df["Effective_Cycles"], marker="o", linestyle="-", label="Effective BESS Cycle")

            ax.set_xlabel("Index")
            ax.set_ylabel("Effective Cycles")
            ax.set_title("Effective BESS Cycles Over Time")

            st.pyplot(fig)

    elif st.session_state.button_clicked == "bess_analysis":
        st.write("### Please fill in the inputs for the Individual BESS Analysis")

        hours = st.number_input("Enter the BESS Hours")
        bess_power = st.number_input("Enter the BESS Capacity in MW")

        # Placeholder for running the model (Add your function here)
        if st.button("Run Model"):
            st.write("Running Individual BESS Analysis...")
