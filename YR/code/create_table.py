import numpy as np
from sklearn.metrics import euclidean_distances
import pandas as pd
import matplotlib.pyplot as plt


def my_KNN2(dictionary, intensity, current_temprature):
    min_dis = float('inf')
    for key in dictionary.keys():
        temp = list(key)
        dist = float(euclidean_distances([intensity], [temp])) # 求距离
        if dist < min_dis:
            min_dis = dist
            mem_key = key
    print(np.abs(dictionary[key] - current_temprature) * 0.5)
    return dictionary[mem_key]  # temperature

def my_KNN3(dictionary, intensity, current_temprature):
    min_dis = float('inf')
    for key in dictionary.keys():
        temp = list(key)
        if np.abs(dictionary[key] - current_temprature) > 2:  # 防止突变
            pass
        dist = float(euclidean_distances([intensity], [temp])) + np.abs(dictionary[key] - current_temprature) * 3  # 距离加正则量
        if dist < min_dis:
            min_dis = dist
            mem_key = key
    # print(np.abs(dictionary[key] - current_temprature) * 0.5)
    return dictionary[mem_key]



if __name__ == '__main__':
    df = pd.read_csv('RGBT_rc_at1point.csv')  # 读取csv文件
    table = {}

    for item in df.values:
        table[(item[2], item[1], item[0])] = item[3]  # 做table

    # print(table)
    # print(my_KNN(table, [97, 107, 106]))

    folder_name = 'data'
    file_name = '604_951_38.npy'
    memo = np.load(f'./{folder_name}/{file_name}')
    xs = np.arange(1, len(memo) + 1)

    temperature = list()

    Ctemp = 22
    for i in memo:
        temperature.append(my_KNN3(table, i, Ctemp))
        Ctemp = temperature[-1]

    np.save(f'./temperature_time/temperature_{file_name}', temperature)
    plt.plot(xs, temperature)
    plt.xlabel('Frame')
    plt.ylabel('Temprature')
    plt.title(f'{file_name}')
    plt.ylim(15, 40)
    plt.show()
