import time
from typing import Callable

import memory_profiler


class Benchmark:
    """
    Helper class for benchmark and profile function
    """
    @staticmethod
    def execute_with_benchmark(f: Callable, *args, **kwargs) -> str:
        """
        Bench callable object with all his child
        :param f: callable object
        :param args: arguments for call object
        :return: time and peak mem for object call
        """
        start_time = time.time()
        mem = int(memory_profiler.memory_usage(proc=(f, args, kwargs),
                                               max_usage=True,
                                               multiprocess=True,
                                               include_children=True))
        end_time = int(time.time() - start_time)
        return f"ok, execution time: {end_time}s, peak memory usage: {mem} Mb"
