"""
uActor module.

uActor multiprocessing microframework.

See README.md provided in source distributions or available
at the `project repository <https://gitlab.com/ergoithz/uactor>`_.

Copyright (c) 2020, Felipe A Hernandez
MIT License (see LICENSE)

"""

__author__ = 'Felipe A Hernandez'
__email__ = 'ergoithz@gmail.com'
__license__ = 'MIT'
__version__ = '0.1.0'
__all__ = (
    'UActorException',
    'ProxyError',
    'BaseProxy',
    'ActorManager',
    'ActorProxy',
    'Actor',
    'proxy',
    'typeid',
    )

import typing
import functools
import multiprocessing
import multiprocessing.managers


def bootstrap(manager: 'ActorManager',
              cls: typing.Type['Actor'],
              args: typing.Iterable[typing.Any],
              kwargs: typing.Dict[str, typing.Any],
              ) -> None:
    """Actor process initialization function."""
    process = multiprocessing.current_process()
    process._uactor_manager = manager
    process._uactor_class = cls
    process._uactor_owner = cls(*args, **kwargs)


def proxy(value: typing.Any,
          typeid: str = 'auto',
          serializer: str = 'pickle',
          ) -> 'BaseProxy':
    """
    Create serialized proxy from given value and typeid (defaults to `auto`).

    This function can be only used from inside the actor process.
    """
    process = multiprocessing.current_process()
    try:
        server = process._manager_server
        manager = process._uactor_manager
        proxytype = server.registry[typeid][-1]
    except AttributeError:
        raise ProxyError(
            'Proxies can only be created under actor processes',
            ) from None
    except KeyError:
        raise ProxyError(
            f'No proxy is registered with typeid {typeid!r}'
            ) from None
    # FIXME: if someday the connection became required, we would need to
    #        subclass multiprocessing.managers.Server to expose it as a
    #        thread local
    ident, exposed = server.create(None, typeid, value)
    token = multiprocessing.managers.Token(typeid, server.address, ident)
    options = {'manager': manager, 'exposed': exposed, 'incref': False}
    return proxytype(token, serializer, **options)


def typeid(proxy: 'BaseProxy') -> str:
    """Get typeid of given proxy object."""
    try:
        return proxy._token.typeid
    except AttributeError:
        exc_type, exc_message = (
            (ProxyError, 'Cannot get typeid, proxy token not available')
            if isinstance(proxy, BaseProxy) else
            (ValueError, f'Cannot get typeid, {proxy!r} is not a proxy')
            )
        raise exc_type(exc_message) from None


def iter_registry(registry: typing.Mapping[str, tuple],
                  mixin: typing.Type['BaseProxy'],
                  ) -> typing.Generator[typing.Tuple[str, tuple], None, None]:
    """Iterate given manager registry yielding patched dict items."""
    context = globals()
    for typeid, params in registry.items():
        # FIXME: implementation breaking code
        head, proxytype, tail = params[1:3], params[3], params[4:]
        # NOTE: autoproxies' proxytype is a function, but it does not
        #       need patching (they don't ever get to use self._manager)
        if isinstance(proxytype, type) and not issubclass(proxytype, mixin):
            proxytype = type(f'Proxy[{typeid}]', (mixin, proxytype), {})
            context[proxytype.__name__] = proxytype
        yield typeid, (None, *head, proxytype, *tail)


class UActorException(Exception):
    """Base exception for uactor module."""


class ProxyError(UActorException):
    """Exception for errors on proxy logic."""


class BaseProxy(multiprocessing.managers.BaseProxy):
    """
    Base Proxy class.

    This class implements a few workarounds around bugs found in
    :class:`multiprocessing.managers.BaseProxy` by preventing
    :attr:`BaseProxy._manager` from getting lost on both unserialization and
    process forking by recreating it on demand.

    """

    @property
    def _manager(self):
        """Get proxy manager, creating it when necessary if possible."""
        create_manager = (
            self._manager_instance is None and
            self._manager_class and
            self._authkey
            )
        if create_manager:
            self._manager_instance = self._manager_class(
                self._token.address,
                self._authkey,
                self._serializer,
                )
        return self._manager_instance

    @_manager.setter
    def _manager(self, value):
        """Set proxy manager along its, manager_class."""
        if value:
            self._manager_class = type(value)
        self._manager_instance = value

    def __init__(self, *args, **kwargs):
        """Initialize proxy with token and manager."""
        self._manager_instance = None
        self._manager_class = kwargs.pop('manager_class', None)
        self._authkey = None
        super().__init__(*args, **kwargs)

    def __reduce__(self):
        """Implement the pickle reduce protocol."""
        # FIXME: implementation breaking code
        builder, args, *state = super().__reduce__()
        args[3]['manager_class'] = self._manager_class
        return (builder, args, *state)


class ActorManager(multiprocessing.managers.BaseManager):
    """
    Multiprocessing manager for uactor.

    This class implements the following proxies:
    * All proxies from :class:`multiprocessing.managers.SyncManager`.
    * `auto`: dynamic proxy wrapping any object.

    And, additionally, when declared at :attr:`uactor.Actor.manager_class`:
    * All proxies defined in :attr:`uactor.Actor._proxies_`.
    * `actor`: pointing to the current process actor.

    """

    _registry = dict(
        iter_registry(
            multiprocessing.managers.SyncManager._registry,
            BaseProxy,
            ),
        )

    @classmethod
    def typeids(cls):
        """Get tuple of typeid of all registered proxies."""
        return tuple(cls._registry)


ActorManager.register('auto', create_method=False)


