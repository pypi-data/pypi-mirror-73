# Method callbacks

One common pattern in the actor programming model is using the result of
a method call as parameter of another one. This is called callback, and can
be used in many contexts to avoid blocking the main application process
while waiting for results.

This can be very useful when used along with asynchronous
[result proxies](./result_proxies.md).

```python
import uactor

class ActorA(uactor.Actor):

    def send(self, target):
        return target('ping')

class ActorB(uactor.Actor):

    def receive(self, value):
        return 'pong' if value == 'ping' else 'error'


actor_a = ActorA()
actor_b = ActorB()
print(actor_a.send(actor_b.receive))
# pong
```
