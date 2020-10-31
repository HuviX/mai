from point import Point
import pygame
import random
import time
from giftWrap import giftWrappingAlg
import argparse
from typing import List
from PIL import Image
from configparser import ConfigParser



config = ConfigParser()
config.read("cfg.ini")
W, H = int(config["DEFAULT"]["width"]), int(config["DEFAULT"]["height"])
MARGIN = int(config["DEFAULT"]["margin"])
POINT_RADIUS = int(config["DEFAULT"]["point_radius"]) #Радиус точки

#цвета для рисования
red = (255,0,0)
white = (230, 230, 230)
gray = (180, 180, 180)


def get_points(n: int, path: str, randomized: bool)->List[Point]:
    points = []
    if randomized:
        for _ in range(n):
            x = random.randint(MARGIN, W-MARGIN)
            y = random.randint(MARGIN, H-MARGIN)
            points.append(Point(x, y))
    else:
        with open(path, 'r') as f:
            while True:
                s = f.readline()
                if not s:
                    break
                s = s.split(',')
                x = int(s[0])
                y = int(s[1])
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
    parser.add_argument('--path', type=str, default="", help='path to points file')
    args = parser.parse_args()
    animate = args.animate
    n = args.n
    path = args.path
    #Нужно ли случайно создавать точки или взять из файла, для этого есть флаг randomized
    if path == "":
        randomized = True
    else:
        randomized = False

    pnts = get_points(n, args.path, randomized)
    pnts = sorted(pnts, key=lambda p: p.x)


    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.update()

    alg = giftWrappingAlg(points=pnts, color=white, convex_color=red, screen=screen, 
        line_color=gray, size=POINT_RADIUS, animate=animate)
    conv_shape = alg.convex_shape()
    to_file(conv_shape)
    print("Done")


    run = True
    #чтобы выйти можно было на крестик
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            pygame.display.update()
    pygame.quit()
