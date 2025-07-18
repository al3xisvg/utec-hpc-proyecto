#pragma once
#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>

const int INF = std::numeric_limits<int>::max();

template <typename T>
std::vector<std::vector<T>> leerArchivo(const std::string& nombreArchivo) {
    std::vector<std::vector<T>> matriz;
    std::ifstream archivo(nombreArchivo);

    if (!archivo) {
        std::cout << "No se pudo abrir el archivo: " << nombreArchivo << std::endl;
        return matriz;
    }

    std::string linea;
    while (getline(archivo, linea)) {
        std::vector<T> fila;
        std::istringstream iss(linea);
        T valor;

        while (iss >> valor) {
            if(valor == 0)
                fila.push_back(INF);
            else
                fila.push_back(valor);
        }

        matriz.push_back(fila);
    }

    archivo.close();
    return matriz;
}

/*template <typename T>
void writeToCSV(const std::string& filename, std::pair<T, double>& data) {
    std::ofstream file(filename, std::ios::app);
    if (!file.is_open()) {
        std::cerr << "Failed to open file: " << filename << std::endl;
        return;
    }

    // Write data
    file << data.first << "," << data.second << std::endl;
    

    file.close();
    std::cout << "Data written to " << filename << std::endl;
}*/

void writeToCSV(const std::string& filename_out, int procesos, double tiempo, double tiempo_com, int costo, const std::string& filename_in) {
    std::ofstream file(filename_out, std::ios::app);
    if (!file.is_open()) {
        std::cerr << "❌ Error al abrir el archivo: " << filename_out << std::endl;
        return;
    }

    file << filename_in << "," << procesos << "," << tiempo << "," << tiempo_com << "," << costo << "\n";
    file.close();
}

template <typename T>
void writeMinPath(std::vector<std::pair<T, T>> const &list, T cost) {
    std::ofstream file("minPath.txt");
    if (!file.is_open()) {
        std::cerr << "Failed to open file " << std::endl;
        return;
    }

    // Write data
    for (int i = 0; i < list.size(); i++)
        file << list[i].first + 1 << " -> " << list[i].second + 1 << std::endl;
    
    file << "cost: " << cost << std::endl;

    file.close();
    std::cout << "Data written " << std::endl;
}