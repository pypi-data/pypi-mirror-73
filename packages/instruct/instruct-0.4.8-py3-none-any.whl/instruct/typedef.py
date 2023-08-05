from __future__ import annotations
import collections.abc
from collections.abc import Mapping as AbstractMapping
from typing import Union, Any, AnyStr, List, Tuple, cast, Optional, Callable, Type

from .utils import flatten_restrict as flatten
from .typing import ICustomTypeCheck


def make_custom_typecheck(func) -> Type[ICustomTypeCheck]:
    """Create a custom type that will turn `isinstance(item, klass)` into `func(item)`
    """
    typename = "WrappedType<{}>"

    class WrappedType(type):
        __slots__ = ()

        def __instancecheck__(self, instance):
            return func(instance)

        def __repr__(self):
            return typename.format(super().__repr__())

    class _WrappedType(metaclass=WrappedType):
        __slots__ = ()

        @staticmethod
        def set_name(name):
            nonlocal typename
            typename = name
            _WrappedType.__name__ = name
            _WrappedType._name__ = name
            return name

    return cast(Type[ICustomTypeCheck], _WrappedType)


def ismetasubclass(cls, metacls):
    return issubclass(type(cls), metacls)


def issubormetasubclass(type_cls, cls, metaclass=False):
    if metaclass is True:
        type_cls = type(type_cls)
    return issubclass(type_cls, cls)


def has_collect_class(
    type_hints: Union[Type, Tuple[Type, ...], List[Type]],
    root_cls: Type,
    *,
    _recursing=False,
    metaclass=False,
):
    if not isinstance(type_hints, (tuple, list)):
        type_hints = (type_hints,)
    for type_cls in type_hints:
        module = getattr(type_cls, "__module__", None)
        if module != "typing":
            continue
        if hasattr(type_cls, "_name") and type_cls._name is None and type_cls.__origin__ is Union:
            if _recursing:
                for child in type_cls.__args__:
                    if isinstance(child, type) and issubormetasubclass(
                        child, root_cls, metaclass=metaclass
                    ):
                        return True
                    if has_collect_class(child, root_cls, _recursing=True, metaclass=metaclass):
                        return True
            continue
        elif isinstance(getattr(type_cls, "__origin__", None), type) and (
            issubclass(type_cls.__origin__, collections.abc.Iterable)
            and issubclass(type_cls.__origin__, collections.abc.Container)
        ):
            if issubclass(type_cls.__origin__, collections.abc.Mapping):
                key_type, value_type = type_cls.__args__
                if has_collect_class(value_type, root_cls, _recursing=True, metaclass=metaclass):
                    return True
            else:
                for child in type_cls.__args__:
                    if isinstance(child, type) and issubormetasubclass(
                        child, root_cls, metaclass=metaclass
                    ):
                        return True
                    elif has_collect_class(child, root_cls, _recursing=True, metaclass=metaclass):
                        return True
    return False


def create_custom_type(container_type, *args):
    if getattr(container_type, "__module__", None) == "typing":
        if (
            hasattr(container_type, "_name")
            and container_type._name is None
            and container_type.__origin__ is Union
        ):
            types = flatten(
                (create_custom_type(arg) for arg in container_type.__args__), eager=True
            )

            def test_func(value):
                return isinstance(value, types)

        elif container_type is AnyStr:
            return (bytes, str)
        elif container_type is Any:
            return object
        elif isinstance(getattr(container_type, "__origin__", None), type) and (
            issubclass(container_type.__origin__, collections.abc.Iterable)
            and issubclass(container_type.__origin__, collections.abc.Container)
        ):
            return parse_typedef(container_type)
        else:
            raise NotImplementedError(container_type, container_type._name)
    elif isinstance(container_type, type) and (
        issubclass(container_type, collections.abc.Iterable)
        and issubclass(container_type, collections.abc.Container)
    ):
        test_func = create_typecheck_container(container_type, args)
    elif isinstance(container_type, type) and not args:
        return container_type
    else:
        assert isinstance(container_type, tuple), f"container_type is {container_type}"

        def test_func(value):
            return isinstance(value, container_type)

    return make_custom_typecheck(test_func)


