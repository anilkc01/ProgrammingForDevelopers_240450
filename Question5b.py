import tkinter as tk
from tkinter import ttk, messagebox
import threading
import requests
import time
import queue
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Configuration (Task 2) ---
API_KEY = "fb9624ee51c4809a9be17ddcc6e9501a"
CITIES = ["Kathmandu", "Pokhara", "Biratnagar", "Nepalgunj", "Dhangadhi"]

class WeatherFinalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Final Task: Threading & Latency")
        self.root.geometry("800x700")
        
        # TASK 4: Thread-safe Queue
        self.result_queue = queue.Queue()
        
        self.setup_gui()
        self.check_queue() # Start the background queue monitor

    def setup_gui(self):
        # Task 1: GUI Table
        tk.Label(self.root, text="Weather Performance Analyzer", font=("Arial", 14, "bold")).pack(pady=10)
        
        cols = ("City", "Temp", "Humidity", "Pressure")
        self.tree = ttk.Treeview(self.root, columns=cols, show='headings', height=5)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(pady=10)

        self.btn = tk.Button(self.root, text="COMPARE LATENCY", command=self.start_analysis, 
                             bg="white", fg="black", font=("Arial", 10, "bold"))
        self.btn.pack(pady=5)

        self.status = tk.Label(self.root, text="Ready", fg="green")
        self.status.pack()

        # Task 5: Plotting Area
        self.chart_frame = tk.Frame(self.root)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    def fetch_data(self, city):
        """Standard Step 2 fetching logic."""
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                d = r.json()
                return (city, f"{d['main']['temp']}°C", f"{d['main']['humidity']}%", f"{d['main']['pressure']} hPa")
        except: pass
        return (city, "Error", "Error", "Error")

    # --- TASK 4: Thread-Safe Update Mechanism ---
    def check_queue(self):
        """Checks the queue for data every 100ms (Main Thread Only)."""
        try:
            while True:
                data = self.result_queue.get_nowait()
                if data == "FINISH":
                    self.status.config(text="Fetch Complete")
                elif isinstance(data, tuple) and len(data) == 4:
                    self.tree.insert("", "end", values=data)
        except queue.Empty:
            pass
        self.root.after(100, self.check_queue)

    # --- TASK 5: Latency Logic ---
    def start_analysis(self):
        self.btn.config(state=tk.DISABLED)
        self.tree.delete(*self.tree.get_children())
        threading.Thread(target=self.run_benchmark, daemon=True).start()

    def run_benchmark(self):
        # 1. Sequential Fetching
        self.status.config(text="Running Sequential Fetch...")
        start_seq = time.time()
        for city in CITIES:
            self.fetch_data(city)
        seq_time = time.time() - start_seq

        # 2. Parallel Fetching (Task 3 & 4)
        self.status.config(text="Running Parallel Fetch...")
        start_par = time.time()
        threads = []
        for city in CITIES:
            t = threading.Thread(target=lambda c=city: self.result_queue.put(self.fetch_data(c)))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        par_time = time.time() - start_par
        
        self.result_queue.put("FINISH")
        # Update Chart in Main Thread
        self.root.after(0, lambda: self.plot_chart(seq_time, par_time))

    def plot_chart(self, seq, par):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(["Sequential", "Parallel"], [seq, par], color=['#e74c3c', '#2ecc71'])
        ax.set_ylabel("Seconds")
        ax.set_title("Latency: Sequential vs Multithreaded")
        
        # Add labels on bars
        ax.text(0, seq, f"{seq:.2f}s", ha='center', va='bottom')
        ax.text(1, par, f"{par:.2f}s", ha='center', va='bottom')

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        self.btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherFinalApp(root)
    root.mainloop()