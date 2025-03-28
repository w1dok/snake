import networkx as nx
import matplotlib.pyplot as plt

# Создание графа
G = nx.Graph()

# Добавление ребер
edges = [
    (0, 1, 4), (0, 7, 8), (1, 2, 8), (1, 7, 11), (2, 3, 7), (2, 8, 2),
    (2, 5, 4), (3, 4, 9), (3, 5, 14), (4, 5, 10), (5, 6, 2), (6, 7, 1),
    (6, 8, 6), (7, 8, 7)
]

for edge in edges:
    G.add_edge(edge[0], edge[1], weight=edge[2])

# Применение алгоритма Дейкстры
source_node = 0
target_node = 4
shortest_path = nx.dijkstra_path(G, source_node, target_node)
shortest_path_length = nx.dijkstra_path_length(G, source_node, target_node)

print(f"Кратчайший путь от {source_node} до {target_node}: {shortest_path}")
print(f"Длина кратчайшего пути: {shortest_path_length}")

# Рисование графа
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Выделение кратчайшего пути
path_edges = list(zip(shortest_path, shortest_path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)

# Показать граф
plt.show(block=True)