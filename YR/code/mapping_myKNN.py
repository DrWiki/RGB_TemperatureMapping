import numpy as np
from sklearn.metrics import euclidean_distances
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
import copy

class KNNClassifier:
    def __init__(self, k=8):
        self.k = k
        self.x_train = None
        self.y_train = None

    def fit(self, x_train, y_train):
        self.x_train = x_train
        self.y_train = y_train
        return self

    def predict(self, x_predict):
        y_predict = [self._predict(x) for x in x_predict]
        return np.array(y_predict)

    def predict2(self, x_predict, current_temp):
        y_predict = [self._predict2(x, current_temp) for x in x_predict]
        return np.array(y_predict)

    def _predict(self, x):
        distances = [np.sqrt(np.sum((x_train - x) ** 2)) for x_train in self.x_train]
        nearest = np.argsort(distances)[:self.k]
        top_k_y = [self.y_train[index] for index in nearest]
        d = {}
        for cls in top_k_y:
            d[cls] = d.get(cls, 0) + 1
        d_list = list(d.items())
        d_list.sort(key=lambda x: x[1], reverse=True)
        return np.array(d_list[0][0])

    def _predict2(self, x, current_temp):
        distances = list()
        for x_train, y_train in zip(self.x_train, self.y_train):
            if np.abs(y_train - current_temp) > 2:
                distances.append(1000)
            else:
                distances.append(np.sqrt(np.sum((x_train - x) ** 2)) + np.abs(y_train - current_temp) * 3)

        nearest = np.argsort(distances)[:self.k]
        top_k_y = [self.y_train[index] for index in nearest]
        d = {}
        for cls in top_k_y:
            d[cls] = d.get(cls, 0) + 1
        d_list = list(d.items())
        d_list.sort(key=lambda x: x[1], reverse=True)
        return np.array(d_list[0][0])

    def __repr__(self):
        return "KNN(k={})".format(self.k)


if __name__ == '__main__':
    RGBT_data = pd.read_csv('.\KNN_Dataset\RGBT_with_all_T_step3.csv')
    # RGBT_data_val = RGBT_data.value
    # train_data, test_data = train_test_split(copy.deepcopy(RGBT_data), test_size=0.1, random_state=0)
    #
    # train_data_val = train_data[train_data.columns[:-1]].values
    # train_data_label = train_data['label'].values
    # test_data_val = test_data[test_data.columns[:-1]].values
    # test_data_label = test_data['label'].values
    #
    # clf = KNNClassifier()
    # clf.fit(train_data_val, train_data_label)
    #
    # test_predictions = clf.predict(test_data_val)
    # print('Accuracy:', accuracy_score(test_data_label, test_predictions))
    # print('MSE:', mean_squared_error(test_data_label, test_predictions))

    train_data_val = RGBT_data[RGBT_data.columns[:-1]].values
    train_data_label = RGBT_data['label'].values

    clf = KNNClassifier()
    clf.fit(train_data_val, train_data_label)

    # 读取时间序列
    folder_name = 'data'
    file_name = '604_951_38.npy'
    memo = np.load(f'./{folder_name}/{file_name}')
    xs = np.arange(1, len(memo) + 1)

    tempC = 24
    tempD = 0
    temperature = list()
    for i in memo:
        result = clf.predict2([i], tempC)[0]
        temperature.append(result)
        tempD = result - tempC
        print(tempC)
        tempC = result

    plt.plot(xs, temperature)
    plt.xlabel('Frame')
    plt.ylabel('Temprature')
    plt.title(f'{file_name}')
    plt.show()