class ActorProxy(BaseProxy):
    """
    Actor proxy base class.

    Actors will inherit from this class to create custom implementations based
    on their declared configuration and interface.

    """

    def __enter__(self, *args, **kwargs):
        """Call actor __enter__ method."""
        self._manager.__enter__()
        return self._callmethod('__enter__', args, kwargs)

    def __exit__(self, *args, **kwargs):
        """Call actor __exit__ method and finalize process."""
        try:
            return self._callmethod('__exit__', args, kwargs)
        finally:
            self._manager.shutdown()

    def shutdown(self, *args, **kwargs):
        """Call actor shutdown method and finalize process."""
        try:
            return self._callmethod('shutdown', args, kwargs)
        finally:
            self._manager.shutdown()


class ActorMeta(type):
    """
    Actor metaclass, providing dynamic initialization.

    This metaclass is what takes our declarative actor-based interface and
    dynamically setup the components required by our usage of
    :module:`multiprocessing.manager` functionality.

    """

    def derive_class(self, name: str, base: type, **kwargs):
        """Create child class ensuring will be available to pickle."""
        name = f'{self.__qualname__}.{name}'
        return type(name, (base,), {'__module__': self.__module__, **kwargs})

    def create_proxy_method(self, name):
        """Create proxy method/property from name."""
        wrapped = getattr(self, name, None)
        if callable(wrapped):
            def wrapper(proxy, *args, **kwargs):
                return proxy._callmethod(name, args, kwargs)
            return functools.update_wrapper(wrapper, wrapped), ()

        def fget(proxy):
            return proxy._callmethod('__getattribute__', (name,))

        def fset(proxy, value):
            return proxy._callmethod('__setattr__', (name, value))

        return property(fget, fset), ('__getattribute__', '__setattr__')

    def current_actor(self, actor: typing.Optional['Actor'] = None):
        """Get current process actor object, used as proxy constructor."""
        current = multiprocessing.current_process()._uactor_owner
        if actor not in (None, current):
            # we must not use an invalid proxy on a foreign actor
            raise ProxyError(
                'Proxy \'actor\' cannot be used with foreign actor references',
                )
        return current

    def __init__(self, name, bases, dct):
        """Generate custom proxy and manager classes, and register proxies."""
        base_vars = tuple(map(vars, reversed(self.mro())))
        exposed = [
            name
            for dct in base_vars
            for exposed in (
                (
                    (
                        key
                        for key, value in dct.items()
                        if not key.startswith('_') and callable(value)
                        )
                    if dct.get('_exposed_') is None else
                    dct['_exposed_']
                    ),
                (
                    dct.get('_method_to_typeid_') or ()
                    ),
                )
            for name in exposed
            ]
        properties = [
            (name, *self.create_proxy_method(name))
            for name in exposed
            ]
        exposed.extend(
            requirement
            for name, func, requirements in properties
            for requirement in requirements
            )
        self.proxy_class = self.derive_class(
            'proxy_class',
            self.proxy_class,
            _exposed_=tuple(exposed),
            _method_to_typeid_={
                method: typeid
                for dct in base_vars
                if dct.get('_method_to_typeid_')
                for method, typeid in dct['_method_to_typeid_'].items()
                },
            **{
                name: func
                for name, func, requirement in properties
                if not hasattr(self.proxy_class, name)
                },
            )
        self.manager_class = self.derive_class(
            'manager_class',
            self.manager_class,
            )
        self.manager_class.register(
            typeid='actor',
            callable=self.current_actor,
            proxytype=self.proxy_class,
            create_method=True,
            )
        reserved = {'actor', 'auto'}  # TODO: place it somewhere
        for dct in base_vars:
            for typeid, proxy in (dct.get('_proxies_') or {}).items():
                if typeid in reserved:
                    raise TypeError(f'typeid {typeid!r} is reserved')
                self.manager_class.register(
                    typeid=typeid,
                    proxytype=proxy,
                    create_method=False,
                    )


class Actor(metaclass=ActorMeta):
    """
    Actor base class.

    This is the base class for your actors to inherit from.

    An actor represents a processing unit, which means that when
    instantiating, a new actor process will be started, and the corresponding
    proxy will be returned.

    Actors also implement the context manager interface, and you can override
    both :meth:`Actor.__enter__` and :meth:`Actor.__exit__` to implement your
    own logic, but keep in mind they're both specially handled and calling
    :meth:`ActorProxy.__exit__` will also terminate the process (just
    like calling :meth:`ActorProxy.shutdown`).

    """

    manager_class = ActorManager
    proxy_class = ActorProxy

    _options_: typing.Mapping[str, typing.Any] = {}
    _exposed_: typing.Optional[typing.Tuple[str]] = (
        '__enter__',
        '__exit__',
        'shutdown',
        )
    _proxies_: typing.Mapping[str, typing.Type[BaseProxy]] = {}
    _method_to_typeid_: typing.Mapping[str, str] = {}

    def __init__(self):
        """Initialize actor (stub)."""

    def __new__(cls, *args, **kwargs):
        """Start actor process, initialize actor and return its proxy."""
        process = multiprocessing.current_process()
        owned = (
            getattr(process, '_uactor_class', None) is cls and
            getattr(process, '_uactor_owner', None) is None
            )
        if not owned:
            manager = cls.manager_class(**cls._options_)
            manager.start(bootstrap, (manager, cls, args, kwargs))
            return manager.actor()

        self = super().__new__(cls)
        process._uactor_class = cls
        process._uactor_owner = self  # prevent recursion
        return self

    def __enter__(self):
        """Enter context, return actor proxy."""
        return proxy(self, 'actor')

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Leave context, calls shutdown."""
        self.shutdown()

    def shutdown(self):
        """Perform shutdown work before the process dies (stub)."""
