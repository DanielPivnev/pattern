from time import time


def debug(func):
    def wrapper(*args):
        if 'debug' in type(args[1].view).__dict__ and args[1].view.debug:
            start = time()
            response = func(*args)
            end = time()

            view_name = type(args[1].view).__name__
            full_time = round(end - start, 3)
            print(f'{view_name} - {full_time}s')

            return response
        else:
            return func(*args)
    return wrapper
