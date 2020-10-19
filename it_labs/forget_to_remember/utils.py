import matplotlib.pyplot as plt
import numpy as np

# n - размер поля.
def plot_grid(grid: np.array, path: str, counter: int, n: int) -> None:
    colord = {-1: (0, 0, 255),
               1: (255, 0, 0),
               0: (255, 255, 255)}

    y, x = np.array([(i,j) for i in range(n) for j in range(n)]).T
    c = np.array([[colord[v] for v in row] for row in grid.T], dtype='B')
    c1 = (c/255.0).reshape((n*n, 3))
    _, ax1 = plt.subplots(figsize = (10, 10))
    y_lim = max(y)
    x_lim = max(x)
    
    ax1.set_ylim([y_lim + 1, -1])
    ax1.set_xlim([-1, x_lim + 1])
    ax1.set_aspect(1)
    plt.scatter(y, x, c = c1, s = 100)
    plt.title("Shelling's model", loc='left')
    plt.title(f"Iter.:{counter}", loc='right')
    plt.savefig(f"{path}/pic{counter}.png")
    plt.close()
