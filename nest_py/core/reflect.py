from typing import Any


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
    def delete(target: Any, key: str) -> None:
        """
        Delete an attribute from the target object.

        Args:
            target: The object from which to delete the attribute.
            key: The name of the attribute to delete.

        Raises:
            AttributeError: If the attribute does not exist or cannot be deleted.
        """
        delattr(target, key)
