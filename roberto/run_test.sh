#!/usr/bin/env bash
set -e

node_files=(17nodos.txt)
threads=(1 2 4 8 16 20 32 40)
reps=10
out=results.csv

# Cabecera
echo "Archivo,Hilos,Repeticion,Tiempo,Coste" > $out

for f in "${node_files[@]}"; do
  for t in "${threads[@]}"; do
    for i in $(seq 1 $reps); do
      outp=$(./tsp_par "$f" "$t")
      tiempo=$(echo "$outp" | sed -n '1p')
      coste=$(echo "$outp" | sed -n '2p')
      echo "$f,$t,$i,$tiempo,$coste" >> $out
      echo "[$i/$reps] $f con $t hilos → $tiempo s, coste $coste"
    done
  done
done

echo "Datos enviados en $out"