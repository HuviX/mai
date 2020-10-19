import argparse
import os
import numpy as np
from typing import Tuple
from utils import plot_grid
import imageio



def get_row_col(index: int, width: int) -> Tuple[int, int]:
    row = (int)(index / width)
    column = index - (row * width)
    return row, column


class Shelling():
    def __init__(self, n):
        self.n = n
        self.create_grid()
    
    
    def create_grid(self):
        size = self.n * self.n
        fraction = 0.9
        indices = list(range(size))
        non_empty_cells = int(fraction * size)
        empty_cells = size - non_empty_cells
        np.random.shuffle(indices)
        self.empties = indices[:empty_cells]
        blue = indices[empty_cells:non_empty_cells// 2 + empty_cells]
        red = indices[empty_cells + non_empty_cells // 2:]
        self.mapping = {-1 : blue, 1 : red}
        self.grid = np.zeros((self.n, self.n))
        for index in blue:
            row, col = get_row_col(index, self.n)
            self.grid[row, col] = -1
        for index in red:
            row, col = get_row_col(index, self.n)
            self.grid[row, col] = 1

    #Скользящее окно размера 3х3
    #Перепишу на numpy (без циклов), но позже, чтобы не вопросов о плагиате.
    def get_nonhappy(self):
        row, col = self.grid.shape
        ker_row, ker_col = 3, 3
        pad_height = int((ker_row-1)/2)
        pad_width = int((ker_col-1)/2)
        padded_mat = np.zeros((row+(2*pad_height), col+(2*pad_width)))
        padded_mat[pad_height: padded_mat.shape[0]-pad_height, pad_width: padded_mat.shape[1]-pad_width] = self.grid
        non_happy = []
        for i in range(row):
            for j in range(col):
                if self.grid[i, j] != 0:
                    same_as_central_element = np.sum(self.grid[i, j] == padded_mat[i:i+ker_row, j:j+ker_col]) - 1
                    if same_as_central_element < 2:
                        non_happy.append(i*col + j)
        return non_happy


    def make_change(self, non_happy) -> None:
        rand_nonhappy = np.random.choice(non_happy)
        rand_empty = np.random.choice(self.empties)
        row, col = get_row_col(rand_nonhappy, self.n)
        new_row, new_col = get_row_col(rand_empty, self.n)
        label = self.grid[row, col]
        
        self.mapping[label].remove(rand_nonhappy)
        self.mapping[label].append(rand_empty)
        self.empties.remove(rand_empty)
        self.empties.append(rand_nonhappy)
        self.grid[row, col] = 0
        self.grid[new_row, new_col] = label


    def run_simulation(self, fps: int) -> None:
        counter = 0
        plot_grid(self.grid, counter, self.n)
        non_happy = self.get_nonhappy()

        while len(non_happy) != 0:
            counter += 1
            self.make_change(non_happy)
            non_happy = self.get_nonhappy()
            plot_grid(self.grid, counter, self.n)

        filenames = [f'pics/pic{num}.png' for num in range(counter + 1)]
        images = [imageio.imread(filename) for filename in filenames]
        imageio.mimsave('movie.gif', images, loop=1, fps=fps)
        _ = list(map(os.remove, filenames))
