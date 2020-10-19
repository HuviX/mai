# Лабораторная работа 2 :mage_man:

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

[![GitHub release](https://img.shields.io/badge/version-v1.0-red)](https://img.shields.io/badge/version-v1.0-red)
[![Contributor](https://img.shields.io/badge/contributors-4-blue)](https://img.shields.io/badge/contributors-4-blue)


## Описание

В этой лабораторной работе мы работали с API Вконтакте, строили граф друзей и находили вершины этого графа удовлетворяющие разным правилам центральности.

Граф был построен на основании дружеских свзяей в нашей группе. Таким образом мы получили граф состоящий из 13 вершин. В нашем случае связного графа не получилось, были вершины которые не соединены ребрам.

После того как граф был построен были найдены вершины центральные по:
- Посредничеству
- Расстоянию
- Собственному векору

Необходимые библиотеки
- ``vk==2.0.2``
- ``pandas==1.1.2``
- ``networkx==2.5 ``
- ``matplotlib==3.3.2``
- ``jupyter==1.0.0``

Иллюстрация графов и значения центральностей представлены в `centrality_plots.ipynb`.
