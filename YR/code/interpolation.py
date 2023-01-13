import numpy as np
from sklearn.metrics import euclidean_distances
import pandas as pd
import matplotlib.pyplot as plt


def my_KNN2(dictionary, intensity, current_temprature):
    min_dis = float('inf')
    for key in dictionary.keys():
        temp = list(key)
        dist = float(euclidean_distances([intensity], [temp]))  # 求距离
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
            continue
        dist = float(euclidean_distances([intensity], [temp])) + np.abs(
            dictionary[key] - current_temprature) * 3  # 距离加正则量
        if dist < min_dis:
            min_dis = dist
            mem_key = key
    # print(np.abs(dictionary[key] - current_temprature) * 0.5)
    return dictionary[mem_key]


def my_KNN4(dictionary, intensity, current_temprature, num_inter):  # based on mykNN2, for interpolation
    min_dis = float('inf')
    for key in dictionary.keys():
        temp = list(key)
        if np.abs(dictionary[key] - current_temprature) > (3 / num_inter):  # 防止突变
            continue
        dist = float(euclidean_distances([intensity], [temp])) + np.abs(
            dictionary[key] - current_temprature) * 3 * num_inter  # 距离加正则量
        if dist < min_dis:
            min_dis = dist
            mem_key = key
    # print(np.abs(dictionary[key] - current_temprature) * 0.5)
    return dictionary[mem_key]


def interpolation(csv_table, num_inter, min_temp=15, max_temp=38):
    inter_table = {}

    for i in range(len(csv_table)):
        if i > 0:
            item0, item1 = csv_table[i - 1], csv_table[i]
            inter_table[(item0[2], item0[1], item0[0])] = item0[3]
            dB, dG, dR = float(item1[2] - item0[2]), float(item1[1] - item0[1]), float(item1[0] - item0[0])
            dB, dG, dR = dB / num_inter, dG / num_inter, dR / num_inter
            for k in range(num_inter):
                inter_table[(item0[2] + (k + 1) * dB, item0[1] + (k + 1) * dG, item0[0] + (k + 1) * dR)] = item0[3] + (
                            k + 1) * (1 / num_inter)
        if i == len(csv_table) - 1:
            inter_table[(item1[2], item1[1], item1[0])] = item1[3]

    return inter_table


if __name__ == '__main__':
    df = pd.read_csv('RGBT_rc_at1point.csv')  # 读取csv文件
    table = {}
    num_inter = 1

    for item in df.values:
        table[(item[2], item[1], item[0])] = item[3]  # 做table

    inter_table = interpolation(df.values, num_inter)

    file_name = '604_951_28'
    memo = np.load(f'D:/Git/RGB_TemperatureMapping/YR/point data/{file_name}.npy')
    xs = np.arange(1, len(memo) + 1)

    temperature = list()

    Ctemp = 24
    print(f'initial temperature: {Ctemp}')
    for i in memo:
        temp = my_KNN4(inter_table, i, Ctemp, num_inter)
        temperature.append(temp)
        Ctemp = temp

    np.save(f'D:/Git/RGB_TemperatureMapping/YR/output/temperature_{file_name}_interpolation{num_inter}', temperature)
    plt.plot(xs, temperature)
    plt.xlabel('Frame')
    plt.ylabel('Temprature')
    plt.title(f'{file_name}_interpolation{num_inter}')
    # plt.ylim(15, 40)
    plt.show()
