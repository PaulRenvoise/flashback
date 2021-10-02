import cProfile
import functools


def profiled(output=None):
    """
    Profiles a call made to a callable and dump the stats to a file for further analysis.

    By default, prints the stats to a file called f"{func.__name__}.pstats", located in the folder
    from where it has been called.

    To visualize the stats collected during profiling, you can use:
        - snakeviz:
            ```bash
            pip install snakeviz
            snakeviz *.pstats
            ```
        - gprof2dot:
            ```bash
            brew/apt-get/yum/pacman install graphviz
            pip install gprof2dot
            gprof2dot -f pstats *.pstats | dot -Tpng -o heatgraph.png
            ```

    Examples:
        ```python
        from flashback.debugging import profiled

        @profiled()
        def fibonnaci(n):
            if n == 0:
                return 0
            elif n == 1:
                return 1
            else:
                return fibonacci(n - 1) + fibonacci(n - 2)

        fib(10)
        #=> Writes "fib.pstats"

        @profiled("profiled")
        def cached_fibonacci(n, _cache={}):
            if n in _cache:
                return _cache[n]
            elif n > 1:
                return _cache.setdefault(n, cached_fibonacci(n - 1) + cached_fibonacci(n - 2))
            return n

        fib(10)
        #=> Writes "profiled.pstats"
        ```

    Params:
        output (str): the output to write the stats to

    Returns:
        Callable: a wrapper used to decorate a callable
    """
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            profiler = cProfile.Profile()

            result = profiler.runcall(func, *args, **kwargs)

            profiler.dump_stats(output or f"{func.__name__}.pstats")

            return result

        return inner
    return wrapper
