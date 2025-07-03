#pragma once
#include <vector>
#include <limits>
#include <queue>
#define INF std::numeric_limits<int>::max()

template <typename T>
struct Node {
    std::vector<std::pair<T, T>> path;
    std::vector<std::vector<T>> matrix_reduced;
    T cost;
    int vertex;
    int level;
};

template <typename T>
Node<T>* newNode(std::vector<std::vector<T>> matrix_parent, std::vector<std::pair<T, T>> const &path, int level, int i, int j, int N) {
    auto node = new Node<T>;
    node->path = path;
    if (level != 0)
        node->path.push_back(std::make_pair(i, j));
    node->matrix_reduced = matrix_parent;
    for (int k = 0; level != 0 && k < N; k++) {
        node->matrix_reduced[i][k] = INF;
        node->matrix_reduced[k][j] = INF;
    }
    node->matrix_reduced[j][0] = INF;
    node->level = level;
    node->vertex = j;
    return node;
}

template <typename T>
T reduce_and_cost(std::vector<std::vector<T>> &matrix, int N) {
    T cost = 0;
    for (int i = 0; i < N; ++i) {
        T row_min = INF;
        for (int j = 0; j < N; ++j)
            row_min = std::min(row_min, matrix[i][j]);
        if (row_min != INF && row_min > 0) {
            cost += row_min;
            for (int j = 0; j < N; ++j)
                if (matrix[i][j] != INF)
                    matrix[i][j] -= row_min;
        }
    }

    for (int j = 0; j < N; ++j) {
        T col_min = INF;
        for (int i = 0; i < N; ++i)
            col_min = std::min(col_min, matrix[i][j]);
        if (col_min != INF && col_min > 0) {
            cost += col_min;
            for (int i = 0; i < N; ++i)
                if (matrix[i][j] != INF)
                    matrix[i][j] -= col_min;
        }
    }

    return cost;
}

template <typename T>
Node<T>* TSP(std::vector<std::vector<T>> &matrix, Node<T>* start) {
    int N = matrix.size();
    std::priority_queue<Node<T>*, std::vector<Node<T>*>, 
        bool(*)(const Node<T>*, const Node<T>*)> pq(
        [](const Node<T>* a, const Node<T>* b) { return a->cost > b->cost; });

    pq.push(start);

    while (!pq.empty()) {
        auto min = pq.top();
        pq.pop();

        int i = min->vertex;

        if (min->level == N - 1) {
            min->path.push_back(std::make_pair(i, 0));
            return min;
        }

        for (int j = 0; j < N; ++j) {
            if (min->matrix_reduced[i][j] != INF) {
                Node<T>* child = newNode(min->matrix_reduced, min->path, min->level + 1, i, j, N);
                child->cost = min->cost + min->matrix_reduced[i][j] + reduce_and_cost(child->matrix_reduced, N);
                pq.push(child);
            }
        }

        delete min;
    }

    return nullptr;
}

std::pair<int, std::vector<int>> solve_branch(std::vector<std::vector<int>> matrix, int from, int to) {
    int N = matrix.size();
    auto root = newNode(matrix, {}, 1, from, to, N);
    root->cost = matrix[from][to] + reduce_and_cost(root->matrix_reduced, N);
    auto result = TSP(matrix, root);
    std::vector<int> route;
    for (auto p : result->path) {
        route.push_back(p.first);
    }
    route.push_back(0);  // cerrar ciclo
    return { result->cost, route };
}
