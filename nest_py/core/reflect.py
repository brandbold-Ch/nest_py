from typing import Any, Optional, Tuple, List, Protocol
from inspect import (
    getmembers,
    isfunction,
    isclass,
    ismethod,
    iscoroutine,
    isasyncgenfunction,
    isabstract,
    isawaitable,
    isdatadescriptor,
    isroutine,
    isasyncgen,
    isbuiltin
)

class FilterType(Protocol):
    def __call__(self, value: Any) -> bool: ...


IS_FUNCTION: FilterType = isfunction
IS_CLASS: FilterType = isclass
IS_METHOD: FilterType = ismethod
IS_COROUTINE: FilterType = iscoroutine
IS_ASYNC_GEN_FUNC: FilterType = isasyncgenfunction
IS_ABSTRACT: FilterType = isabstract
IS_AWAITABLE: FilterType = isawaitable
IS_DATA_DESCRIPTOR: FilterType = isdatadescriptor
IS_ROUTINE: FilterType = isroutine
IS_ASYNC_GEN: FilterType = isasyncgen
IS_BUILTIN: FilterType = isbuiltin


class Reflect:
    """
    Utility class that provides simple reflection helpers for Python objects.

    Methods mirror common reflection operations: getting, setting, checking
    existence, and deleting attributes on arbitrary targets.
    """

    @staticmethod
    def get(target: Any, key: str) -> Any:
        """
        Retrieve an attribute from the target object.

        Args:
            target: The object from which to retrieve the attribute.
            key: The name of the attribute to retrieve.

        Returns:
            The value of the attribute or None.

        """
        return getattr(target, key, None)

    @staticmethod
    def set(target: Any, key: str, value: Any) -> None:
        """
        Set an attribute on the target object.

        Args:
            target: The object on which to set the attribute.
            key: The name of the attribute to set.
            value: The value to assign to the attribute.

        Raises:
            AttributeError: If the attribute cannot be set on the target.
            TypeError: If the operation is not supported for the target.
        """
        setattr(target, key, value)

    @staticmethod
    def has(target: Any, key: str) -> bool:
        """
        Check whether the target object has an attribute with the given name.

        Args:
            target: The object to inspect.
            key: The name of the attribute to check.

        Returns:
            True if the attribute exists, False otherwise.
        """
        return hasattr(target, key)

    @staticmethod
    def deleteProperty(target: Any, key: str) -> None:
        """
        Delete an attribute from the target object.

        Args:
            target: The object from which to delete the attribute.
            key: The name of the attribute to delete.

        Raises:
            AttributeError: If the attribute does not exist or cannot be deleted.
        """
        delattr(target, key)

    @staticmethod
    def getProperties(target: Any, predicate: Optional[FilterType] = None) -> List[Tuple[str, Any]]:
        """
        Return the members of `target` as (name, value) pairs.

        Args:
            target: The object or module to inspect.
            predicate: Optional callable used to filter members (see `inspect.getmembers`).

        Returns:
            A list of `(name, value)` tuples for each member. If `predicate` is provided,
            only members for which `predicate(value)` is True are returned.
        """
        if predicate:
            return getmembers(target, predicate)
        return getmembers(target)

    @staticmethod
    def getFunctions(target: Any) -> List[Tuple[str, Any]]:
        """
        Return functions defined on `target`.

        Args:
            target: The object or module to inspect.

        Returns:
            A list of `(name, function)` tuples for all functions found on `target`.
        """
        return Reflect.getProperties(target, IS_FUNCTION)

    @staticmethod
    def getClasses(target: Any) -> List[Tuple[str, Any]]:
        """
        Return classes defined on `target`.

        Args:
            target: The object or module to inspect.

        Returns:
            A list of `(name, class)` tuples for all classes found on `target`.
        """
        return Reflect.getProperties(target, IS_CLASS)

    @staticmethod
    def getMethods(target: Any) -> List[Tuple[str, Any]]:
        """
        Return methods of `target`.

        Args:
            target: The object or module to inspect.

        Returns:
            A list of `(name, method)` tuples for all methods found on `target`.
        """
        return Reflect.getProperties(target, IS_METHOD)

    @staticmethod
    def getCoroutines(target: Any) -> List[Tuple[str, Any]]:
        """
        Return coroutine functions defined on `target`.

        Args:
            target: The object or module to inspect.

        Returns:
            A list of `(name, coroutine_function)` tuples for async coroutines.
        """
        return Reflect.getProperties(target, IS_COROUTINE)

    @staticmethod
    def getAsyncGenFunctions(target: Any) -> List[Tuple[str, Any]]:
        """
        Return asynchronous generator functions defined on `target`.

        Args:
            target: The object or module to inspect.

        Returns:
            A list of `(name, async_gen_function)` tuples for async generator functions.
        """
        return Reflect.getProperties(target, IS_ASYNC_GEN_FUNC)

    @staticmethod
    def getAbstracts(target: Any) -> List[Tuple[str, Any]]:
        """
        Return abstract members of `target`.

        Args:
            target: The object or module to inspect.

        Returns:
            A list of `(name, value)` tuples for members marked as abstract.
        """
        return Reflect.getProperties(target, IS_ABSTRACT)

    @staticmethod
    def getAwaitables(target: Any) -> List[Tuple[str, Any]]:
        """
        Return awaitable objects found on `target`.

        Args:
            target: The object or module to inspect.

        Returns:
            A list of `(name, awaitable)` tuples for awaitable members.
        """
        return Reflect.getProperties(target, IS_AWAITABLE)

    @staticmethod
    def getDataDescriptors(target: Any) -> List[Tuple[str, Any]]:
        """
        Return data descriptor members of `target`.

        Args:
            target: The object or module to inspect.

        Returns:
            A list of `(name, descriptor)` tuples for data descriptors (e.g., properties).
        """
        return Reflect.getProperties(target, IS_DATA_DESCRIPTOR)

    @staticmethod
    def getRoutines(target: Any) -> List[Tuple[str, Any]]:
        """
        Return routines (functions or bound methods) of `target`.

        Args:
            target: The object or module to inspect.

        Returns:
            A list of `(name, routine)` tuples for routine members.
        """
        return Reflect.getProperties(target, IS_ROUTINE)

    @staticmethod
    def getAsyncGens(target: Any) -> List[Tuple[str, Any]]:
        """
        Return asynchronous generator objects found on `target`.

        Args:
            target: The object or module to inspect.

        Returns:
            A list of `(name, async_gen)` tuples for async generator members.
        """
        return Reflect.getProperties(target, IS_ASYNC_GEN)

    @staticmethod
    def getBuiltins(target: Any) -> List[Tuple[str, Any]]:
        """
        Return builtin members of `target`.

        Args:
            target: The object or module to inspect.

        Returns:
            A list of `(name, builtin)` tuples for builtin members.
        """
        return Reflect.getProperties(target, IS_BUILTIN)
