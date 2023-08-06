# Actor inheritance

Actor inheritace works just as regular inheritance.

```python
import os
import uactor

class Feline(uactor.Actor):

    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"[{os.getpid()}] Hi, it's {self.name}."

class Cat(Feline):

    def greet(self):
        return f'{super().greet()} Meow.'

class Tiger(Feline):

    def greet(self):
        return f'{super().greet()} Roar.'

cat = Cat('Mr. Whiskers')
tiger = Tiger('Mr. Fangs')

print(f'[{os.getpid()}] Hello everyone.')
# [297381] Hello everyone.

print(cat.greet())
# [299145] Hi, it's Mr. Whiskers. Meow.

print(tiger.greet())
# [299165] Hi, it's Mr. Fangs. Roar.
```

## Configuration inheritance

Actor configuration attributes `_exposed_`, `_proxies_` and
`_method_to_typeid_` are inheritance-aware (that is, all parent values
are honored), so you don't need to carry parent values manually when updating
them.

```python
import uactor

class Parent(uactor.Actor):

    _exposed_ = ('greet',)

    def greet(self):
        return f"It's {type(self).__name__}."

    def private(self):
        return "This method won't be available in the proxy"

class Child(Parent):

    _exposed_ = ('hello',)

    def hello(self):
        return f'{super().greet()} Hello.'

print(Parent().greet())
# It's Parent.

print(Child().greet())
# It's Child.

print(Child().hello())
# It's Child. Hello.

try:
    print(Parent().private())
except AttributeError as e:
    print(e)
    # 'Parent.proxy_class' object has no attribute 'private'

try:
    print(Child().private())
except AttributeError as e:
    print(e)
    # 'Child.proxy_class' object has no attribute 'private'
```
