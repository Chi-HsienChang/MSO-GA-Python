import networkx as nx
import matplotlib.pyplot as plt

# 建立一個有向圖
G = nx.DiGraph()

# 添加節點和邊
G.add_edge("1'", "0")
G.add_edge("2'", "0")
G.add_edge("3'", "0")
G.add_edge("3''", "1'")

# 計算節點的位置
pos = nx.spring_layout(G)

# 繪製圖形
nx.draw(G, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, font_color='black', arrows=True)

# 存儲圖片
plt.savefig("tree_structure.png")

# 顯示圖形
plt.show()
