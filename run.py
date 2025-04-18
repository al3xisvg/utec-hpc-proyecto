from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD

rank = comm.Get_rank()

size = comm.Get_size()

# Ejemplo 1: Base
# print(f"Hello there!. ths is processor {rank} de {size}")

# Ejemplo 2: Envío y Respuesta
if rank == 0:
    data = "Hola procso 1"
    comm.send(data, dest=1)
    print(f"Proceso {rank} ha enviado: {data}")
elif rank == 1:
    data = comm.recv(source=0)
    print(f"Proceso {rank} ha recibido: {data}")

# Ejemplo 3: Suma distribuida
if rank == 0:
    data = np.arange(8, dtype='i')
    chunks = np.array_split(data, size)
else:
    chunks = None

chunk = comm.scatter(chunks, root=0) # Cada prceso recibe su parte
local_sum = np.sum(chunk) # Cada proceso calcula suma local
total_sum = comm.reduce(local_sum, op=MPI.SUM, root=0) # Recolectar y sumar todos los resultados

print(f"Soy el proceso {rank} y mi data es: scattered={chunk}, processed={local_sum}")

if rank == 0:
    print(f"Suma total: {total_sum}")