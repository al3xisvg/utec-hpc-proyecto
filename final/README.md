```
~ sudo apt install -y build-essential openmpi-bin libopenmpi-dev
```

```
~ mpic++ main.cpp -o tsp_mpi
```

```
~ mpiexec -n 4 ./tsp_mpi test/5nodos.txt
```
