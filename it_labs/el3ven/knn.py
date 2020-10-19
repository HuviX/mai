import numpy as np
import pandas as pd



class KNN():
    def __init__(self, k):
        self.k = k
        if k%2 == 0: #Условие на то что число соседей не должно быть четным
            print("Even K values can be misleading. Reinitialize object with odd K value.")
    
    def predict_point_class(self, test_point, labels):
        self.labels = labels 
        self.dist = self.data[test_point] #достаем из набора данных расстояние от данной станции метро до 9 станций, которые лежат в размеченном наборе(трейне)
        ind = np.array(self.dist).argsort()[:self.k] #сортируем объекты по возрастанию и получаем индексы К самых маленьких(близких)
        return  1 if self.labels[ind].mean() > 0.5 else 0 #смотрим, если единичек больше, то класс 1. Если меньше, то 0

    def get_distances(self):
        self.data = pd.read_csv('data/metroMatrix.csv') #грузим матрицу


        
        
