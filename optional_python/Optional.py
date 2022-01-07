from typing import Any, Type, TypeVar, Generic, Callable

T = TypeVar('T')
NT = TypeVar('NT')

class Optional(Generic[T]):
    """
    This class is meant to avoid use of None checking and throwing strange related exceptions.

    Args:
        Generic ([type]): The type of the object that will be stored in the Optional.
    """

    # ==== AVOID PUBLIC CONSTRUCTOR ====
    def __init__(self, obj: T) -> None:
        """The constructor is not meant to be used by the user. 
        Else it is advised to use either of the 3 static methods :
            - of
            - of_nullable
            - empty
        """
        self._obj = obj

    def __call__(cls, *args, **kwargs):
        raise TypeError(
            f"{cls.__module__}.{cls.__qualname__} has no public constructor"
        )

    def _create(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        return super().__call__(*args, **kwargs)  # type: ignore

    # ====  ====

    def get(self) -> T:
        """Return the object contained in the Optional

        Raises:
            TypeError: If nothing is in the object

        Returns:
            T: The object in the optional
        """
        if self._obj is None:
            raise TypeError("Optional contains no object")
        return self._obj

    def is_present(self) -> bool:
        """Check if the Optional contains any non-None object.
        """
        return self._obj is not None

    def is_empty(self) -> bool:
        """Check if the Optional does not contain any object 
        """
        return self._obj is None

    def if_present(self, consumer: Callable[[T], None]) -> None:
        """If optional is not empty, do a specified operation on it.

        Args:
            consumer (Callable[[T], None]): The consumer (a non-returning function) to use.
        """
        if self.is_present():
            consumer(self._obj)

    def map(self, function: Callable[[T], NT]) -> "Optional[NT]":
        """If contains an object, transform it to another

        Returns:
            Optional[NT]: A new optional containing the new element
        """
        if self.is_present():
            new_obj: NT = function(self._obj)
            return Optional.of_nullable(new_obj)
        else:
            return Optional.empty()

    def filter(self, predicate: Callable[[T], bool]) -> "Optional[T]":
        """If the predicate is False or the optional is already empty,
        return an empty optional. Else, return the same optional.
        """
        if self.is_empty() or predicate(self._obj):
            return self
        else:
            return Optional.empty()

    def or_else(self, other_value: T) -> T:
        """Returns the object contained in the optional if exists or a
        default one

        Args:
            other_value (T): The output if optional is empty

        Returns:
            T: The object in the optional or "other_value"
        """
        if self.is_present():
            return self._obj
        else:
            return other_value

    def or_else_get(self, provider: Callable[[], T]) -> T:
        """Same as "or_else", but the default value is a provider function.
        Useful if the default value is expensive to get (like querying a database
        for example).

        Args:
            provider (Callable[[], T]): the function to call if optional empty

        Returns:
            T: The optional content or the provider output.
        """
        if self.is_present():
            return self._obj
        else:
            return provider()

    def or_else_throw(self, exception_provider: Callable[[], Type[Exception]]=TypeError.__new__) -> T:
        """Returns the object in optional or raises the exception
        created by the method provided

        Args:
            exception_provider (Callable[[], Type[Exception]]): the exception creator

        Raises:
            exception_provider: a specified exception if optional is empty

        Returns:
            T: The object in the optional
        """
        if self.is_empty():
            raise exception_provider()
        else:
            return self._obj

    @classmethod
    def of(cls, obj: T) -> "Optional[T]":
        """Create an optional with a non "None" value.
        If obj is None, an exception is thrown

        Raises:
            AttributeError: If the object is None

        Returns:
            T: The optional containing the object (in this case containing a non-None object)
        """
        if obj is None:
            raise AttributeError("The object provided is None, not allowed")
        return cls(obj)

    @classmethod
    def of_nullable(cls, obj: T) -> "Optional[T]":
        """Create an optional with a possible "None" value.

        Returns:
            T: The optional containing the object of nothing
        """
        return cls(obj)

    @classmethod
    def empty(cls) -> "Optional[T]":
        """Create an optional without any value inside

        Returns:
            [type]: An empty optional
        """
        return cls(None)
