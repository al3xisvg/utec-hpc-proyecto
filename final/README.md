```
~ sudo apt install -y build-essential openmpi-bin libopenmpi-dev
```

```
~ mpic++ main.cpp -o tsp_mpi
```

```
~ mpiexec -n 4 ./tsp_mpi test/5nodos.txt salida.csv
```

```
~ ./run_multi_files.sh
```

### En Khipu:

```
~ module avail
~ module purge
~ module load gnu12
~ module load openmpi4/4.1.6
```

```
~ mpic++ -std=c++17 -O2 -o tsp_mpi main.cpp
```