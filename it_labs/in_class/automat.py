vecs = [(1, 1, 1),
        (1, 1, 0),
        (1, 0, 1),
        (1, 0, 0),
        (0, 1, 1),
        (0, 1, 0),
        (0, 0, 1),
        (0, 0 ,0)]


## example gen_bin(10) -> [0, 0, 0, 0, 1, 0, 1, 0]
def gen_bin(x):
    return list(map(lambda x: int(x), list(format(x, '#010b')[2:]))) 


#x - rule, n - vector length
def automat(x, n, m=10):
    center = n//2
    arr = [0 if i!= center else 1 for i in range(n)]
    rules = dict(zip(vecs, gen_bin(x)))
    while m != 0:
        new_vec = [0]
        for i in range(1, len(arr)-1):
            value = rules[tuple(arr[i-1:i+2])]
            new_vec.append(value)
        m -= 1
        new_vec.append(0)
        arr = new_vec
        print(arr)
