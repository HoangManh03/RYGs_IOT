#11:01 24 jun 2024
import tkinter as tk
from tkinter import ttk

g_real_points = []

class RealCoordinatesInput:
    def __init__(self, root):
        self.root = root
        self.root.title("Real Coordinates Input")
        
        self.quadrilaterals = []

        for i in range(4):
            self.add_ponits_inputs(i + 1)
        
        self.save_button = ttk.Button(self.root, text="SAVE", command=self.save)
        self.save_button.grid(row=4, column=0, columnspan=9, pady=10)
        
        self.output_label = ttk.Label(self.root, text="")
        self.output_label.grid(row=5, column=0, columnspan=9, pady=10)

    def add_ponits_inputs(self, quad_number):
        label = ttk.Label(self.root, text=f"Traffic Light {quad_number}")
        label.grid(row=quad_number-1, column=0, padx=5, pady=5)

        x1_label = ttk.Label(self.root, text="x1")
        x1_label.grid(row=quad_number-1, column=1, padx=2, pady=5)
        x1_entry = ttk.Entry(self.root, width=5)
        x1_entry.grid(row=quad_number-1, column=2, padx=2, pady=5)

        y1_label = ttk.Label(self.root, text="y1")
        y1_label.grid(row=quad_number-1, column=3, padx=2, pady=5)
        y1_entry = ttk.Entry(self.root, width=5)
        y1_entry.grid(row=quad_number-1, column=4, padx=2, pady=5)

        x2_label = ttk.Label(self.root, text="x2")
        x2_label.grid(row=quad_number-1, column=5, padx=2, pady=5)
        x2_entry = ttk.Entry(self.root, width=5)
        x2_entry.grid(row=quad_number-1, column=6, padx=2, pady=5)

        y2_label = ttk.Label(self.root, text="y2")
        y2_label.grid(row=quad_number-1, column=7, padx=2, pady=5)
        y2_entry = ttk.Entry(self.root, width=5)
        y2_entry.grid(row=quad_number-1, column=8, padx=2, pady=5)

        x3_label = ttk.Label(self.root, text="x3")
        x3_label.grid(row=quad_number-1, column=9, padx=2, pady=5)
        x3_entry = ttk.Entry(self.root, width=5)
        x3_entry.grid(row=quad_number-1, column=10, padx=2, pady=5)

        y3_label = ttk.Label(self.root, text="y3")
        y3_label.grid(row=quad_number-1, column=11, padx=2, pady=5)
        y3_entry = ttk.Entry(self.root, width=5)
        y3_entry.grid(row=quad_number-1, column=12, padx=2, pady=5)

        x4_label = ttk.Label(self.root, text="x4")
        x4_label.grid(row=quad_number-1, column=13, padx=2, pady=5)
        x4_entry = ttk.Entry(self.root, width=5)
        x4_entry.grid(row=quad_number-1, column=14, padx=2, pady=5)

        y4_label = ttk.Label(self.root, text="y4")
        y4_label.grid(row=quad_number-1, column=15, padx=2, pady=5)
        y4_entry = ttk.Entry(self.root, width=5)
        y4_entry.grid(row=quad_number-1, column=16, padx=2, pady=5)

        self.quadrilaterals.append((x1_entry, y1_entry, x2_entry, y2_entry, x3_entry, y3_entry, x4_entry, y4_entry))

    def save(self):
        global g_real_points
        g_real_points = []
        for entries in self.quadrilaterals:
            quad_coords = [entry.get() for entry in entries]
            g_real_points.append(quad_coords)

        self.output_label.config(text=f"Coordinates is saved")

def RealCoordinatesInputApp():
    global g_real_points
    root = tk.Tk()
    app = RealCoordinatesInput(root)
    root.mainloop()
    return g_real_points

if __name__ == "__main__":
    RealCoordinatesInputApp()