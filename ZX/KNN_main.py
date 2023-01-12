import pandas as pd
import copy
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

# 读入数据
RGBT_data = pd.read_csv('.\data\EveryDegree\RGBT_with_all_T_step1_maxbias15.csv')

# 将数据分为训练集和测试集，用来测试模型分类正确率
train_data, test_data = train_test_split(copy.deepcopy(RGBT_data), test_size=0.1, random_state=0)   # 9：1分割
# 可以试一试8：2 或 7：3 或 6：4 的分割比例，需要展示，看泛化性能

# 定义训练函数
def train(k=8):
    # 创建分类器
    clf = KNeighborsClassifier(n_neighbors=k)

    # 训练数据
    clf.fit(train_data[train_data.columns[:-1]], train_data['T'])

    # 测试数据
    test_predictions = clf.predict(test_data[test_data.columns[:-1]])
    print('Accuracy:', accuracy_score(test_data['T'], test_predictions))
    print('MSE:', mean_squared_error(test_data['T'], test_predictions))

    return test_predictions

# 测试
test_predictions = train(k=8)

# 画混淆矩阵图
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(test_data['T'], test_predictions)

xticks = np.linspace(15, 39, 39-15+1, dtype=np.int8)
yticks = np.linspace(15, 39, 39-15+1, dtype=np.int8)
plt.figure(figsize = (25,17))
sns.heatmap(cm, annot=True, fmt='.20g', xticklabels=xticks, yticklabels=yticks)
plt.xlabel('Predicted')
plt.ylabel('Truth')
plt.title('Confusion Matrix (train:test = 9:1)')
plt.show()