def logging_decorator(function):
    def wrapper(*args):
        print(f"You called {function.__name__}({args[0]}, {args[1]}, {args[2]})")
        print(f"It returned: {function(args[0], args[1], args[2])}")

    return wrapper

def logging_decorator2(function):
    def wrapper(*args):
        print(f"You called {function.__name__}{args}")
        print(f"It returned: {function(args[0], args[1], args[2])}")

    return wrapper


@logging_decorator
def a_function(var1, var2, var3):
    return var1 + var2 + var3


@logging_decorator2
def a_function2(var1, var2, var3):
    return var1 + var2 + var3


a_function(1, 2, 3)
a_function2(1, 2, 3)
