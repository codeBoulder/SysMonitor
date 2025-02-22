import matplotlib.pyplot as plt
import matplotlib.animation as animation
import ctypes

# Завантаження бібліотеки
get_stats = ctypes.CDLL(r"C:\Users\Admin\Documents\GitHub\SysMonitor\system_stats.dll")

# Вказуємо типи повернення
get_stats.get_cpu_usage.restype = ctypes.c_double
get_stats.get_memory_stats.restype = ctypes.c_double
get_stats.get_disk_usage.restype = ctypes.c_double

# === Буфери для даних ===
time_window = 60  # Останні 60 секунд
cpu_data = [0] * time_window
ram_data = [0] * time_window
disk_data = [0] * time_window
time_labels = list(range(-time_window, 0))

# === Налаштування фігури ===
fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

# Налаштування графіків
for ax, title, color in zip(axes, ["CPU Usage (%)", "RAM Usage (%)", "Disk Usage (%)"], ["red", "blue", "green"]):
    ax.set_xlim(-time_window, 0)  # Часова шкала
    ax.set_ylim(0, 100)  # Відсоткове використання
    ax.set_ylabel("Використання (%)")
    ax.set_title(title)
    ax.grid(True)

# Назначення графіків
cpu_line, = axes[0].plot(time_labels, cpu_data, color="red")
ram_line, = axes[1].plot(time_labels, ram_data, color="blue")
disk_line, = axes[2].plot(time_labels, disk_data, color="green")

axes[2].set_xlabel("Час (с)")  # Підпис для X

# === Функція оновлення даних ===
def update(frame):
    global cpu_data, ram_data, disk_data

    # Отримуємо свіжі дані
    cpu_usage = get_stats.get_cpu_usage() / 100000000
    ram_usage = get_stats.get_memory_stats()
    disk_usage = get_stats.get_disk_usage()

    # Додаємо дані в буфери
    cpu_data.append(cpu_usage)
    ram_data.append(ram_usage)
    disk_data.append(disk_usage)

    # Видаляємо найстаріші значення
    cpu_data.pop(0)
    ram_data.pop(0)
    disk_data.pop(0)

    # Оновлення графіків
    cpu_line.set_ydata(cpu_data)
    ram_line.set_ydata(ram_data)
    disk_line.set_ydata(disk_data)

    return cpu_line, ram_line, disk_line

# === Запуск анімації ===
ani = animation.FuncAnimation(fig, update, interval=1000, blit=False)

plt.tight_layout()
plt.show()
