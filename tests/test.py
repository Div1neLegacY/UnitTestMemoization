import time
# Needed for memoization and caching
import functools
import pytest
# Needed for runtime accessibility of system code function calls
#import inspect

'''
Discussion:
Caching and memoization vs. normal expectation of functions and mocking them.
This method I would think is preferrable in integration testing as it still runs
the underlying system code, whereas unit testing is mainly focused on line
coverage and the idea of "mocking" functions to prevent the actual system code from
running.
'''

'''
Decorator example as a timer that prints the runtime of function calls
'''
def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__}() in {run_time:.4f} secs")
        return value
    return wrapper_timer


'''
System-under-test code
'''
class SystemTestCode:
    def waste_some_time(num_times):
        for _ in range(num_times):
            return sum([number**2 for number in range(10_000)])

    def recursive_function(n):
        print("Called recursive_function()")
        if n == 0:
            return 0
        return SystemTestCode.recursive_function(n - 1) + 1

# Same as functools.cache (unbounded cache)
'''
@functools.lru_cache(maxsize=None)  # Cache all results
def expensive_calculation(n):
    # Simulate a time-consuming operation
    return SystemTestCode.waste_some_time(n)

@functools.lru_cache(maxsize=None)  # Cache all results
def expensive_recursion(n):
    SystemTestCode.recursive_function(n)
'''

def apply_lru_cache_to_methods(cls, maxsize=None, typed=False):
    """
    Dynamically applies @lru_cache to all non-special methods of a given class.

    Args:
        cls: The class whose methods are to be decorated.
        maxsize: The maximum size of the cache.
        typed: If True, arguments of different types will be cached separately.
    """
    for name in dir(cls):
        # Exclude special methods (e.g., __init__, __str__)
        if not name.startswith('__') and not name.endswith('__'):
            attribute = getattr(cls, name)
            if callable(attribute):
                # Check if it's a method and not a staticmethod or classmethod
                # (which are handled differently, but generally lru_cache works on them too)
                if hasattr(attribute, '__get__'): # This typically indicates a method or property
                    # Wrap the method with lru_cache
                    setattr(cls, name, functools.lru_cache(maxsize=maxsize, typed=typed)(attribute))
    return cls

# Apply the lru_cache decorator to class and all of its functions
SystemTestCode = apply_lru_cache_to_methods(SystemTestCode)

class TestExpensiveFunction():
    # Called after every test
    def __del__(self) -> None:
        return

    #@unittest.skip("DISABLED")
    @timer
    def test_first_call(self):
        #print("Test test_first_call:")
        result = SystemTestCode.waste_some_time(500)
        print(f"Success! test_first_call finished with result: {result}")

    #@unittest.skip("DISABLED")
    @timer
    def test_cached_call(self):
        #print("Test test_cached_call:")
        # The second call with the same argument will be much faster
        result = SystemTestCode.waste_some_time(500)
        print(f"Success! test_cached_call finished with result: {result}")

    #@unittest.skip("DISABLED")
    @timer
    def test_different_argument(self):
        #print("Test test_different_argument:")
        result = SystemTestCode.waste_some_time(100)
        print(f"Success! test_different_argument finished with result: {result}")

    #@unittest.skip("DISABLED")
    @timer
    def test_recursion_1(self):
        print("Started test_recursion_1")
        result = SystemTestCode.recursive_function(5)
        print(f"test_recursion_1 returns: {result}")

    '''
    *Note* Caching also works when a different argument is a subset of the function stack trace?
    Passing values lower than the cached value '5', will automagically return the correct value
    without running the recursion? Probably uses the inner trace calls and determines this
    '''
    #@unittest.skip("DISABLED")
    @timer
    def test_recursion_2(self):
        print("Started test_recursion_2")
        result = SystemTestCode.recursive_function(5)
        print(f"test_recursion_2 returns: {result}")
        
    #@unittest.skip("DISABLED")
    def test_pyshark(self):
        import pyshark
        bpf_filter = f'tcp and host 127.0.0.1 and port 49743' 
        capture = pyshark.LiveCapture(interface='\\Device\\NPF_Loopback', bpf_filter=bpf_filter)
        
        for packet in capture.sniff_continuously():
            print(packet)
            #import pdb; pdb.set_trace()
            # Use to see all layers in packet
            packet.layers
            # Use to see all field names in layer
            packet.tcp.field_names
            # Get original binary data of field
            packet.ip.addr.binary_value
            # Get integer value of field
            #packet.ip.addr.int_value
        
        capture.close()

    def test_python_stuff(self):
        return
        

    # Might need something like this for memory safety, we are running multiple TestSuites in the same python process.
    # Assuming the TestSuites are calling different methods and we no longer need cache from a previous TestSuite
    @classmethod
    def tearDownClass(cls):
        #functions_list = [method[0] for method in inspect.getmembers(
        #SystemTestCode, predicate=inspect.isfunction)]
        #print(functions_list)
        #name.cache_clear()
        return