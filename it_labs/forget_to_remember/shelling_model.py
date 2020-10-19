import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple
from PIL import Image

import imageio
import argparse
import os


def get_row_col(index: int, width: int) -> Tuple[int, int]:
    row    = (int)(index / width)
    column = index - (row * width)
    return row, column


def create_grid(n: int) -> Tuple[np.array, dict, list]:
    size = n * n
    fraction = 0.9
    indices = list(range(size))
    non_empty_cells = int(fraction * size)
    empty_cells = size - non_empty_cells
    np.random.shuffle(indices)
    empties = indices[:empty_cells]
    blue = indices[empty_cells:non_empty_cells// 2 + empty_cells]
    red = indices[empty_cells + non_empty_cells // 2:]
    mapping = {-1 : blue, 1 : red}
    grid = np.zeros((n, n))
    
    for index in blue:
        row, col = get_row_col(index, n)
        grid[row, col] = -1
    for index in red:
        row, col = get_row_col(index, n)
        grid[row, col] = 1
    return grid, mapping, empties


def plot_grid(grid: np.array, counter: int) -> None:
    colord = {-1: (0, 0, 255),
          1: (255, 0, 0),
          0: (255, 255, 255)}
    y, x = np.array([(i,j) for i in range(n) for j in range(n)]).T
    c = np.array([[colord[v] for v in row] for row in grid.T], dtype='B')
    c1 = (c/255.0).reshape((n*n, 3))
    f, ax1 = plt.subplots(figsize = (10, 10))
    y_lim = max(y)
    x_lim = max(x)
    
    ax1.set_ylim([y_lim + 1, -1])
    ax1.set_xlim([-1, x_lim + 1])
    ax1.set_aspect(1)
    plt.scatter(y, x, c = c1, s = 100)
    plt.title("Shelling's model", loc='left')
    plt.title(f"Iter.:{counter}", loc='right')
    plt.savefig('pics/pic{}.png'.format(counter))
    plt.close()
    

def get_nonhappy(matrix: np.array) -> list:
    row, col = matrix.shape
    ker_row, ker_col = 3, 3
    pad_height = int((ker_row-1)/2)
    pad_width = int((ker_col-1)/2)
    padded_mat = np.zeros((row+(2*pad_height),col+(2*pad_width)))
    padded_mat[pad_height:padded_mat.shape[0]-pad_height,pad_width:padded_mat.shape[1]-pad_width] = matrix
    non_happy = []
    
    for i in range(row):
        for j in range(col):
            if matrix[i, j] != 0:
                same_as_central_element = np.sum(matrix[i,j] == padded_mat[i:i+ker_row,j:j+ker_col]) - 1
                if same_as_central_element < 2:
                    non_happy.append(i*col + j)
    return non_happy


def make_change(grid: np.array, non_happy: list) -> np.array:
    rand_nonhappy = np.random.choice(non_happy)
    rand_empty = np.random.choice(empties)
    row, col = get_row_col(rand_nonhappy, n)
    new_row, new_col = get_row_col(rand_empty, n)
    label = grid[row, col]
    
    mapping[label].remove(rand_nonhappy)
    mapping[label].append(rand_empty)
    empties.remove(rand_empty)
    empties.append(rand_nonhappy)
    grid[row, col] = 0
    grid[new_row, new_col] = label
    return grid


def run_simulation(grid: np.array, fps: int) -> None:
    counter = 0
    non_happy = get_nonhappy(grid)
    plot_grid(grid, counter)
    
    while len(non_happy) != 0:
        counter += 1
        grid = make_change(grid, non_happy)
        plot_grid(grid, counter)
        non_happy = get_nonhappy(grid)   
    filenames = [f'pics/pic{num}.png' for num in range(counter + 1)]
    images = [imageio.imread(filename) for filename in filenames]
    imageio.mimsave('movie.gif', images, loop=1, fps=fps)
    dont_notice_me_pls = list(map(os.remove, filenames))

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
	
	grid, mapping, empties = create_grid(n)
	run_simulation(grid, fps)
	print('Take a look at movie.gif')
