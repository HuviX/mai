import argparse
import os
from shelling import Shelling
import shutil


if __name__ == '__main__':
    print('Started !')
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, default=10)
    parser.add_argument("--fps", type=int, default=3)
    #временная папка для рисунков
    parser.add_argument("--path", type=str, default="tmp")
    #Флаг, который показывает нужно ли оставить временные рисунки (0 - удаляет папку в --path)
    parser.add_argument("--keep", type=int, default=0)
    parser.add_argument("--name", type=str, default="movie")

    args = parser.parse_args()
    n = args.N
    fps = args.fps
    path = args.path
    name = args.name

    if not os.path.exists(path):
        os.makedirs(path)

    model = Shelling(n)
    model.run_simulation(fps, path, name)
    if args.keep == 0:
        shutil.rmtree(path)
    print(f'Take a look at {name}.gif')
