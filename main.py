
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from Models.Heat_Map_Analysis import run_heatmap_analysis_model
from Models.Individual_Bess_Analysis import run_individual_bess_analysis_model
# Custom Navbar
st.title("BESS Sizing Model")


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
        background-color: white !important;
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
# monthly_details_file = st.sidebar.file_uploader("Upload the monthly details file", type=["xlsx", "xls"], key="2")

if bess_input_file :

    bess_input_df = pd.read_excel(bess_input_file)

    monthly_details_path = './Input/month_details_input.xlsx'
    monthly_details_df = pd.read_excel(monthly_details_path)
    monthly_details_df.set_index("Month", inplace=True)
    print(monthly_details_df)

    rte = st.number_input("Enter the RTE",value=0.85)
    dod = st.number_input("Enter the DOD in %",value=10)

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

        config = [hours , start , end , step , rte , dod]

        # Run Model button
        if st.button("Run Model"):
            heat_map_df = run_heatmap_analysis_model(config, bess_input_df, monthly_details_df)

            output = BytesIO()
            with pd.ExcelWriter(output) as writer:
                
               
                heat_map_df.to_excel(writer, sheet_name="HeatMap", index=True)
                
            excel_data = output.getvalue()
           
            # Create a download button
            download_file_name = 'Heat_Map_Results_{hours}_hours.xlsx'
            download_file_name = download_file_name.format(hours=hours)

            st.download_button(
                label="Download HeatMap Results",
                data=excel_data,
                file_name = download_file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )





            st.dataframe(heat_map_df)
            fig, ax = plt.subplots(figsize=(7, 3))  # Adjust width and height
            ax.plot(heat_map_df.index, heat_map_df["Effective_Cycles"], marker="o", linestyle="-", label="Effective BESS Cycle")

            ax.set_xlabel("Index")
            ax.set_ylabel("Effective Cycles")
            ax.set_title("Effective BESS Cycles Over Time")

            st.pyplot(fig)

    elif st.session_state.button_clicked == "bess_analysis":
        st.write("### Please fill in the inputs for the Individual BESS Analysis")
        
        hours = st.number_input("Enter the BESS Hours" , value=4)
        bess_power = st.number_input("Enter the BESS Capacity in MW" ,  value=100)

        # Placeholder for running the model (Add your function here)
        if st.button("Run Model"):
            st.write("Running the model for the following configuration:")
            st.write(f"BESS Hours: {hours}")
            st.write(f"BESS Power: {bess_power} MW")

            config = [hours, bess_power, rte, dod]

            data = run_individual_bess_analysis_model(config , bess_input_df, monthly_details_df)


            output = BytesIO()
            with pd.ExcelWriter(output) as writer:
                # Sheet 1: Summary
                summary_df = pd.DataFrame(list(data.items())[:10], columns=["Heading", "Value"])
                summary_df.to_excel(writer, sheet_name="Summary", index=False)
                
                # Sheet 2: Monthwise Combined Data
                data["Monthwise_Data"].to_excel(writer, sheet_name="Monthwise_Combined")
                
                # Sheets 3-14: Monthwise Slotwise Battery Analysis
                for month in range(1, 13):
                    month_df = data["Monthwise_Slotwise_Battery_Analysis"].xs(month, level="Month")
                    month_df.to_excel(writer, sheet_name=str(month))

            
            excel_data = output.getvalue()
           
            # Create a download button
            download_file_name = 'bess_{hours}_hour_{bess_power}_MW_Results.xlsx'
            download_file_name = download_file_name.format(hours=hours, bess_power=bess_power)

            st.download_button(
                label="Download Results",
                data=excel_data,
                file_name = download_file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


            summary_df = pd.DataFrame(list(data.items())[:10], columns=["Heading", "Value"])
            st.write(" Summary for the analysis is as follows: ")
            st.dataframe(summary_df)

            monthwise_data_df = data["Monthwise_Data"]
            st.write(" Monthwise aggregated data for the analysis is as follows: ")
            st.dataframe(monthwise_data_df)




            