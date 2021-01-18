# ID3 решающее дерево :deciduous_tree:

В ноутбуке демонстрация работы алгоритма с визуализацией дерева.
В данные был добавлен признак gender (пол). 

## Пакеты

- `graphviz` 
    * Если пакета нет, то `sudo apt-get install graphviz`

- `pydot`

- `pandas`

- `pickle5`

## Использование

Для построения дерева: 
```python
from tree import tree
tree_name = tree()
tree_name.fit(data, target_name)`
```

Как делать предсказание на новых данных:
```python
data = {'os': 'linux', 
        'mobile_os': 'iphone',
        'gender': 'male', 
        'drink': 'чай', 
        'wine': 'никакое'}
pred = tree_name.predict(data)
```

Сохранение из загрузка дерева из файла:
```python

tree_name.save("path/to/tree.pkl")
tree_name.load("path/to/tree.pkl")
```

Сохранение отображения структуры дерева в `.png`:
```python
tree.to_png(filename)
```
## Примеры

Ниже представлены различные деревья, построенные по набору данных `data.csv`

Для предсказания OS:

![tree](my_tree_os.png)

Для предсказания мобильной OS:

![tree](my_tree_mobile_os.png)

Для предсказания кофе/чай:

![tree](my_tree_drink.png)
