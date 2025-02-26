import matplotlib.pyplot as plt
import matplotlib.animation as animation
import ctypes
import time
from GUI import stats_type, colors

# Library download
get_stats = ctypes.CDLL("code/system_stats.dll")

# Specifying the result type
get_stats.get_cpu_usage.restype = ctypes.c_double
get_stats.get_memory_usage.restype = ctypes.c_double
get_stats.get_disk_usage.restype = ctypes.c_double

# Saving data
time_window = 60
cpu_data = [0] * time_window
ram_data = [0] * time_window
disk_data = [0] * time_window
time_labels = list(range(-time_window, 0))

# Figure settings
fig, axes = plt.subplots(len(stats_type), 1, figsize=(10, 8), sharex=True)

# Schedule settings
for ax, title, color in zip(axes, stats_type, colors):
    ax.set_xlim(-time_window, 0)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Usage (%)")
    ax.set_title(title)
    ax.grid(True)

# Assignment of schedules
lines = []
for ax, title, color in zip(axes, stats_type, colors):
    line, = ax.plot(time_labels, [0] * time_window, color=color)
    lines.append(line)


# Update data
def update(frame):
    global cpu_data, ram_data, disk_data

    # Get data
    cpu_usage = get_stats.get_cpu_usage()
    ram_usage = get_stats.get_memory_usage()
    disk_usage = get_stats.get_disk_usage()

    # Add data into storage
    cpu_data.append(cpu_usage)
    ram_data.append(ram_usage)
    disk_data.append(disk_usage)

    # Delete oldest data
    cpu_data.pop(0)
    ram_data.pop(0)
    disk_data.pop(0)

    # Schedule update
    for line, data in zip(lines, [cpu_data, ram_data, disk_data][:len(stats_type)]):
        line.set_ydata(data)

    return lines

# Animation start
ani = animation.FuncAnimation(fig, update, interval=1000, blit=False, cache_frame_data=False)

plt.tight_layout()
plt.show()
