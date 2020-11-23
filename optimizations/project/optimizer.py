import numpy as np
from sklearn.metrics import mean_squared_error


class Nadam():
    def __init__(self, eta: float, beta1: float, beta2: float, early_stopping: float=1e-6):
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
        grad_a = 2*np.mean(y_pred - y)
        grad_b = 2*np.mean((y_pred - y)*x)
        grad_c = 2*np.mean((y_pred - y)*x**2)
        return np.array([grad_a, grad_b, grad_c])


    def do_it(self, x, y, niters):
        self.eps = 1e-8
        self.init_all()
        for i in range(1, niters):
            y_pred = self.func(self.w, x)
            cur_loss = self.metric(y, y_pred)
            self.loss.append(cur_loss)
            grads = self.get_grads(y, y_pred, x)
            #Nadam params calculation
            self.mom1 = self.beta1 * self.mom1 + (1-self.beta1) * grads
            self.mom2 = self.beta2 * self.mom2 + (1-self.beta2) * grads**2
            m1 = (self.beta1 * self.mom1) / (1 - np.power(self.beta1, i+1)) - \
                ((1-self.beta1)*grads)/(1-np.power(self.beta1, i))
            m2 = (self.mom2*self.beta2) / (1 - np.power(self.beta2, i))
            prev_w = self.w.copy()
            self.w -= (self.eta/(np.sqrt(m2)+self.eps))*m1

            if abs(np.linalg.norm(self.w - prev_w)) < self.early_stopping:
                print("Early Stopping")
                print(f"Current difference < {self.early_stopping}:", abs(self.w - prev_w))
                return self.w, self.loss
        return self.w, self.loss


class batchGD():
    def __init__(self, eta: float = 1e-2, decay_rate: float = 0.99,  early_stopping: float = 1e-6, decay_counter: int = 1000):
        self.eta = eta
        self.func = lambda w, x: w[0] + w[1]*x + w[2]*x**2
        self.loss = []
        self.metric = mean_squared_error
        self.early_stopping = early_stopping
        self.cache = [eta]
        self.lr_decay = decay_rate
        self.decay_counter = decay_counter #LR decay each decay_counter steps


    def get_grads(self, y, y_pred, x):
        grad_a = np.mean(y_pred - y)
        grad_b = np.mean((y_pred - y)*x)
        grad_c = np.mean((y_pred - y)*x**2)
        return np.array([grad_a, grad_b, grad_c])


    def do_it(self, x, y, niters):
        self.loss = []
        self.w = np.zeros(shape=(3, ))
        self.eta = self.cache[0]
        data_size = y.shape[0]
        lr_history = []
        indices = np.arange(data_size)
        e = 0
        for i in range(niters):
            
            #Shuffle Data each epoch.
            if i % data_size == 0:
                np.random.shuffle(indices)
                e += 1
            
            #Getting loss and prediction
            y_pred = self.func(self.w, x)
            cur_loss = self.metric(y, y_pred)
            self.loss.append(cur_loss)
            
            #take "random" index. We can assume random choice because of shuffling at each epoch.
            index = indices[i %  data_size]
            
            #getting prediction for specific element to get gradient and weigths update
            y_pred = self.func(self.w, x[index])
            grad = self.get_grads(y[index], y_pred, x[index])
            prev_w = self.w.copy()
            self.w -= self.eta * grad
            lr_history.append(self.eta)

            if abs(self.w - prev_w).all() < self.early_stopping:
                print("Early Stopping")
                print(f"Current difference < {self.early_stopping}:", abs(self.w - prev_w))
                return self.w, self.loss, lr_history, e

            if i % self.decay_counter == 0:
                self.eta *= self.lr_decay
            
        y_pred = self.func(self.w, x)
        self.loss.append(self.metric(y, y_pred))
        return self.w, self.loss, lr_history, e
