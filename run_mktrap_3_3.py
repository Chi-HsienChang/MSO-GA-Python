import random
import sys
from pdb import set_trace
import networkx as nx
import matplotlib.pyplot as plt
import os

# 定義問題相關的參數
ell = 6  # 基因數量
population_size = 10  # 基因組個數
num_generations = 10 # 代數

first_gen = True
NFE = 0
population_fitness_dict = {}

def result():
    global NFE
    global population_fitness_dict
    max_fitness = max(population_fitness_dict.values())
    max_key = next(key for key, value in population_fitness_dict.items() if value == max_fitness)

    print("最大值:", max_fitness)
    print("對應的鍵:", max_key)
    print("NFE:", NFE)

def trap_fitness1(ch):
    
    if ch[0] == 1 and ch[1] == 1 and ch[2] == 1:
        return 1
    elif ch[0] == 1 and ch[1] == 1 and ch[2] == 0:
        return 0
    elif ch[0] == 1 and ch[1] == 0 and ch[2] == 1:
        return 0.15
    elif ch[0] == 0 and ch[1] == 1 and ch[2] == 1:
        return 0.3
    elif ch[0] == 1 and ch[1] == 0 and ch[2] == 0:
        return 0.45
    elif ch[0] == 0 and ch[1] == 1 and ch[2] == 0:
        return 0.6
    elif ch[0] == 0 and ch[1] == 0 and ch[2] == 1:
        return 0.75
    elif ch[0] == 0 and ch[1] == 0 and ch[2] == 0:
        return 0.9

def trap_fitness2(ch):
    
    if ch[0] == 1 and ch[1] == 1 and ch[2] == 1:
        return 1
    elif ch[0] == 1 and ch[1] == 1 and ch[2] == 0:
        return 0
    elif ch[0] == 1 and ch[1] == 0 and ch[2] == 1:
        return 0.13
    elif ch[0] == 0 and ch[1] == 1 and ch[2] == 1:
        return 0.26
    elif ch[0] == 1 and ch[1] == 0 and ch[2] == 0:
        return 0.39
    elif ch[0] == 0 and ch[1] == 1 and ch[2] == 0:
        return 0.69
    elif ch[0] == 0 and ch[1] == 0 and ch[2] == 1:
        return 0.82
    elif ch[0] == 0 and ch[1] == 0 and ch[2] == 0:
        return 0.95

def trap_fitness(ch):
    countOne = 0
    for i in ch:
        if i == 1:
            countOne+=1

    if countOne == 3:
        return 1
    elif countOne == 2:
        return 0
    elif countOne == 1:
        return 0.4
    else:
        return 0.8

# 定義MKTrap函數
def mk_trap_fitness(ch):
    global NFE
    global population_fitness_dict
    if str(ch) in population_fitness_dict:
        return population_fitness_dict[str(ch)]            
    else:
        fitness = trap_fitness1(ch[0:3]) + trap_fitness2(ch[3:6])
        NFE += 1

        if fitness == 2:
            population_fitness_dict.setdefault(str(ch), fitness)
            result()
            print("第 {} gen 找到最佳解".format(generation))
            sys.exit() 
        return fitness

def GHC(ch):
    global population_fitness_dict
    for i in range(ell):
        if ch[i] == 0:
            ch[i] = 1
            population_fitness_dict.setdefault(str(ch), mk_trap_fitness(ch))
            ch[i] = 0
        elif ch[i] == 1:
            ch[i] = 0
            population_fitness_dict.setdefault(str(ch), mk_trap_fitness(ch))
            ch[i] = 1
       

# 初始化種群
population = [[random.randint(0, 1) for _ in range(ell)] for _ in range(population_size)]


# print(population)

# 追蹤呼叫適應度函數的次數
NFE = 0

