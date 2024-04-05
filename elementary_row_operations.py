from __future__ import annotations

from abc import ABC, abstractmethod
from fractions import Fraction


class ElementaryRowOperation(ABC):
    """Abstract elementary row operation."""

    @abstractmethod
    def inv(self) -> ElementaryRowOperation:
        """Get inverse row operation."""


class RowSwap(ElementaryRowOperation):
    """Swap rows i and j."""

    __match_args__ = ("i", "j")

    def __init__(self, i: int, j: int) -> None:
        if i == j:
            raise ValueError("i == j in RowSwap.")
        self.i = i
        self.j = j

    def __str__(self) -> str:
        return f"P_{{{self.i},{self.j}}}"

    def inv(self) -> RowSwap:
        """Get inverse row operation."""
        return self


class ScalarMultiplication(ElementaryRowOperation):
    """Multiply row i by scalar r."""

    __match_args__ = ("i", "r")

    def __init__(self, i: int, r: Fraction) -> None:
        if r == 0:
            raise ValueError("r = 0 in ScalarMultiplication.")
        self.i = i
        self.r = r

    def __str__(self) -> str:
        return f"D_{{{self.i}}}({self.r})"

    def inv(self) -> ScalarMultiplication:
        """Get inverse row operation."""
        return ScalarMultiplication(self.i, 1 / self.r)


class RowSum(ElementaryRowOperation):
    """Add multiplied by s row j to row i."""

    __match_args__ = ("i", "j", "s")

    def __init__(self, i: int, j: int, s: Fraction = Fraction(1)) -> None:
        if i == j:
            raise ValueError("i == j in RowSum.")

        self.i = i
        self.j = j
        self.s = s

    def __str__(self) -> str:
        return f"T_{{{self.i},{self.j}}}({self.s})"

    def inv(self) -> RowSum:
        """Get inverse row operation."""
        return RowSum(self.i, self.j, -self.s)
