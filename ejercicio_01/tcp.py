from mpi4py import MPI
from itertools import permutations
import numpy as np
import time, argparse

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Número de ciudades (puedes cambiar este valor)
# NUM_CITIES = 8
parser = argparse.ArgumentParser(description="Cantidad de Ciudades")
parser.add_argument("cities", type=int, help="Cities")
args = parser.parse_args()
NUM_CITIES = int(args.cities)
print("Cities: ", NUM_CITIES)

def generate_cities(num):
    return np.random.rand(num, 2) * 100

def euclidean_matrix(cities):
    n = len(cities)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = np.linalg.norm(cities[i] - cities[j])
    return matrix

# Cálculo distribuido
if rank == 0:
    # Matriz de disntacias entre 4 ciudades
    """
    distance_matrix = np.array([
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ])
    """
    # num_cities = len(distance_matrix)
    # cities = list(range(1, num_cities)) # excluyendo la ciudad 0 ( de origen)

    cities = generate_cities(NUM_CITIES)
    distance_matrix = euclidean_matrix(cities)
    nodes = list(range(1, NUM_CITIES))

    all_permutations = list(permutations(nodes)) # [(1,2,3), (1,3,2), ...]
    chunks = np.array_split(all_permutations, size)
    start_time = time.time()
else:
    distance_matrix = None
    chunks = None
    cities = None

# Repartir rutas entre procesos
"""
Se hace un broadcast de la matrix a todos los procesos porq aunqu cada proceso
trabaje con distintas rutas, TODOS necesitan CONOCER la MISMA MATRIX de
DISTANCIAS para poder calcular correctamente las distancias de sus rutas asignadas
"""
distance_matrix = comm.bcast(distance_matrix, root=0)
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
    best = min(all_best_routes, key=lambda x: x[0])

    print(f"\n Coordenadas de las ciudades:")
    for i, c in enumerate(cities):
        print(f"Ciudad {i}: ({c[0]:.2f}, {c[1]:.2f})")

    beststr = ' -> '.join(map(str, best[1]))

    print(f"Ruta óptima: [0 -> {beststr} -> 0]")
    print(f"Distancia mínima: {best[0]:.2f}")
    print(f"Tiempo de ejecución: {elapsed_time:.4f} segundos")

    # Guardado de archivo para graficar
    with open('performance_log.csv', "a") as f:
        f.write(f"{NUM_CITIES},{size},{elapsed_time},{best[0]},{beststr}\n")