'''matrix_base.py'''


from typing import List, Iterable, Union, Iterator, Tuple
from abc import ABC, abstractmethod

from mastapy._internal.vector_base import VectorBase, VectorException
from mastapy._internal.scalar import NUM


ERROR_TUPLE = (KeyError, TypeError, AttributeError, IndexError)
MATRIX_TYPE = Union[Iterable[NUM], Iterable[Iterable[NUM]]]
MATRIX_TYPE_OR_NUM = Union[NUM, Iterable[NUM], Iterable[Iterable[NUM]]]

ERROR_COMP_MESSAGE = (
    'Matrices must have equal number of '
    'dimensions for comparison.')


def flatten(self, value: MATRIX_TYPE) -> Tuple[NUM]:
    try:
        return tuple(float(v) for i in value for v in i)
    except IndexError:
        return tuple(float(v) for v in value)


class MatrixException(VectorException):
    '''MatrixExcetion

    Exception raised for errors occurring in the Matrix classes.
    '''


class MatrixBase(ABC):
    '''MatrixBase

    Abstract Base Class for all matrix types.
    '''

    def __init__(self, values: List[float]):
        self._values = values

    def _iter_conv_comp(self, iterable: MATRIX_TYPE) -> Tuple[NUM]:
        values = self._flatten(iterable)

        if len(values) != len(self):
            raise MatrixException(ERROR_COMP_MESSAGE)

        return values

    @classmethod
    @abstractmethod
    def broadcast(cls, value: NUM) -> 'MatrixBase':
        pass

    @classmethod
    @abstractmethod
    def diagonal(cls, value: NUM) -> 'MatrixBase':
        pass

    @classmethod
    @abstractmethod
    def from_iterable(cls, t: Iterable[NUM]) -> 'MatrixBase':
        pass

    @abstractmethod
    def __add__(self, other) -> 'MatrixBase':
        pass

    @abstractmethod
    def __sub__(self, other) -> 'MatrixBase':
        pass

    @abstractmethod
    def __mul__(self, other) -> 'MatrixBase':
        pass

    @abstractmethod
    def __matmul__(self, other) -> Union['MatrixBase', 'VectorBase']:
        pass

    @abstractmethod
    def __truediv__(self, other) -> 'MatrixBase':
        pass

    @abstractmethod
    def __floordiv__(self, other) -> 'MatrixBase':
        pass

    @abstractmethod
    def __abs__(self) -> 'MatrixBase':
        pass

    @abstractmethod
    def __mod__(self, other) -> 'MatrixBase':
        pass

    @abstractmethod
    def __pow__(self, other) -> 'MatrixBase':
        pass

    @abstractmethod
    def __pos__(self, other) -> 'MatrixBase':
        pass

    @abstractmethod
    def __neg__(self, other) -> 'MatrixBase':
        pass

    def __len__(self) -> int:
        return len(self.values)

    def __contains__(self, value: object) -> bool:
        return value in self._values

    @abstractmethod
    def __getitem__(self, index: Union[int, slice]) -> 'VectorBase':
        pass

    @abstractmethod
    def __setitem__(
            self,
            index: Union[int, slice],
            value: MATRIX_TYPE):
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[float]:
        return iter(self._values)

    def __eq__(
            self,
            value: MATRIX_TYPE) -> Tuple[bool]:
        try:
            values = self._iter_conv_comp(value)
            return tuple(
                map(lambda t: t[0] == t[1], zip(self._values, values)))
        except ValueError:
            raise MatrixException(ERROR_COMP_MESSAGE) from None

    def __lt__(
            self,
            value: MATRIX_TYPE) -> Tuple[bool]:
        try:
            values = self._iter_conv_comp(value)
            return tuple(
                map(lambda t: t[0] < t[1], zip(self._values, values)))
        except ValueError:
            raise MatrixException(ERROR_COMP_MESSAGE) from None

    def __le__(
            self,
            value: MATRIX_TYPE) -> Tuple[bool]:
        try:
            values = self._iter_conv_comp(value)
            return tuple(
                map(lambda t: t[0] <= t[1], zip(self._values, values)))
        except ValueError:
            raise MatrixException(ERROR_COMP_MESSAGE) from None

    def __gt__(
            self,
            value: MATRIX_TYPE) -> Tuple[bool]:
        try:
            values = self._iter_conv_comp(value)
            return tuple(
                map(lambda t: t[0] > t[1], zip(self._values, values)))
        except ValueError:
            raise MatrixException(ERROR_COMP_MESSAGE) from None

    def __ge__(
            self,
            value: MATRIX_TYPE) -> Tuple[bool]:
        try:
            values = self._iter_conv_comp(value)
            return tuple(
                map(lambda t: t[0] >= t[1], zip(self._values, values)))
        except ValueError:
            raise MatrixException(ERROR_COMP_MESSAGE) from None

    def __not__(self) -> Tuple[bool]:
        return tuple(map(lambda x: not x, self._values))

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass