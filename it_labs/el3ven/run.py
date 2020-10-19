import numpy as np
from knn import KNN
import pandas as pd

POINT = "Электрозаводская" #Объект который надо классифицировать
NEIGHBOURS = 5 # Количество соседей, на основании которых будем классифицировать

#Грузим исходную дату
data = pd.read_csv('data/data.csv', delimiter = ',', header = None)
data.columns = ['station','drink']

#Делаем маппинг, чтобы можно было определить класс новой точки простым средним.
mapping = {'Кофе':0,  'Чай':1}
reverse_mapping = dict({v, k} for k, v in mapping.items())  

labels = data['drink'].map(mapping).values

#Делаем объект КНН с параметром 3
knn_obj = KNN(NEIGHBOURS)
knn_obj.get_distances() #получем матрицу расстояний (ту которую с помощью селена получили)
prediction = knn_obj.predict_point_class(POINT, labels) #предсказываем класс точки.

print('{0} --> {1}'.format(POINT, reverse_mapping[prediction]))#делаем обратный маппинг, чтобы понять чё ето - чай или кофе.
