'''matrix_2x2.py'''


from mastapy._internal.matrix_base import MatrixBase
from mastapy._internal.scalar import NUM


__all__ = ('Matrix2x2',)


ERROR_2D_MESSAGE = 'Vector must match matrix dimension.'


class Matrix2x2(MatrixBase):
    ''' Create a column-major Matrix2x2 from M11, M12, M21, M22 components.

    Args:
        m11: NUM
        m12: NUM
        m21: NUM
        m22: NUM

    Returns:
        Matrix2x2
    '''

    def __init__(self, m11: NUM, m12: NUM, m21: NUM, m22: NUM) -> 'Matrix2x2':
        super().__init__([float(m11), float(m12), float(m21), float(m22)])

    @classmethod
    def broadcast(cls, value: NUM) -> 'Matrix2x2':
        ''' Create a Matrix2x2 by broadcasting a value to all of its components

        Args:
            value: NUM

        Returns:
            Matrix2x2
        '''

        return cls(value, value, value, value)

    @classmethod
    def diagonal(cls, value: NUM) -> 'Matrix2x2':
        ''' Create a Matrix2x2 by broadcasting a value along the diagonal

        Args:
            value: NUM

        Returns:
            Matrix2x2
        '''

        return cls(value, 0.0, 0.0, value)

    @classmethod
    def from_iterable(
            cls,
            t: Union[Iterable[Iterable[NUM]], Iterable[NUM]]) -> 'MatrixBase':
        try:
            return cls(*[i for sub in t for i in sub])
        except:
            return cls(*[i for i in t])
