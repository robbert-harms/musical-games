__author__ = 'Robbert Harms'
__date__ = '2024-04-07'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'

from abc import ABCMeta, abstractmethod

from musical_games.external.exceptions import MissingDependencyError
from musical_games.external.utils import bash_function_exists


class ExternalFunction(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def function_name(cls) -> str:
        """Get the name of the external function we wish to wrap.

        Returns:
            The name of the function we are wrapping
        """

    @classmethod
    @abstractmethod
    def is_available(cls) -> bool:
        """Check if the external function we need is available on the system.

        Returns:
            True if this method is available on the operating system.
        """


class SimpleExternalFunction(ExternalFunction, metaclass=ABCMeta):
    """Simple implementation of the external function type.

    By setting the class attribute `_function_name` we can implement the class methods from the base class.

    Attributes:
        _function_name: the name of the function we are wrapping
    """
    _function_name: str

    @classmethod
    def is_available(cls) -> bool:
        return bash_function_exists(cls._function_name)

    @classmethod
    def function_name(cls) -> str:
        return cls._function_name


class ExternalFunctionFactory(metaclass=ABCMeta):

    @abstractmethod
    def create(self) -> ExternalFunction:
        """A factory for creating external function objects.

        Returns:
            An external function object we can use
        """


class ApplicableExternalFunctionFactory(ExternalFunctionFactory, metaclass=ABCMeta):

    def __init__(self, external_function_types: list[type[ExternalFunction]]):
        """Factory for creating available external functions.

        An external function is marked available when it is available on the operating system.
        This factory scans the provided list of external function types and returns an instance of the
        first type for which the function is available on the operating system.

        If no suitable tool can be found, a `MissingDependencyError` may be raised.
        """
        self._external_function_types = external_function_types
        self._available_functions = [func for func in self._external_function_types if func.is_available()]

    def _check_available(self):
        """Helper function to raise an exception if no available function could be found.

        Raises:
            MissingDependencyError: if none of the function is available.
        """
        if not len(self._available_functions):
            function_names = [func.function_name() for func in self._external_function_types]
            raise MissingDependencyError('No available function could be found on the system. '
                                         f'We tried the following list: {function_names}')


