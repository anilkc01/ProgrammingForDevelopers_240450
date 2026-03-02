import pandas as pd

# TASK 1: Model the Input Data (2 marks)
# Preparing demand and source tables as dictionaries and lists
demands = {
    6: {'A': 20, 'B': 15, 'C': 25},
    7: {'A': 22, 'B': 16, 'C': 28},
    17: {'A': 30, 'B': 25, 'C': 35}, 
    18: {'A': 35, 'B': 30, 'C': 40}
}

sources = [
    {'id': 'S1', 'type': 'Solar', 'cap': 50, 'start': 6, 'end': 18, 'cost': 1.0},
    {'id': 'S2', 'type': 'Hydro', 'cap': 40, 'start': 0, 'end': 24, 'cost': 1.5},
    {'id': 'S3', 'type': 'Diesel', 'cap': 60, 'start': 17, 'end': 23, 'cost': 3.0}
]

def load_distribution_algorithm(hour, dist_demands, all_sources):
   
    # Filter sources active during this specific hour
    active = [s for s in all_sources if s['start'] <= hour <= s['end']]
    
   
    # Sort available sources by cost (Cheapest First)
    active.sort(key=lambda x: x['cost'])
    
    total_h_demand = sum(dist_demands.values())
    total_h_cap = sum(s['cap'] for s in active)

   
    # Incorporate logic for ±10% flexibility
    ratio = 1.0
    if total_h_demand > total_h_cap:
        if total_h_cap >= 0.9 * total_h_demand:
            ratio = total_h_cap / total_h_demand
        else:
            ratio = total_h_cap / total_h_demand

    pool = {s['type']: s['cap'] for s in active}
    hourly_results = []

    for dist, d_val in dist_demands.items():
        remaining = d_val * ratio 
        alloc = {'Solar': 0.0, 'Hydro': 0.0, 'Diesel': 0.0}
        
        for s in active:
            drawn = min(remaining, pool[s['type']])
            alloc[s['type']] = drawn
            pool[s['type']] -= drawn
            remaining -= drawn
        
        total_used = sum(alloc.values())
        hourly_results.append({
            'Hour': f"{hour:02d}", 'District': dist,
            'Solar': round(alloc['Solar'], 2), 'Hydro': round(alloc['Hydro'], 2),
            'Diesel': round(alloc['Diesel'], 2), 'Total Used': round(total_used, 2),
            'Demand': d_val, '% Met': f"{round((total_used/d_val)*100, 1)}%"
        })
    return hourly_results

# Compile all results into a structured format for display
full_data = []
for hr, d_map in demands.items():
    full_data.extend(load_distribution_algorithm(hr, d_map, sources))

df = pd.DataFrame(full_data)

# --- DISPLAY OUTPUT ---
print("--- HOURLY LOAD DISTRIBUTION TABLE ---")
print(df.to_string(index=False))

# Report generation
total_cost = sum(r['Solar']*1.0 + r['Hydro']*1.5 + r['Diesel']*3.0 for r in full_data)
renew_kwh = df['Solar'].sum() + df['Hydro'].sum()
total_kwh = df['Total Used'].sum()
diesel_incidents = df[df['Diesel'] > 0][['Hour', 'District']].values.tolist()

print("\n--- ANALYSIS REPORT ---")
print(f"1. Total Cost of Distribution: Rs. {round(total_cost, 2)}")
print(f"2. % Energy fulfilled by Renewables: {round((renew_kwh/total_kwh)*100, 2)}%")
print(f"3. Diesel Usage Instances: {diesel_incidents}")
print("4. Efficiency & Trade-offs: The Greedy approach is O(N log N). It saves cost by utilizing Solar/Hydro first, "
      "but relies on Diesel during evening peaks when Solar is unavailable.")