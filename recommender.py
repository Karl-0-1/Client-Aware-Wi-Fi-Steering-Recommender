import pandas as pd

# Define the minimum RSSI improvement (in dB) to trigger a steer
RSSI_IMPROVEMENT_THRESHOLD = 15

def find_steering_candidates(row):
    """
    Analyzes a single client's report (a DataFrame row) to find a 
    potential steering opportunity.
    """
    client_id = row['client_id']
    current_ap = row['connected_ap']
    current_rssi = row['client_rssi']
    
    # List of (ap_name, ap_rssi) tuples for all neighbors
    neighbors = [
        (row['neighbor_ap_1'], row['neighbor_rssi_1']),
        (row['neighbor_ap_2'], row['neighbor_rssi_2'])
    ]
    
    best_target_ap = None
    best_improvement = 0
    
    # Evaluate all potential neighbors
    for ap_name, rssi in neighbors:
        # Don't steer to the same AP
        if ap_name == current_ap:
            continue
            
        improvement = rssi - current_rssi
        
        # Check if this neighbor is a valid candidate and better than any other we've found
        if improvement >= RSSI_IMPROVEMENT_THRESHOLD and improvement > best_improvement:
            best_improvement = improvement
            best_target_ap = ap_name
            
    # If we found a suitable target, create a recommendation string
    if best_target_ap:
        return (
            f"Recommend steering {client_id} to {best_target_ap} "
            f"(Reason: +{best_improvement}dB RSSI improvement over {current_ap})."
        )
        
    return None

def main():
    """
    Main function to load data, analyze, and print recommendations.
    """
    try:
        df = pd.read_csv('client_reports.csv')
    except FileNotFoundError:
        print("Error: 'client_reports.csv' not found.")
        print("Please run 'generate_data.py' first to create the file.")
        return

    df['recommendation'] = df.apply(find_steering_candidates, axis=1)
    
    # Filter the DataFrame to get only the rows that produced a recommendation
    final_recommendations = df['recommendation'].dropna().tolist()
    
    print("--- Client-Aware Steering Recommender ---")
    if final_recommendations:
        print(f"\nFound {len(final_recommendations)} steering opportunities:\n")
        for rec in final_recommendations:
            print(f"  -> {rec}")
    else:
        print("\nAll clients appear to be optimally connected.")
        print("No steering recommendations at this time.")

if __name__ == "__main__":
    main()
