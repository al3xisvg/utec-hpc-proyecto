#include <mpi.h>
#include <vector>
#include <iostream>
#include <chrono>
#include <sys/stat.h>

#include "reader.h"
#include "tsp_mpi.h"

bool file_exists(const std::string& name) {
    struct stat buffer;
    return (stat(name.c_str(), &buffer) == 0);
}

int main(int argc, char *argv[]) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    std::vector<std::vector<int>> matrix;
    int N;

    if (rank == 0) {
        matrix = leerArchivo<int>(argv[1]);
        N = matrix.size();
    }

    // Broadcast del tamaño y matriz
    MPI_Bcast(&N, 1, MPI_INT, 0, MPI_COMM_WORLD);
    if (rank != 0) matrix.resize(N, std::vector<int>(N));
    for (int i = 0; i < N; ++i) {
        MPI_Bcast(matrix[i].data(), N, MPI_INT, 0, MPI_COMM_WORLD);
    }

    // División de ramas desde el nodo 0
    std::vector<int> children_indices;
    for (int j = 1 + rank; j < N; j += size) {
        if (matrix[0][j] != INF)
            children_indices.push_back(j);
    }

    double start_time = MPI_Wtime();
    double local_cost = INF;
    std::vector<int> local_path;

    for (int j : children_indices) {
        auto solution = solve_branch(matrix, 0, j);
        if (solution.first < local_cost) {
            local_cost = solution.first;
            local_path = solution.second;
        }
    }

    double end_time = MPI_Wtime();
    double local_time = end_time - start_time;

    // Cada proceso envía su costo
    double all_costs[size];
    MPI_Gather(&local_cost, 1, MPI_DOUBLE, all_costs, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    // Cada proceso envía el tamaño de su camino
    int path_len = local_path.size();
    int all_path_lens[size];
    MPI_Gather(&path_len, 1, MPI_INT, all_path_lens, 1, MPI_INT, 0, MPI_COMM_WORLD);

    // Reunir rutas
    int max_path_len = N + 1;
    std::vector<int> send_path = local_path;
    send_path.resize(max_path_len, -1);
    std::vector<int> all_paths(size * max_path_len, -1);

    MPI_Gather(send_path.data(), max_path_len, MPI_INT, all_paths.data(), max_path_len, MPI_INT, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        int best_idx = 0;
        double best_cost = all_costs[0];
        for (int i = 1; i < size; ++i) {
            if (all_costs[i] < best_cost) {
                best_cost = all_costs[i];
                best_idx = i;
            }
        }

        std::cout << "\n🏁 Mejor ruta encontrada por el proceso " << best_idx << ":\n";
        for (int i = 0; i < all_path_lens[best_idx]; ++i) {
            std::cout << all_paths[best_idx * max_path_len + i] + 1;
            if (i < all_path_lens[best_idx] - 1) std::cout << " -> ";
        }
        std::cout << "\n💰 Costo total: " << best_cost << "\n";

        // Ahora guarda CSV
        // std::string output_file = "output.csv";
        /*bool exists = file_exists(output_file);

        std::ofstream out(output_file, std::ios::app);
        if (!exists)
            out << "procesos,tiempo,costo\n";  // encabezado solo si no existe*/

        // std::pair<int, double> data = std::make_pair(size, local_time);
        std::string input_file = argv[1];
        std::string filename = input_file.substr(input_file.find_last_of("/\\") + 1);
        writeToCSV(argv[2], size, local_time, best_cost, filename);

        /*std::ofstream extra(output_file, std::ios::app);
        extra << size << "," << local_time << "," << best_cost << "\n";
        out.close();*/
    }

    MPI_Finalize();
    return 0;
}
