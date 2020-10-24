import pygame
import time
from point import Point
from typing import Tuple, List, TypeVar


class giftWrappingAlg:
    def __init__(self, points: List[Point], color:Tuple[int], convex_color:Tuple[int], screen, line_color, size: int, animate: int = 1):
        self.points = points
        self.color = color
        self.screen = screen
        self.line_color = line_color
        self.left_most = points[0]
        self.size = size
        self.convex_color = convex_color
        if animate == 0:
            self.algorithm = self.find_convex_shape
        else:
            self.algorithm = self.find_convex_shape_draw
        self.start_draw()


    def start_draw(self):
        pygame.draw.circle(self.screen, self.convex_color, (self.left_most.x, self.left_most.y), self.size*2)
        pygame.display.update()
        for p in self.points[1:]:
            pygame.draw.circle(self.screen, self.color, (p.x,p.y), self.size, self.size)
        pygame.display.update()
        time.sleep(0.5)


    def convex_shape(self):
        return self.algorithm()


    def cross_product(self, x, y)->int:
        return y[1]*x[0] - y[0]*x[1]


    def find_convex_shape(self)->List[Point]:
        current_vertex = self.points[0]
        index = 1
        next_vertex = self.points[index]
        self.res_points = [self.left_most]

        while (self.left_most != next_vertex) or index == 1:
            index += 1
            next_vertex = self.points[index]
            for p in self.points:

                a = next_vertex - current_vertex
                b = p - current_vertex

                if self.cross_product(a, b) < 0:
                    next_vertex = p
            self.res_points.append(next_vertex)
            current_vertex = next_vertex

        self.draw_contour(draw_points=True)
        return self.res_points


    def find_convex_shape_draw(self)->List[Point]:
        current_vertex = self.points[0]
        index = 1
        next_vertex = self.points[index]
        self.res_points = [self.left_most]

        while (self.left_most != next_vertex) or index == 1:
            index = (index + 1) % (len(self.points))
            next_vertex = self.points[index]
            for p in self.points:
                pygame.draw.line(self.screen, self.line_color, (current_vertex.x, current_vertex.y),
                                            (p.x, p.y))
                pygame.display.update()

                a = next_vertex - current_vertex
                b = p - current_vertex

                if self.cross_product(a, b) < 0:
                    next_vertex = p

                time.sleep(0.1)
            self.res_points.append(next_vertex)
            current_vertex = next_vertex
            pygame.draw.circle(self.screen, self.convex_color, (current_vertex.x, current_vertex.y), self.size*2)
        self.draw_contour()
        return self.res_points


    def draw_contour(self, draw_points = False):
        for i, p in enumerate(self.res_points):
            if draw_points:
                pygame.draw.circle(self.screen, self.convex_color, (p.x, p.y), self.size*2)
            if i < len(self.res_points)-1:
                pygame.draw.line(self.screen, self.convex_color, (p.x, p.y), (self.res_points[i+1].x, self.res_points[i+1].y))
                time.sleep(0.1)
            pygame.display.update()
