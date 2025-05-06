import matplotlib.pyplot as plt
import csv

processes = []
times = []

with open("performance_log.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        processes.append(int(row[0]))
        times.append(float(row[1]))

t1 = times[0]
speedups = [t1/t for t in times]
efficiences = [s/p for s,p in zip(speedups, processes)]

plt.figure(figsize=(12, 4))

# tiemspo
plt.subplot(1, 3, 1)
plt.plot(processes, times, marker="o")
plt.title("Tiempo de ejecución")
plt.xlabel("Procesos")
plt.ylabel("Tiempo (seg)")

# Speedup
plt.subplot(1, 3, 2)
plt.plot(processes, speedups, marker="o")
plt.plot(processes, processes, linestyle="--", label="Speedup ideal")
plt.title("Speedup")
plt.xlabel("Procesos")
plt.ylabel("Speedup")
plt.legend()

# Eficiencia
plt.subplot(1, 3, 3)
plt.plot(processes, efficiences, marker="o")
plt.title("Eficiencia")
plt.xlabel("Procesos")
plt.ylabel("Eficiencia")

plt.tight_layout()
plt.show()
