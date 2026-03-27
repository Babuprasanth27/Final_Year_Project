import time


def log_time(func):
    """Decorator to log the execution time of a function."""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"⏱️ {func.__name__} executed in {end - start:.2f}s")
        return result
    return wrapper
