import numpy as np


class Convex_hull():
    def __init__(self, algorithm):
        """
        Gift Wrapping Algo = 'gift'
        """
        if algorithm == 'gift':
            self.algorithm = self.__giftWrappingAlgorithm
    
    def cross_product(self, x, y):
        return y[1]*x[0] - y[0]*x[1]

    def find(self, points):
        return self.algorithm(points)
    

    def __giftWrappingAlgorithm(self, points):
        points = points[np.argsort(points[:,0])]
        left_most = points[0]
        current_vertex = points[0]
        index = 1
        next_vertex = points[index]
        self.res_points = [left_most.tolist()]
        while (left_most != next_vertex).all() or index == 1:
            index += 1
            next_vertex = points[index]
            for p in points:
                a = next_vertex - current_vertex
                b = p - current_vertex
                if self.cross_product(a, b) > 0:
                    next_vertex = p
            self.res_points.append(next_vertex.tolist())
            current_vertex = next_vertex
        return self.res_points
