#!/bin/bash

# Lista de cantidades de procesos a probar
procs=(1 2 3 4 6 8 10 12)

# Archivo de entrada
input="test/5nodos.txt"

# Salida CSV
output="output.csv"

# Escribir encabezado
echo "procesos,tiempo,tiempo_com,costo" > "$output"

# Ejecutar por cada cantidad de procesos
for n in "${procs[@]}"; do
    echo "▶ Ejecutando con $n procesos..."
    mpiexec -n "$n" ./tsp_mpi "$input"
done

echo "✅ Finalizado. Revisa el archivo: $output"
