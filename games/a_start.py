import networkx as nx
import matplotlib.pyplot as plt

# Создаем граф
G = nx.Graph()

# Добавление ребер
edges = [
    (0, 1, 4), (0, 7, 8), (1, 2, 8), (1, 7, 11), (2, 3, 7), (2, 8, 2),
    (2, 5, 4), (3, 4, 9), (3, 5, 14), (4, 5, 10), (5, 6, 2), (6, 7, 1),
    (6, 8, 6), (7, 8, 7)
]

for edge in edges:
    G.add_edge(edge[0], edge[1], weight=edge[2])

# Определяем эвристическую функцию (например, евклидово расстояние)
def heuristic(u, v):
    # Для простоты задаем эвристику как 0 (можно заменить на реальную функцию)
    return abs(u - v)

# Применение алгоритма A*
source_node = 0  # Начальная вершина
target_node = 4  # Конечная вершина
shortest_path = nx.astar_path(G, source_node, target_node, heuristic=heuristic)
shortest_path_length = nx.astar_path_length(G, source_node, target_node, heuristic=heuristic)

print(f"Кратчайший путь от {source_node} до {target_node}: {shortest_path}")
print(f"Длина кратчайшего пути: {shortest_path_length}")
print(f"Ребра графа: {edges}")

# Рисование графа
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Выделение кратчайшего пути
path_edges = list(zip(shortest_path, shortest_path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)

# Показать граф
plt.show()