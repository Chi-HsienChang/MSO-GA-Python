import random
import sys

# 定義問題相關的參數
ell = 10  # 基因數量
gene_length = 1  # 單個基因長度
population_size = 80  # 基因組個數
num_generations = 100  # 代數

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

def trap_fitness(ch):
    countOne = 0
    for i in ch:
        if i == 1:
            countOne+=1

    if countOne == 5:
        return 1
    elif countOne == 4:
        return 0
    elif countOne == 3:
        return 0.2
    elif countOne == 2:
        return 0.4
    elif countOne == 1:
        return 0.6
    else:
        return 0.8

# 定義MKTrap函數
def mk_trap_fitness(ch):
    global NFE
    NFE += 1
    fitness = trap_fitness(ch[0:5]) +  trap_fitness(ch[5:10])

    if fitness == 2:
        print(ch)
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
max_fitness = max(population_fitness_dict.values())
max_key = next(key for key, value in population_fitness_dict.items() if value == max_fitness)

print("最大值:", max_fitness)
print("對應的鍵:", max_key)
print("NFE:", NFE)
