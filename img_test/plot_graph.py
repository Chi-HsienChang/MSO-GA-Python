import networkx as nx
import matplotlib.pyplot as plt

def plot_tree(parent, children, edges, filename):
    G = nx.DiGraph()
    G.add_node(parent)
    for child in children:
        G.add_edge(child, parent)  # 將子節點指向父節點
    for edge in edges:
        G.add_edge(edge[0], edge[1])  # 建立新的邊

    pos = nx.spring_layout(G)  # 計算節點的位置
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color='skyblue')  # 繪製圖形
    plt.savefig(filename)  # 將圖片存為文件
    plt.close()  # 關閉圖形

# 定義節點和其父節點
parent_node = 0
child_nodes = [1, 2, 3, 4, 5]
new_edges = [(1, 3), (2, 3)]

# 繪製樹狀結構圖並存為圖片檔案
plot_tree(parent_node, child_nodes, new_edges, 'tree_with_new_edges.png')
