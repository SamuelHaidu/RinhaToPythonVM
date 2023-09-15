def add(a, b):
    return a + b

def minus(a, b):
    def useless_fn():
        return a

    return useless_fn() - b

add(10, 10)
