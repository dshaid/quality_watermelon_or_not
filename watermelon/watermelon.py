# 判断西瓜好坏核心代码
# 朴素贝叶斯算法
# 西瓜书 P151
import numpy as np
import pandas as pd


def load_data(rate=0.9):
    data_path = r'H:\Project\quality_watermelon_or_not\watermelon\data\watermelon3_0.csv'
    df = pd.read_csv(data_path)
    del df['编号']
    del df['密度']
    del df['含糖率']
    data = df.values
    return data


def trainNB(data):
    labels = data[:, -1]
    PGood = sum([1 for l in labels if l == '是']) / len(labels)
    PBad = 1 - PGood
    NBClassify = {'是': {}, '否': {}}
    for label in NBClassify.keys():
        sub_data = data[data[:, -1] == label]
        sub_data = np.array(sub_data)
        for k in range(sub_data.shape[1]):
            NBClassify[label][k] = dict()
            tags = list(set(data[:, k]))
            d = sub_data[:, k]
            for tag in tags:
                NBClassify[label][k][tag] = (
                    sum([1 for i in d if i == tag]) + 1) / len(d)
    return PGood, PBad, NBClassify


def testNB(data, PG, PB, NBClassify):
    predict_vec = list()
    for sample in data:
        pg = np.math.log(PG, 2)
        pb = np.math.log(PB, 2)
        for label in NBClassify.keys():
            for k, tag in enumerate(sample):
                if label == '是':
                    pg += np.math.log(NBClassify[label][k][tag], 2)
                else:
                    pb += np.math.log(NBClassify[label][k][tag], 2)
        if pg >= pb:
            predict_vec.append('是')
        else:
            predict_vec.append('否')
    return np.array(predict_vec)


# 被调函数
def pre(list_data):
    data = load_data()
    PG, PB, NBClassify = trainNB(data)
    predict_vec = testNB(list_data, PG, PB, NBClassify)
    return predict_vec
