# Result proxies

Two different approaches are available enabling returning proxies to object
living inside the actor process: declarative and wrapping, both available to
support different use-cases:

* Defining the method proxy via `uactor.Actor._method_to_typeid_` results in
  the specified proxy to be returned only when called from actor proxy, so
  calls from within the actor itself will still receive the actual result.
* Using `uactor.proxy` helper to explicitly specify a proxy from the method,
  so you can to dynamically choose between different proxies and return values.
  These proxies will only be functional when received by the main process or
  other actors.

```python
import uactor

class Actor(uactor.Actor):
    _method_to_typeid_ = {'get_declarative_proxy_to_data': 'list'}

    def __init__(self):
        self.data = [1, 2, 3]

    def get_declarative_proxy_to_data(self):
        return self.data

    def get_serialized_proxy_to_data(self):
        return uactor.proxy(self.data, 'list')

with Actor() as actor:

    proxy = actor.get_declarative_proxy_to_data()
    print(type(proxy), uactor.typeid(proxy), list(proxy))
    # <class 'multiprocessing.managers.ListProxy'> list [1, 2, 3]

    proxy = actor.get_serialized_proxy_to_data()
    print(type(proxy), uactor.typeid(proxy), list(proxy))
    # <class 'multiprocessing.managers.ListProxy'> list [1, 2, 3]
```

## Serialized proxies

The serialized proxy pattern is useful when you need to conditionally return
different proxies or values.

When `uactor.proxy` is called, a new proxy is created for the given value
and typeid, which can be transferred safely to other processes.

```python
import uactor

class Actor(uactor.Actor):

    def __init__(self):
        self.data = [1, 2, 3]

    def get_data(self, as_proxy=False):
        return uactor.proxy(self.data, 'list') if as_proxy else self.data

with Actor() as actor:

    value = actor.get_data()
    print(type(value), value)
    # <class 'list'> [1, 2, 3]

    proxy = actor.get_data(as_proxy=True)
    print(type(proxy), list(proxy))
    # <class 'multiprocessing.managers.ListProxy'> [1, 2, 3]
```

## Synchronization proxies

uActor makes quite easy to share synchronization primitives between processes,
by including specific proxies for this such as `Event`, `Lock`, `RLock`,
`Semaphore`, `BoundedSemaphore`, `Condition` and `Barrier`, which can be
used with primitives from `threading`, or even `multiprocessing` (albeit
using proxies to `multiprocessing` should be avoided):

```python
import threading
import uactor

class Actor(uactor.Actor):
    _exposed_ = ('event',)

    @property
    def event(self):
        return uactor.proxy(self._event, 'Event')

    def __init__(self):
        self._event = threading.Event()

with Actor() as actor:
    print('Ready' if actor.event.wait(1) else 'Not ready')
    # Not ready

    actor.event.set()

    print('Ready' if actor.event.wait(1) else 'Not ready')
    # Ready
```

## Asynchronous proxies

uActor includes those extremely useful `Pool` and `AsyncResult` (for
(for `multiprocessing.pool.Pool`) and `Queue` (for `queue.Queue`) proxies.

This allow to parallelize work across multiple actors way easier than using
raw primitives, just by sharing asynchronous result objects or queues.

```python
import time
import multiprocessing.pool
import uactor

class Actor(uactor.Actor):
    _exposed_ = ('pool',)

    @property
    def pool(self):
        return uactor.proxy(self._pool, 'Pool')

    def __init__(self):
        self._pool = multiprocessing.pool.ThreadPool()

with Actor() as actor:
    start = time.time()
    async_result = actor.pool.apply_async(time.sleep, (2,))
    print(f'{round(time.time() - start, 4)}s')
    # 0.0014s

    async_result.get()
    print(f'{round(time.time() - start, 4)}s')
    # 2.0032s
```