def create_typecheck_container(container_type, items: Tuple[Any]):
    test_types = []
    test_func: Optional[Callable[[Any], bool]] = None

    if issubclass(container_type, tuple):
        container_type = tuple
        # Special support: Tuple[type, ...]
        if any(item is Ellipsis for item in items):
            if len(items) != 2:
                raise TypeError("Tuple[type, ...] is allowed but it must be a two pair tuple!")
            homogenous_type_spec, ellipsis = items
            if ellipsis is not Ellipsis or homogenous_type_spec is Ellipsis:
                raise TypeError(
                    "Tuple[type, ...] is allowed but it must have ellipsis as second arg"
                )
            homogenous_type = parse_typedef(homogenous_type_spec)

            def test_func(value):
                if not isinstance(value, container_type):
                    return False
                return all(isinstance(item, homogenous_type) for item in value)

            return test_func

        else:
            for some_type in items:
                test_types.append(create_custom_type(some_type))

            def test_func(value):
                if not isinstance(value, container_type):
                    return False
                if len(value) != len(test_types):
                    raise ValueError(f"Expecting a {len(test_types)} value tuple!")
                for index, (item, item_type) in enumerate(zip(value, test_types)):
                    if not isinstance(item, item_type):
                        # raise TypeError(f"{item!r} at index {index} should be a {item_type}")
                        return False
                return True

    elif issubclass(container_type, AbstractMapping):
        if items:
            key_type_spec, value_type_spec = items
            key_type = parse_typedef(key_type_spec)
            value_type = parse_typedef(value_type_spec)

            def test_func(mapping) -> bool:
                if not isinstance(mapping, container_type):
                    return False
                for key, value in mapping.items():
                    if not all((isinstance(key, key_type), isinstance(value, value_type))):
                        return False
                return True

    if test_func is None:
        if items:
            for some_type in items:
                test_types.append(create_custom_type(some_type))
            test_types = tuple(test_types)

            def test_func(value):
                if not isinstance(value, container_type):
                    return False
                return all(isinstance(item, test_types) for item in value)

        else:

            def test_func(value):
                return isinstance(value, container_type)

    return test_func


def is_typing_definition(item):
    if getattr(item, "__module__", None) == "typing":
        return True
    return False


def parse_typedef(typedef: Union[Tuple[Type, ...], List[Type]]) -> Union[Type, Tuple[Type]]:
    """
    Break a type def into types suitable for doing an isinstance(item, ...) check.

    typeA -> typeA
    (typeA, typeB) -> (typeA, typeB)
    Union[typeA, typeB] -> (typeA, typeB)
    Optional[typeA] -> (NoneType, typeA)

    Support collection typelimiting like

    List[int] -> (IntList,) where IntList is a custom type with a special
    metaclass that executes an embedded function for checking if all members
    of the collection is the right type. i.e all(isintance(item, int) for item in object)
    """
    if type(typedef) is tuple or type(typedef) is list:
        return tuple(parse_typedef(x) for x in typedef)
    if not is_typing_definition(typedef):
        # ARJ: Okay, we're not a typing module descendant.
        # Are we a type itelf?
        if isinstance(typedef, type):
            return typedef
        raise NotImplementedError(f"Unknown typedef definition {typedef!r} ({type(typedef)})!")

    if typedef is AnyStr:
        return str, bytes
    elif typedef is Any:
        return object
    elif typedef is Union:
        raise TypeError("A bare union means nothing!")
    elif hasattr(typedef, "_name"):
        if typedef._name is None:
            # special cases!
            if typedef.__origin__ is Union:
                return flatten(
                    (parse_typedef(argument) for argument in typedef.__args__), eager=True
                )
            raise NotImplementedError(
                f"The type definition for {typedef} is not supported, report as an issue."
            )
        if hasattr(typedef, "_special"):
            if not typedef._special:  # this typedef is specific!
                cls = create_custom_type(typedef.__origin__, *typedef.__args__)
                cls.set_name(str(typedef).replace("typing.", ""))
                return cls
        return (typedef.__origin__,)
    raise NotImplementedError(
        f"The type definition for {typedef!r} is not supported yet, report as an issue."
    )
