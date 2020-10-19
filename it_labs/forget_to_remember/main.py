import argparse
import os
from shelling import Shelling


if __name__ == '__main__':
    print('Started !')
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, default=10)
    parser.add_argument("--fps", type=int, default=3)

    args = parser.parse_args()
    n = args.N
    fps = args.fps

    if not os.path.exists('pics'):
        os.makedirs('pics')

    model = Shelling(n)
    model.run_simulation(fps)
    print('Take a look at movie.gif')
