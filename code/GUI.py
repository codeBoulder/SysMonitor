import tkinter as tk
import os

stats_type = []
colors = []

# Creating window
root = tk.Tk()
root.title("System stats")
root.geometry("350x200")

# Add label with instruction
label = tk.Label(root, text="Choose the stats you need:", font=("Arial", 12))
label.pack()

stats_frame = tk.Frame(root)
stats_frame.pack(pady=10)

# Creating radiobuttons with stats tyypes
checked_cpu = tk.BooleanVar()
checked_ram = tk.BooleanVar()
checked_disk = tk.BooleanVar()
tk.Checkbutton(stats_frame, text="CPU", variable=checked_cpu).pack(side=tk.LEFT)
tk.Checkbutton(stats_frame, text="RAM", variable=checked_ram).pack(side=tk.LEFT)
tk.Checkbutton(stats_frame, text="Disk", variable=checked_disk).pack(side=tk.LEFT)

# Start processing
def start_button_def():
    global stats_type, colors
    stats_type = []
    colors = []

    if checked_cpu.get():
        stats_type.append("CPU")
        colors.append("red")
    if checked_ram.get():
        stats_type.append("RAM")
        colors.append("green")
    if checked_disk.get():
        stats_type.append("DISK")
        colors.append("blue")
    
    if len(stats_type) >= 2:  # If list is not empty
        entry.delete(0, tk.END)
        entry.insert(tk.END, f"Starting...")
        os.startfile("code\\main.py")
        root.after(2000, root.destroy)
    
    elif len(stats_type) < 2:
        entry.delete(0, tk.END)
        entry.insert(tk.END, f"You must pick at least 2 elements.")

# Creating start button
tk.Button(root, text='Start', command=start_button_def, width=20).pack()

# Output place
entry = tk.Entry(root, width=30, font=("Arial", 10))
entry.pack(padx=20, pady=20)

# Start
root.mainloop()
