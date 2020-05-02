import functools
from queue import Queue
import random
import time

from .formatting import oxford_join


class sampled:  # pylint: disable=invalid-name
    """
    Implements a way of sampling requests made to a callable.

    Currently implements three strategies:
        - constant: All calls are accepted (rate=0) or refused (rate=1) (default: 1)
        - probabilistic: A percentage of the calls are accepted (ratio between 0 and 1) (default: 0.5)
        - ratelimiting: A fixed number of requests per second are accepted (above 0) (default: 10)

    When a callable decorated with `@sampled` is called and the call is not accepted, `None` is returned

    Inspired from https://github.com/jaegertracing/jaeger-client-python/blob/master/jaeger_client/sampler.py

    Examples:
        ```python
        from flashback import sampled

        # Handles constant sampling
        @sampled()
        def decorated(strategy='constant', rate=1):
            print('Called')

        decorated()
        #=> Called

        # Handles rate limiting per second (here 5)
        @sampled(strategy='ratelimiting', rate=5)
        def decorated():
            print('Called')

        for _ in range(10):
            decorated()
        #=> Called
        #=> Called
        #=> Called
        #=> Called
        #=> Called

        # Probabilistic sampling with a rate of 0.5
        @sampled(strategy='probabilistic')
        def decorated():
            print('Called')

        decorated()
        decorated()
        #=> Called
        ```

    Params:
        - `strategy (str)` the sampling strategy to use
        - `param (int|float)` the parameter to fine-tune the sampling strategy

    Returns:
        - `Callable` a wrapper used to decorate a callable
    """
    STRATEGIES = (
        'constant',
        'probabilistic',
        'ratelimiting',
    )

    def __init__(self, strategy='constant', rate=None):
        if strategy == 'constant':
            if rate is None:
                rate = 1
            elif rate not in {0, 1}:
                raise ValueError(f"Invalid rate {rate!r}, expecting an integer of 0 or 1.")

            self._rate = rate

            self.should_sample = self._sample_constant
        elif strategy == 'probabilistic':
            if rate is None:
                rate = 0.5
            elif not 0 < rate < 1:
                raise ValueError(f"Invalid rate {rate!r}, expecting a float between 0 and 1.")

            self._rate = rate

            self.should_sample = self._sample_probabilistic
        elif strategy == 'ratelimiting':
            if rate is None:
                rate = 10
            elif rate < 0:
                raise ValueError(f"Invalid rate {rate!r}, expecting a positive integer.")

            self._rate = rate
            self._queue = Queue(maxsize=0)

            self.should_sample = self._sample_ratelimiting
        else:
            strategies_choices = oxford_join(self.STRATEGIES, last_sep=', or ')
            raise ValueError(f"Invalid strategy {strategy!r}, expecting {strategies_choices}.")

    def __call__(self, func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            return func(*args, **kwargs) if self.should_sample() else None

        return inner

    def _sample_constant(self):
        return self._rate

    def _sample_probabilistic(self):
        return random.random() < self._rate

    def _sample_ratelimiting(self):
        now = int(time.time())

        queue_size = self._queue.qsize()
        last_second = now - 1
        total_requests = 0
        for timestamp_index, timestamp in enumerate(self._queue.queue):
            if timestamp >= last_second:
                total_requests = queue_size - timestamp_index
                break

        if total_requests >= self._rate:
            return False

        for _ in range(queue_size - total_requests):
            self._queue.get()

        self._queue.put(now)

        return True
