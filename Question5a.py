import tkinter as tk
from tkinter import messagebox
import json
import math
import matplotlib.pyplot as plt
import itertools
import time

# --- TASK 2: Load/Define Tourist Spot Dataset (3 Marks) ---
def get_dataset():
    data = """
    [
        {"name": "Pashupatinath Temple", "lat": 27.7104, "lon": 85.3488, "fee": 100, "tags": ["culture", "religious"]},
        {"name": "Swayambhunath Stupa", "lat": 27.7149, "lon": 85.2906, "fee": 200, "tags": ["culture", "heritage"]},
        {"name": "Garden of Dreams", "lat": 27.7125, "lon": 85.3170, "fee": 150, "tags": ["nature", "relaxation"]},
        {"name": "Chandragiri Hills", "lat": 27.6616, "lon": 85.2458, "fee": 700, "tags": ["nature", "adventure"]},
        {"name": "Kathmandu Durbar Square", "lat": 27.7048, "lon": 85.3076, "fee": 100, "tags": ["culture", "heritage"]}
    ]
    """
    return json.loads(data)

# --- TASK 3: Heuristic Optimization Logic (5 Marks) ---
def greedy_itinerary(dataset, max_time, max_budget, interests):
    current_pos = (27.7172, 85.3240) 
    itinerary = []
    time_left = max_time
    budget_left = max_budget
    available = [s for s in dataset if any(t in s['tags'] for t in interests)]
    
    while available and time_left >= 2.5:
        # Heuristic: Pick the nearest neighbor
        available.sort(key=lambda s: math.sqrt((s['lat']-current_pos[0])**2 + (s['lon']-current_pos[1])**2))
        
        best_next = None
        for spot in available:
            if spot['fee'] <= budget_left:
                best_next = spot
                break
        
        if not best_next: break
        
        itinerary.append(best_next)
        budget_left -= best_next['fee']
        time_left -= 2.5 
        current_pos = (best_next['lat'], best_next['lon'])
        available.remove(best_next)
        
    return itinerary, max_budget - budget_left, max_time - time_left

# --- TASK 5: Brute-Force Comparison (4 Marks) ---
def run_comparison(dataset, budget):
    # Heuristic performance
    start_h = time.time()
    greedy_itinerary(dataset, 10, budget, ["culture", "nature"])
    end_h = time.time()

    # Brute Force performance
    start_b = time.time()
    valid_spots = [s for s in dataset if s['fee'] <= budget]
    # Check all permutations (O(n!))
    list(itertools.permutations(valid_spots))
    end_b = time.time()
    
    return (end_h - start_h), (end_b - start_b)

# --- TASK 1: GUI Design (3 Marks) ---
class TouristApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tourist Spot Optimizer")
        self.root.geometry("400x450")

        tk.Label(root, text="Total Time (Hours):", font=('Arial', 10, 'bold')).pack(pady=5)
        self.time_entry = tk.Entry(root)
        self.time_entry.insert(0, "10")
        self.time_entry.pack()

        tk.Label(root, text="Max Budget (Rs):", font=('Arial', 10, 'bold')).pack(pady=5)
        self.budget_entry = tk.Entry(root)
        self.budget_entry.insert(0, "1000")
        self.budget_entry.pack()

        tk.Label(root, text="Interests:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.culture_var = tk.BooleanVar(value=True)
        self.nature_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Culture", variable=self.culture_var).pack()
        tk.Checkbutton(root, text="Nature", variable=self.nature_var).pack()

        self.btn = tk.Button(root, text="GENERATE ITINERARY", command=self.solve, bg="blue", fg="black", height=2)
        self.btn.pack(pady=20)

    # --- TASK 4: Result Display & Visualization (5 Marks) ---
    def solve(self):
        budget = int(self.budget_entry.get())
        t_limit = int(self.time_entry.get())
        interests = []
        if self.culture_var.get(): interests.append("culture")
        if self.nature_var.get(): interests.append("nature")

        data = get_dataset()
        path, cost, used_time = greedy_itinerary(data, t_limit, budget, interests)
        h_time, b_time = run_comparison(data, budget)

        # Text Summary
        path_names = [s['name'] for s in path]
        summary = (f"--- ITINERARY ---\n"
                   f"Sequence: {' -> '.join(path_names)}\n\n"
                   f"Total Cost: Rs {cost}\n"
                   f"Total Time: {used_time} hrs\n\n"
                   f"--- PERFORMANCE ---\n"
                   f"Heuristic Time: {h_time:.6f}s\n"
                   f"Brute-Force Time: {b_time:.6f}s")
        
        messagebox.showinfo("Optimization Results", summary)

        # Path Visualization
        if path:
            lons = [s['lon'] for s in path]
            lats = [s['lat'] for s in path]
            plt.figure("Travel Sequence Map")
            plt.plot(lons, lats, 'ro-', linewidth=2, markersize=8)
            for i, s in enumerate(path):
                plt.text(s['lon'], s['lat'], f"{i+1}. {s['name']}", fontsize=9)
            plt.title("Heuristic Path (Greedy Nearest Neighbor)")
            plt.grid(True)
            plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = TouristApp(root)
    root.mainloop()