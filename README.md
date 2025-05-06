- [x] Ejecutar

```
~ mpiexec -n 4 python run.py
```

- [x] Editar WSL

```
~ vim ~/.bashrc
~ source ~/.bashrc
```

- [x] Compilar C

```
~ sudo apt install build-essential
```

```
~ gcc -Wall -o iregex.out iregex.c
~ gcc -Wall -o iregex.out iregex.c -fopenmp
```

- [x] For Khipu

```
~ module load python3
~ module swap openmpi4 mpich/3.4.3-ofi
~ module load py3-mpi4py
```
