#Actor lifetime
It is always advised to hold external resources only as long as they're
needed, freeing them after that, and actors are not an exception to this.

Actors expose both [context manager protocol][context-managers] and `shutdown`
methods to enable finalizing the actor process once is no longer required.

```python
import uactor

class Actor(uactor.Actor):

    def __init__(self):
        print('Initialized')

    def __enter__(self):
        print('Context enter')
        return super().__enter__()  # return actor proxy

    def __exit__(self, exc_type, exc_value, traceback):
        print('Context exit')
        return super().__exit__(exc_type, exc_value, traceback)  # shutdown

    def shutdown(self):
        print('Shutdown')

with Actor() as actor:
    # Initialized
    # Context enter
    pass
# Context exit
# Shutdown

actor = Actor()
# Initialized
actor.shutdown()
# Shutdown
```
