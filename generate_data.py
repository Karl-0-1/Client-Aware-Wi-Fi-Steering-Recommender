import pandas as pd
import numpy as np
import random

N_ROWS = 100
N_BAD_SCENARIOS = 15
AP_LIST = ['AP_Lobby', 'AP_ConfRoom_1', 'AP_Floor1_East', 'AP_Floor1_West', 'AP_BreakRoom']

data = []

# --- Create Normal Scenarios ---
n_normal = N_ROWS - N_BAD_SCENARIOS
for i in range(n_normal):
    data.append({
        'client_id': f'client_{i:03d}',
        'connected_ap': np.random.choice(AP_LIST),
        'client_rssi': np.random.randint(-75, -50),
        'neighbor_ap_1': np.random.choice(AP_LIST),
        'neighbor_rssi_1': np.random.randint(-90, -60),
        'neighbor_ap_2': np.random.choice(AP_LIST),
        'neighbor_rssi_2': np.random.randint(-90, -60),
    })

# --- Create "Bad" Scenarios (Steering Candidates) ---
for i in range(n_normal, N_ROWS):
    current_ap = np.random.choice(AP_LIST)
    neighbor_ap = np.random.choice([ap for ap in AP_LIST if ap != current_ap])
    
    data.append({
        'client_id': f'client_{i:03d}',
        'connected_ap': current_ap,
        'client_rssi': np.random.randint(-90, -75),
        'neighbor_ap_1': neighbor_ap,
        'neighbor_rssi_1': np.random.randint(-65, -50),
        'neighbor_ap_2': np.random.choice(AP_LIST),
        'neighbor_rssi_2': np.random.randint(-90, -70),
    })

# Create DataFrame and shuffle it
df = pd.DataFrame(data)
df = df.sample(frac=1).reset_index(drop=True)

# --- CORRECTED CONFLICT FIX ---
# Loop through each row to fix conflicts individually.
# This is safer and avoids the empty list error.
for index, row in df.iterrows():
    # Get the AP this client is connected to
    current_ap = row['connected_ap']
    
    # Create a list of all *other* APs
    possible_neighbors = [ap for ap in AP_LIST if ap != current_ap]

    # Check neighbor 1: if it's the same as the current AP, pick a new one
    if row['neighbor_ap_1'] == current_ap:
        df.at[index, 'neighbor_ap_1'] = np.random.choice(possible_neighbors)
        
    # Check neighbor 2: if it's the same as the current AP, pick a new one
    if row['neighbor_ap_2'] == current_ap:
        df.at[index, 'neighbor_ap_2'] = np.random.choice(possible_neighbors)

# Save to CSV
df.to_csv('client_reports.csv', index=False)

print(f"Successfully generated 'client_reports.csv' with {N_ROWS} records.")
print("\nSample Data:")
print(df.head())