# 主循環：演化
for generation in range(num_generations):
    if first_gen:
        for i in range(population_size):
            GHC(population[i])
            population_fitness_dict.setdefault(str(population[i]), mk_trap_fitness(population[i]))
            first_gen = False
    else:
        flag = True
        while flag:
            new_ch = [random.randint(0, 1) for _ in range(ell)]
            GHC(new_ch)
            ch_count = len(population_fitness_dict)
            population_fitness_dict.setdefault(str(new_ch), mk_trap_fitness(new_ch))
            if len(population_fitness_dict) == ch_count + 1:
                break
    
    
    print("第"+str(generation+1)+" gen"+"已出現"+str(len(population_fitness_dict))+"條不同的ch")
    
    population_fitness_list = list(population_fitness_dict.items())

    # 根據值對列表中的值進行排序
    sorted_population_fitness_list = sorted(population_fitness_list, key=lambda item: item[1], reverse=True)

    # 建立包含相同值鍵的索引的字典
    # value_to_keys = {}
    # for index, (key, value) in enumerate(sorted_population_fitness_list):
    #     if value not in value_to_keys:
    #         value_to_keys[value] = []
    #     value_to_keys[value].append(index)

    # print("相同值鍵的索引：")
    # for value, indices in value_to_keys.items():
    #     print(f"值 {value} 對應的索引：{indices}")

    # 使用循環創建方陣並初始化為零
    arrow_matrix = []
    for i in range(ell):
        row = [0] * ell  # 初始化一行為零
        arrow_matrix.append(row)
        
    # print("arrow_matrix", arrow_matrix)

    def IsArrow(i, j):
        global sorted_population_fitness_list
        # set_trace()
        current_best_i = eval(sorted_population_fitness_list[0][0])[i]
        current_best_j = eval(sorted_population_fitness_list[0][0])[j]

        if current_best_i == 0:
            flip_i = 1
        elif current_best_i == 1:
            flip_i = 0
        else:
            print("錯誤")
            sys.exit()

        flip_flag = True
        for k in range(1, len(population_fitness_dict)):
            if flip_i == eval(sorted_population_fitness_list[k][0])[i]:
                current_best_j_after_flip_i = eval(sorted_population_fitness_list[k][0])[j]
                flip_flag = False
                break
            
        if flip_flag:
            print("supply不足")
            return 0
        else:
            if current_best_j_after_flip_i == current_best_j:
                return 0
            else:
                return 1
    
    for i in range(ell):
        for j in range(ell):
            if j == i:
                continue
            arrow_matrix[i][j] = IsArrow(i, j)

    print("arrow_matrix", arrow_matrix)

    # plot arrow graph

    one_layer_arrow = []
    for j in range(ell):
        temp_index = []
        for i in range(ell):
            if j == i:
                continue
            if arrow_matrix[i][j] == 1:
                temp_index.append(i)

        one_layer_arrow.append(temp_index)

    print("one_layer_arrow", one_layer_arrow)

    def plot_tree(j, depth, one_layer_arrow):
        G = nx.DiGraph()
        for k in one_layer_arrow[j]:
            # des = str(j) + "'"*depth
            # sou = str(k) + "'"*(depth+1)
            des = str(j) 
            sou = str(k) 
            G.add_edge(sou, des)
        # 計算節點的位置
        pos = nx.spring_layout(G)
            # 繪製圖形
        node_colors = ['orange' if node == des else 'skyblue' for node in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color=node_colors, font_size=10, font_color='black', arrows=True)

        folder_path = f"./img/gen{generation}"
        os.makedirs(folder_path, exist_ok=True) 

        plt.savefig(f"{folder_path}/tree_structure_gen{generation}_des{j}.png")
           
            # 存儲圖片
        # plt.savefig("./img/tree_structure_gen{}_des{}.png".format(generation, depth))
        plt.clf()

    depth = 0
    for j in range(ell): 
        plot_tree(j, depth, one_layer_arrow)

           
    # build MSO



# 找出最佳解
result()
