# f = x*x x为区间[0,31]内整数

import math
import random

def init_population(pop_size, chromosome_length):
    # 初始化种群
    pop = []
    for i in range(pop_size):
        temp = []
        for j in range(chromosome_length):
            temp.append(random.randint(0, 1))
        pop.append(temp)
        print("----------种群:", pop[i])
    return pop


def pop_b2d(pop):
    # 种群个体染色体二进制串转十进制表示
    temp = []
    index = len(pop)
    # print(pop)
    for i in range(index):
        temp.append(b2d(pop[i]))
    print("----------种群二进制转十进制", temp)
    return temp


def b2d(binary):
    t = 0
    index = len(binary)
    for i in range(index):
        print("==========染色体怎么就是列表了?", binary[i])
        t += binary[i]*math.pow(2, index-i-1)
    # t = t * end / (2 ** chromosome_length - 1)
    return t


def calobjvalue(pop, chromosome_length):
    # 计算种群内个体适应度
    obj_value = []
    temp = pop_b2d(pop)
    print("----------种群二进制转十进制", temp)
    index = len(temp)
    for i in range(index):
        x = temp[i]
        obj_value.append(x*x)
    print("----------种群适应度", obj_value)
    return obj_value


def findbest(pop, fit_value):
    # 寻找种群内最优个体及对应染色体
    index = len(pop)
    best_individual = pop[0]
    best_fit = fit_value[0]
    for i in range(1, index):
        if fit_value[i] >= best_fit:
            best_fit = fit_value[i]
            best_individual = pop[i]
            print("+++++++", pop[i])
    print("********", best_individual)
    return best_individual, best_fit


def cumsum(fit_value):
    # 从后往前算概率,不包括1
    index = len(fit_value)
    for i in range(index-2, -1, -1):
        t, j = 0, 0
        while j <= i:
            t += fit_value[j]
            j += 1
        fit_value[i] = t
        fit_value[index-1] = 1


def select(pop, fit_value):
    # 选择
    index = len(fit_value)
    newfit_value = []
    total_fit_value = 0
    print("----------选择前种群适应度", fit_value)
    for i in range(index):
        total_fit_value += fit_value[i]
    for i in range(index):
        newfit_value.append(fit_value[i]/total_fit_value)
    cumsum(newfit_value)
    ms = []
    pop_len = len(pop)
    for i in range(pop_len):
        ms.append(random.random())
    ms.sort()
    newindex, fitindex, newpop = 0, 0, pop

    # 轮盘选择
    while newindex < pop_len:
        if ms[newindex] < newfit_value[fitindex]:
            newpop[newindex] = pop[fitindex]
            newindex = newindex+1
        else:
            fitindex = fitindex+1
    pop = newpop

def cross(pop, pc):
    # 交叉
    index = len(pop)
    c_len = len(pop[0])
    for i in range(index-1):
        c_point = random.randint(0, c_len)
        if random.random() < pc:
            t1, t2 = [], []
            t1.extend(pop[i][:c_point])
            t1.extend(pop[i+1][c_point:])
            t2.extend(pop[i+1][:c_point])
            t2.extend(pop[i][c_point:])
            pop[i] = t1
            pop[i+1] = t2


def mutate(pop, pm):
    # 突变
    index = len(pop)
    c_len = len(pop[0])
    for i in range(index):
        if random.random() < pm:
            m_point = random.randint(0, c_len-1)
            if pop[i][m_point] == 1:
                pop[i][m_point] = 0
            else:
                pop[i][m_point] = 1


def main():
    iter_time = 500
    pop_size = 4  # 种群大小
    chromosome_length = 5  # 染色体长度
    start = 0  # 基因中允许出现的最小值00000
    end = 31  # 基因中允许出现的最大值11111
    pop_cross = 0.6  # 发生变异概率
    pop_mutate = 0.01  # 发生交叉概率
    pop = init_population(pop_size, chromosome_length)  # 初始化种群
    results = []
    best_y = 0
    for i in range(iter_time):
        fit_value = calobjvalue(pop, chromosome_length)
        best_individual, best_fit = findbest(pop, fit_value)
        print("----------种群最优个体", best_individual)
        print("----------种群最优适应度", best_fit)
        results.append([best_individual, best_fit])
        select(pop, fit_value)
        cross(pop, pop_cross)
        mutate(pop, pop_mutate)
        if(best_y < best_fit):
            best_y = best_fit
        for i in range(500):
            if results[i][1] == best_y:
                best_x = results[i][0]
                break
    print("代代最优个体集合: ", results)
    print("最适应个体: ", best_x)
    print("最优函数值: ", best_y)

if __name__ == "__main__":
    main()