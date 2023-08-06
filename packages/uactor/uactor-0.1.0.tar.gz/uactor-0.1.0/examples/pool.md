# Actor pool example

## Client parallelization

Actor pool example where parallelization is achieved at the client side using
threads, calling to a synchronous actor.

```python
import os
import itertools
import multiprocessing.pool
import uactor

class SyncActor(uactor.Actor):
    def getpid(self):
        return os.getpid()

class AsyncActorPool:
    def __init__(self, size, cls, *args, **kwargs):
        self.threadpool = multiprocessing.pool.ThreadPool(size)
        self.pool = [cls(*args, **kwargs) for _ in range(size)]
        self.actors = itertools.cycle(self.pool)

    def call(self, method, *args, **kwargs):
        func = getattr(next(self.actors), method)
        return self.threadpool.apply_async(func, args, kwargs)

    def broadcast(self, method, *args, **kwargs):
        return self.threadpool.map_async(
            lambda actor: getattr(actor, method)(*args, **kwargs),
            self.pool,
            )

    def __enter__(self):
        self.threadpool.__enter__()
        self.broadcast('__enter__').wait()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return any([
            *self.broadcast('__exit__', exc_type, exc_val, exc_tb).get(),
            self.threadpool.__exit__(exc_type, exc_val, exc_tb),
            ])

with AsyncActorPool(4, SyncActor) as pool:
    results = [pool.call('getpid') for _ in range(5)]
    print([result.get() for result in results])
```

## Actor asynchronous results

Actor pool example where parallelization is at the actor side, which returns
`AsyncResult` proxies (see [result proxies](result_proxies.md)).

```python
import os
import itertools
import multiprocessing.pool
import uactor

class AsyncActor(uactor.Actor):
    _method_to_typeid_ = {'getpid': 'AsyncResult'}

    def __init__(self):
        self.threadpool = multiprocessing.pool.ThreadPool(4)

    def getpid(self):
        return self.threadpool.apply_async(os.getpid)

class SyncActorPool:
    def __init__(self, size, cls, *args, **kwargs):
        self.pool = [cls(*args, **kwargs) for _ in range(size)]
        self.actors = itertools.cycle(self.pool)

    def call(self, method, *args, **kwargs):
        return getattr(next(self.actors), method)(*args, **kwargs)

    def __enter__(self):
        for actor in self.pool:
            actor.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return any([
            actor.__exit__(exc_type, exc_val, exc_tb)
            for actor in self.pool
            ])

with SyncActorPool(4, AsyncActor) as pool:
    results = [pool.call('getpid') for _ in range(5)]
    print([result.get() for result in results])
```
