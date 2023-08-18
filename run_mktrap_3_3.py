import random
import sys
from pdb import set_trace

# 定義問題相關的參數
ell = 6  # 基因數量
gene_length = 1  # 單個基因長度
population_size = 10  # 基因組個數
num_generations = 10 # 代數

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
    NFE += 1
    fitness = trap_fitness1(ch[0:3]) + trap_fitness2(ch[3:6])

    if fitness == 2:
        population_fitness_dict.setdefault(str(ch), fitness)
        result()
        print("找到最佳解")
        sys.exit() 
    return fitness

# 初始化種群
population = [[random.randint(0, 1) for _ in range(ell * gene_length)] for _ in range(population_size)]

# print(population)

# 追蹤呼叫適應度函數的次數
NFE = 0

# 主循環：演化
for generation in range(num_generations):
    # 計算適應度
    fitness_scores = [mk_trap_fitness(individual) for individual in population]

    for i in range(population_size):
        population_fitness_dict.setdefault(str(population[i]), mk_trap_fitness(population[i]))
    
    print("第"+str(generation+1)+" gen"+"已出現"+str(len(population_fitness_dict))+"條不同的ch")
    
    population_fitness_list = list(population_fitness_dict.items())

    # 根據值對列表中的值進行排序
    sorted_population_fitness_list = sorted(population_fitness_list, key=lambda item: item[1], reverse=True)

    # 建立包含相同值鍵的索引的字典
    value_to_keys = {}
    for index, (key, value) in enumerate(sorted_population_fitness_list):
        if value not in value_to_keys:
            value_to_keys[value] = []
        value_to_keys[value].append(index)

    print("相同值鍵的索引：")
    for value, indices in value_to_keys.items():
        print(f"值 {value} 對應的索引：{indices}")

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


        for k in range(1, population_size):
            if flip_i == eval(sorted_population_fitness_list[k][0])[i]:
                current_best_j_after_flip_i = eval(sorted_population_fitness_list[k][0])[j]
                break

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

    # build MSO

            


    

    

    


    
    

    # 選擇
    selected_indices = random.choices(range(population_size), weights=fitness_scores, k=population_size)
    selected_population = [population[i] for i in selected_indices]
    
    # 交叉
    new_population = []
    for _ in range(population_size // 2):
        parent1 = random.choice(selected_population)
        parent2 = random.choice(selected_population)
        crossover_point = random.randint(1, ell * gene_length - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        new_population.extend([child1, child2])
    
    # 突變
    for individual in new_population:
        if random.random() < 0.05:  # 假設突變率為5%
            mutation_point = random.randint(0, ell * gene_length - 1)
            individual[mutation_point] = 1 - individual[mutation_point]
    
    population = new_population
    
# 找出最佳解
result()
