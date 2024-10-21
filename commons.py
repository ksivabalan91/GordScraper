import time
import functools

def timer(func):
    """Decorator that prints the time a function takes to execute."""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.time()  # Start time
        result = func(*args, **kwargs)  # Call the function
        end_time = time.time()  # End time
        elapsed_time = end_time - start_time  # Calculate elapsed time
        print(f"Function '{func.__name__}' took {elapsed_time:.4f} seconds to complete.")
        return result
    return wrapper_timer
