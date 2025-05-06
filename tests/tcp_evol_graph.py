import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Leer el CSV generado durante las ejecuciones paralelas
df = pd.read_csv("performance_log.csv", header=None, names=["num_cities", "num_processes", "time"])

# Aseguramos que los tipos estén correctos
df["num_cities"] = df["num_cities"].astype(int)
df["num_processes"] = df["num_processes"].astype(int)

# Estilo bonito
sns.set(style="whitegrid")

# Creamos el gráfico
plt.figure(figsize=(10, 6))
sns.lineplot(
    data=df,
    x="num_processes",
    y="time",
    hue="num_cities",  # Agrupar por cantidad de ciudades
    marker="o",
    palette="Set2"
)

# Títulos y etiquetas
plt.title("⏱️ Tiempos de ejecución del TSP vs Número de procesos")
plt.xlabel("Número de procesos")
plt.ylabel("Tiempo de ejecución (segundos)")
plt.legend(title="Número de ciudades")
plt.tight_layout()

# Guardar y mostrar
# plt.savefig("grafico_tiempos_vs_procesos.png")
plt.show()
