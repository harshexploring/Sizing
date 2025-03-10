import pandas as pd
import numpy as np
import os



def process_bess_data(config, input_df):
    # Extract parameters from config dictionary
    bess_power = config['bess_power']
    bess_hours = config['bess_hours']
    bess_DOD = float(config['bess_DOD']) 
    bess_RTE = float(config['bess_RTE'])
    bess_total_capacity = bess_power * bess_hours




    # Initialize arrays for faster computation
    charge = np.zeros(len(input_df))
    discharge = np.zeros(len(input_df))
    soc = np.full(len(input_df), bess_DOD)

    for i in range(0, len(input_df)):
        prev_soc = soc[i-1]  # Previous SOC

        # Vectorized charge and discharge calculations
        charge_possible = min(bess_power, input_df['Surplus'].iloc[i] * bess_RTE, (100 - prev_soc) * bess_total_capacity / 100)
        charge[i] = max(0.0, charge_possible)

        discharge_possible = min(bess_power * bess_RTE, input_df['Deficit'].iloc[i], (prev_soc - bess_DOD) * bess_total_capacity * bess_RTE / 100)
        discharge[i] = max(0.0, discharge_possible)

        # Update SOC (Vectorized)
        soc[i] = max(bess_DOD, prev_soc + (charge[i] / bess_total_capacity) * 100 - (discharge[i] / (bess_RTE * bess_total_capacity)) * 100)

    # Assign arrays back to DataFrame
    input_df['Charge'] = charge
    input_df['Discharge'] = discharge
    input_df['SOC'] = soc

    input_df['Deficit_after_bess'] = input_df['Deficit'] - input_df['Discharge']
    input_df['Deficit_after_bess'] = input_df['Deficit_after_bess'].clip(lower=0)

    input_df['Surplus_after_bess'] = input_df['Surplus'] - input_df['Charge']
    input_df['Surplus_after_bess'] = input_df['Surplus_after_bess'].clip(lower=0)

    return input_df


def analysis(config, df , month_details_df):
    
    bess_power = config['bess_power']
    bess_hours = config['bess_hours']
    bess_DOD = config['bess_DOD']
    bess_RTE = config['bess_RTE']
    bess_total_capacity = bess_power * bess_hours

    total_discharge = df['Discharge'].sum()
    
    effective_cycles = total_discharge / (bess_total_capacity * 365 * bess_RTE)

    total_deficit = df['Deficit'].sum()/1000
    total_surplus = df['Surplus'].sum()/1000
    
    total_load = df['Load'].sum()/1000
    total_load_met_by_plant = df['Load Met By Plant'].sum()/1000
    total_bess_consumption = (df['Deficit'] - df['Deficit_after_bess']).sum()/1000

    bess_penetration = (total_bess_consumption / total_load)  * 100
    plant_penetration = (total_load_met_by_plant / total_load) * 100

    RE_penetration = ((total_load_met_by_plant + total_bess_consumption) / total_load) * 100

    total_surplus_after_bess = df['Surplus_after_bess'].sum()/1000
    total_deficit_after_bess = df['Deficit_after_bess'].sum()/1000

    # Monthwise analysis..........................................................................
    monthwise_data = df.groupby('Month').agg({
        'Load': 'sum',
        'Generation_Plant_Periphery': 'sum',
        'Surplus': 'sum',
        'Deficit': 'sum',
        'Surplus_after_bess': 'sum',
        'Deficit_after_bess': 'sum',    
        })/1000

    monthwise_battery_cycles = df.groupby('Month')['Discharge'].sum() / (bess_total_capacity * bess_RTE)
    monthwise_effective_battery_cycles = monthwise_battery_cycles/month_details_df['Size'] 
    monthwise_utilization = monthwise_effective_battery_cycles * 100

    monthwise_combined = pd.concat([
        monthwise_data,
        monthwise_battery_cycles.rename("Battery_Cycles"),
        monthwise_effective_battery_cycles.rename("Effective_Battery_Cycles"),
        monthwise_utilization.rename("Utilization")
    ], axis=1)
    
    #Monthwise slotwise analysis.....................................................................
    monthwise_slotwise_battery_analysis = df.groupby(['Month','Slots']).agg({
        'Load': 'mean',
        'Generation_Plant_Periphery': 'mean',
        'Charge': 'mean',
        'Discharge': 'mean'
        })

    #Exporting the data.... 
    data = {
        "Total_Load(in MUs)": total_load,
        "Total_Surplus(in MUs)": total_surplus,
        "Total_Deficit(in MUs)": total_deficit,
        "Total_Load_Met_By_Plant(in MUs)": total_load_met_by_plant,
        "Total_BESS_Consumption(in MUs)": total_bess_consumption,
        "BESS_Penetration(in %)": bess_penetration,
        "Plant_Penetration(in %)": plant_penetration,
        "RE_Penetration(in %)": RE_penetration,

        "Total_Surplus_After_BESS(in MUs)": total_surplus_after_bess,
        "Total_Deficit_After_BESS(in MUs)": total_deficit_after_bess,

        "Effective_Cycles": effective_cycles,

        "Monthwise_Data": monthwise_combined,

        "Monthwise_Slotwise_Battery_Analysis": monthwise_slotwise_battery_analysis
    }
    return data


# Main execution
def run_heatmap_analysis_model(config, input_df, month_details_df):

    bess_hour , start, end , step, bess_rte , bess_dod = config
    bess_power_range = range(start, end + 1, step)  # 5 to 105 with step 10
    data = {}



    
    input_df['Surplus'] = np.maximum(input_df['Generation_Plant_Periphery'] - input_df['Load'], 0)
    input_df['Deficit'] = np.maximum(input_df['Load'] - input_df['Generation_Plant_Periphery'], 0)
    input_df['Load Met By Plant'] = np.minimum(input_df['Generation_Plant_Periphery'], input_df['Load'])
    

    print(f"For bess_hour: {bess_hour}")


    heat_map_df = pd.DataFrame(index=bess_power_range, columns=[
    "Total_Load(in MUs)", "Total_Surplus(in MUs)", "Total_Deficit(in MUs)", 
    "Total_Load_Met_By_Plant(in MUs)", "Total_BESS_Consumption(in MUs)", 
    "BESS_Penetration(in %)", "Plant_Penetration(in %)", "RE_Penetration(in %)", "Total_Surplus_After_BESS(in MUs)","Total_Deficit_After_BESS(in MUs)","Effective_Cycles"
    ])

    for bess_power in bess_power_range:
        config = {
            'bess_power': float(bess_power),
            'bess_hours': float(bess_hour),
            'bess_DOD': bess_dod, # 10% depth of discharge
            'bess_RTE': bess_rte  # 85% round trip efficiency
        }
        #step1: Preparing the dataframe
        
        result_df = process_bess_data(config, input_df.copy())  # Pass a copy to avoid modifying the original DF
        
        #Step2: Analyzing the dataframe
        analysis_results = analysis(config, result_df,month_details_df)

        for key in heat_map_df.columns:
            heat_map_df.loc[bess_power, key] = analysis_results[key]

        
        

    return heat_map_df
               

