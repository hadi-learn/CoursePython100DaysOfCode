def decorator(function):
    def wrapper(**kwargs):
        return kwargs.values()