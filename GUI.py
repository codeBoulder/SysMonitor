import tkinter as tk
import os

stats_type = []
colors = []

root = tk.Tk()
root.title("System stats")
root.geometry("350x200")

label = tk.Label(root, text="Choose the stats you need:", font=("Arial", 12))
label.pack()

stats_frame = tk.Frame(root)
stats_frame.pack(pady=10)

checked_cpu = tk.BooleanVar()
checked_ram = tk.BooleanVar()
checked_disk = tk.BooleanVar()
tk.Checkbutton(stats_frame, text="CPU", variable=checked_cpu).pack(side=tk.LEFT)
tk.Checkbutton(stats_frame, text="RAM", variable=checked_ram).pack(side=tk.LEFT)
tk.Checkbutton(stats_frame, text="Disk", variable=checked_disk).pack(side=tk.LEFT)

def start_button_def():
    global stats_type, colors
    if checked_cpu.get():
        stats_type.append("CPU")
        colors.append("red")
    if checked_ram.get():
        stats_type.append("RAM")
        colors.append("green")
    if checked_disk.get():
        stats_type.append("DISK")
        colors.append("blue")
    
    if stats_type:  # Якщо список не порожній
        os.startfile("show_stats.py")
        root.after(2000, root.destroy)

tk.Button(root, text='Start', command=start_button_def, width=10).pack()

root.mainloop()
