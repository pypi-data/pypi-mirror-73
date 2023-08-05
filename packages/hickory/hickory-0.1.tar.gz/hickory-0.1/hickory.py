import functools

def task(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("stuff")
        func(*args, **kwargs)
        return "hi"
    return wrapper
