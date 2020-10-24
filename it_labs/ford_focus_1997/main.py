from point import Point
import pygame
import random
import time
from giftWrap import giftWrappingAlg
import argparse
from typing import List


W, H = 1600, 900 #Ширина и высота канваса
POINT_RADIUS = 5 #Радиус точки
MARGIN = 50 # отступ чтобы точки не находились на границе канваса

#цвета для рисования
red = (255,0,0)
white = (230, 230, 230)
gray = (180, 180, 180)


def get_points(n: int)->List[Point]:
    points = []
    for _ in range(n):
        x = random.randint(MARGIN, W-MARGIN)
        y = random.randint(MARGIN, H-MARGIN)
        points.append(Point(x, y))
    return points


def to_file(shape: list):
    with open("convex_shape.txt", 'w') as f:
        for p in shape:
            f.write(f"{p.x},{p.y}\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--animate", type=int, default=1, help='show animation')
    parser.add_argument('--n', type=int, default=50, help='number of points')
    args = parser.parse_args()
    animate = args.animate
    n = args.n
    

    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.update()


    pnts = get_points(n)
    pnts = sorted(pnts, key=lambda p: p.x)
    alg = giftWrappingAlg(points=pnts, color=white, convex_color=red, screen=screen, 
        line_color=gray, size=POINT_RADIUS, animate=animate)

    conv_shape = alg.convex_shape()
    to_file(conv_shape)
    print("Done")


    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            pygame.display.update()
    pygame.quit()
