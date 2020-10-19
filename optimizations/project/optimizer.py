import numpy as np
from sklearn.metrics import mean_squared_error


class Nadam():
    def __init__(self, eta: int, beta1: int, beta2: int, early_stopping: float=1e-8):
        self.eta = eta
        self.beta1 = beta1
        self.beta2 = beta2
        self.func = lambda w, x: w[0] + w[1]*x + w[2]*x**2
        self.metric = mean_squared_error
        self.early_stopping = early_stopping


    def init_all(self):
        self.w = np.zeros(shape=(3,))
        self.mom1 = np.zeros(shape=(3,))
        self.mom2 = np.zeros(shape=(3,))
        self.loss = []
        return self
    

    def get_grads(self, y, y_pred, x):
        grad_a = np.mean(y_pred - y)
        grad_b = np.mean((y_pred - y)*x)
        grad_c = np.mean((y_pred - y)*x**2)
        return np.array([grad_a, grad_b, grad_c])


    def do_it(self, x, y, niters):
        self.eps = 1e-8
        self.init_all()
        for i in range(1, niters):
            y_pred = self.func(self.w, x)
            cur_loss = self.metric(y, y_pred)
            self.loss.append(cur_loss)
            if cur_loss < self.early_stopping:
                print("Early Stopping")
                print(f"Current Loss < {self.early_stopping}:", cur_loss)
                return self.w, self.loss
            grads = self.get_grads(y, y_pred, x)
            #Nadam params calculation
            self.mom1 = self.beta1 * self.mom1 + (1-self.beta1) * grads
            self.mom2 = self.beta2 * self.mom2 + (1-self.beta2) * grads**2
            m1 = (self.beta1 * self.mom1) / (1 - np.power(self.beta1, i+1)) - \
                ((1-self.beta1)*grads)/(1-np.power(self.beta1, i))
            m2 = (self.mom2*self.beta2) / (1 - np.power(self.beta2, i))
            self.w -= (self.eta/(np.sqrt(m2)+self.eps))*m1

        return self.w, self.loss


class batchGD():
    def __init__(self, eta, early_stopping: float = 1e-8):
        self.eta = eta
        self.func = lambda w, x: w[0] + w[1]*x + w[2]*x**2
        self.loss = []
        self.metric = mean_squared_error
        self.early_stopping = early_stopping


    def get_grads(self, y, y_pred, x):
        grad_a = np.mean(y_pred - y)
        grad_b = np.mean((y_pred - y)*x)
        grad_c = np.mean((y_pred - y)*x**2)
        return np.array([grad_a, grad_b, grad_c])


    def do_it(self, x, y, niters):
        self.loss = []
        self.w = np.zeros(shape=(3,))
        indices = np.arange(y.shape[0])
        for _ in range(niters):
            y_pred = self.func(self.w, x)
            cur_loss = self.metric(y, y_pred)
            self.loss.append(cur_loss)
            if cur_loss < self.early_stopping:
                print("Early Stopping")
                print(f"Current Loss < {self.early_stopping}:", cur_loss)
                return self.w, self.loss
            #inplace index shuffling in order to get some randomness
            np.random.shuffle(indices)
            for index in indices:
                y_pred = self.func(self.w, x[index])
                grad = self.get_grads(y[index], y_pred, x[index])
                self.w -= self.eta * grad
        y_pred = self.func(self.w, x)
        self.loss.append(self.metric(y, y_pred))
        return self.w, self.loss
