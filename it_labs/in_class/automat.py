def automat(x, n, m):
    center = n//2
    arr = "".join(str(0) if i!= center else str(1) for i in range(n))
    #print(arr)
    new_rule = "{0:b}".format(x)
    new_rule = new_rule.zfill(8)[::-1]
    while m != 0:
        #print(arr)
        new_arr = '0'
        for i in range(1, len(arr)-1):
            val = arr[i-1:i+2]
            val_int = int(val, 2)
            new_arr += new_rule[val_int]
        new_arr += '0'
        arr = new_arr
        m-=1

if __name__ == "__main__":
    x = 222
    m = 20
    n = 30
    automat(x, n, m)

############################################
## TO DO 
import numpy as np
import functools

def automat_no_loops(x, m, n):
    rule = "{0:b}".format(x)
    rule = list(map(lambda y: int(y), rule.zfill(8)[::-1]))
    arr = np.zeros((n+2,), dtype=int)
    arr[n//2 + 1] = 1
    while m != 0:
        res = list(map(functools.partial(get_decimal, new_rule=rule), rolling_window(arr, 3)))
        m-=1
        print(res)
        arr[1:-1] = np.array(res)

def rolling_window(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

def get_decimal(x, new_rule):
    index = int(str(x[0]) + str(x[1]) + str(x[2]), 2)
    return new_rule[index]