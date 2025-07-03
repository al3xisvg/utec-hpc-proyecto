#!/bin/bash

# Lista de procesos a probar
procs=(1 2 4 6 8 10 12)

# Carpeta de archivos de entrada
input_dir="test"

# Archivo de salida
output_file="output.csv"

# Encabezado CSV
echo "archivo,procesos,tiempo,costo" > "$output_file"

# Iterar sobre cada archivo .txt dentro de /test
for input_file in "$input_dir"/*.txt; do
    filename=$(basename "$input_file")  # ejemplo: 5nodos.txt
    echo "📂 Procesando archivo: $filename"

    for n in "${procs[@]}"; do
        echo "▶ Ejecutando con $n procesos en $filename..."
        result=$(mpiexec -n "$n" ./tsp_mpi "$input_file")

        # Leer valores generados en CSV interno
        # Asegúrate de que el programa aún escribe en output.csv temporal
        # Luego leer la última línea para extraer tiempo y costo
        last_line=$(tail -n 1 output.csv)

        # Agregar nombre del archivo como primer campo y reescribir en master output
        # echo "$filename,$last_line" >> "$output_file"
    done
done

echo "✅ Pruebas finalizadas. Resultados completos en: $output_file"
