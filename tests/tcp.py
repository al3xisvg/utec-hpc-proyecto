from mpi4py import MPI
from itertools import permutations
import numpy as np
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Matriz de disntacias entre 4 ciudades
distance_matrix = np.array([
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
])

num_cities = len(distance_matrix)
cities = list(range(1, num_cities)) # excluyendo la ciudad 0 ( de origen)

# Cálculo distribuido
if rank == 0:
    all_permutations = list(permutations(cities)) # [(1,2,3), (1,3,2), ...]
    chunks = np.array_split(all_permutations, size)
    start_time = time.time()
else:
    chunks = None

# Repartir rutas entre procesos
local_routes = comm.scatter(chunks, root=0) # Cada prceso recibe su parte

# Funcoin pa obtener la distancia
def route_distance(route):
    total = 0
    current = 0 # partir desde la ciudad 0
    for city in route:
        total += distance_matrix[current][city]
        current = city
    total += distance_matrix[current][0] # volver a la ciudad origen
    return total

# Buscar mejor ruta local
local_best_route = None
local_best_dist = float('inf')
for route in local_routes:
    dist = route_distance(route)
    if dist < local_best_dist:
        local_best_dist = dist
        local_best_route = route

# Reunir resultados
all_best_routes = comm.gather((local_best_dist, local_best_route), root=0)

# El proceso 0 selecciona la mejor de todas
if rank == 0:
    end_time = time.time()
    elapsed_time = end_time - start_time
    global_best = min(all_best_routes, key=lambda x: x[0])

    print(f"Ruta óptima: [0 → {' → '.join(map(str, global_best[1]))} → 0]")
    print(f"Distancia mínima: {global_best[0]}")
    print(f"Tiempo total: {elapsed_time:.4f} segundos")

    # Guardado de archivo para graficar
    with open('performance_log.csv', "a") as f:
        f.write(f"{size},{elapsed_time}\n")