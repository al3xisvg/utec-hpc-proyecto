import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Leer el archivo CSV
df = pd.read_csv("performance_log.csv", header=None, names=["num_cities", "num_processes", "time"])

# Convertir tipos por seguridad
df["num_cities"] = df["num_cities"].astype(int)
df["num_processes"] = df["num_processes"].astype(int)

# Estilo de gráficos
sns.set(style="whitegrid")

# Crear el gráfico
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x="num_cities", y="time", hue="num_processes", marker="o", palette="viridis")

plt.title("⏱️ Performance del TSP Paralelo")
plt.xlabel("Número de ciudades")
plt.ylabel("Tiempo de ejecución (segundos)")
plt.legend(title="Número de procesos")
plt.tight_layout()
plt.savefig("grafico_performance_tsp.png")
plt.show()
