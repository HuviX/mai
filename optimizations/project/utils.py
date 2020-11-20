from matplotlib import pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

f = lambda w, x: w[0] + w[1]*x + w[2]*x**2

def gen_dataset(size, w = None):
    x = np.linspace(-5,5,size)
    if w == None:
        w = np.random.randint(low=-5, high=5, size=(3,))
    y = f(w, x)
    #30 процентов в test, 70 в train
    x_train, y_train, x_test, y_test = train_test_split(x, y, test_size=0.3, shuffle=False)
    return x_train, y_train, x_test, y_test, w


def plot_(x_train, x_test, y_train, y_test, w_hat, hist):
    mse = mean_squared_error(f(w_hat, x_train), y_train)
    plt.scatter(x_train, y_train, label = 'train data')
    plt.plot(x_train, f(w_hat, x_train),'--', label='prediction on train data')
    plt.title("$MSE$ train:" + str(round(mse, 9)))
    plt.legend()
    plt.show();

    mse = mean_squared_error(f(w_hat, x_test), y_test)
    plt.scatter(x_test, y_test, label = 'test data')
    plt.plot(x_test, f(w_hat, x_test),'--', label='prediction on test data', c='r')
    plt.title("$MSE$ test:"+ str(round(mse, 9)))
    plt.legend()
    plt.show();
    
    plt.plot(hist[1:], label = 'mse')
    plt.title("History")
    plt.legend()
    plt.grid()
    plt.show();
