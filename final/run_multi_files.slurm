#!/bin/bash
#SBATCH --job-name=tsp_experiments
#SBATCH --output=logs/tsp_%j.out
#SBATCH --error=logs/tsp_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --time=00:10:00

module load gnu12
module load openmpi4/4.1.6

# Crear carpeta de logs si no existe
mkdir -p logs

# Configura los parámetros
ARCHIVOS=("test/5nodos.txt" "test/11nodos.txt" "test/12nodos.txt" "test/15nodos.txt")
PROCESOS=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16)
OUTPUT="output.csv"

# Limpiar el archivo de salida
echo "archivo,procesos,tiempo,costo" > $OUTPUT

# Ejecutar cada combinación
for archivo in "${ARCHIVOS[@]}"; do
  echo "📂 Procesando archivo: $archivo"
  for p in "${PROCESOS[@]}"; do
    echo "▶ Ejecutando con $p procesos en $archivo..."
    mpiexec -n $p ./tsp_mpi "$archivo" "$OUTPUT"
  done
done

