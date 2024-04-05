from fractions import Fraction

from elementary_row_operations import (
    ElementaryRowOperation,
    RowSum,
    RowSwap,
    ScalarMultiplication,
)


class Matrix:
    """Matrix of numbers in Q, can be extended by unit matrix."""

    def __init__(self, items: list[list[Fraction]], *, extend: bool = False) -> None:
        self._extend = extend
        if extend:
            self._items = []
            n = len(items)
            for i, row in enumerate(items):
                extra_cols = [0] * i + [1] + [0] * (n - i - 1)
                self._items.append(row[:] + extra_cols)
        else:
            self._items = items
        self._rows = len(self._items)
        self._cols = len(self._items[0])
        self._operations: list[ElementaryRowOperation] = []

    @property
    def history(self) -> list[ElementaryRowOperation]:
        """History of applied row operations."""
        return self._operations

    def apply(self, operation: ElementaryRowOperation) -> None:
        """Apply row operation."""
        match operation:
            case RowSwap(i, j):
                self._items[i - 1], self._items[j - 1] = (
                    self._items[j - 1],
                    self._items[i - 1],
                )
            case ScalarMultiplication(i, r):
                for k in range(self._cols):
                    self._items[i - 1][k] *= r
            case RowSum(i, j, s):
                for k in range(self._cols):
                    self._items[i - 1][k] += self._items[j - 1][k] * s
            case _:
                raise ValueError("Unknown Row Operation.")

        self._operations.append(operation)

    def undo(self) -> None:
        """Undo last row operation if any."""
        if not self._operations:
            return
        last_op = self._operations.pop()
        self.apply(last_op.inv())
        self._operations.pop()

    def __str__(self) -> str:
        string_table: list[list[str]] = [
            ["" for _ in range(self._cols)] for _ in range(self._rows)
        ]
        max_len_per_col: list[int] = [0 for _ in range(self._cols)]
        for i, row in enumerate(self._items):
            for j, cell in enumerate(row):
                cell_str = str(cell)
                string_table[i][j] = cell_str
                if len(cell_str) > max_len_per_col[j]:
                    max_len_per_col[j] = len(cell_str)

        lines = []
        proper_columns = self._cols - self._rows
        for row in string_table:
            if self._extend:
                left_part = [
                    row[j].rjust(max_len_per_col[j]) for j in range(proper_columns)
                ]
                right_part = [
                    row[j].rjust(max_len_per_col[j])
                    for j in range(proper_columns, self._cols)
                ]
                line = " ".join([*left_part, " | ", *right_part])
            else:
                line = " ".join(
                    value.rjust(max_len_per_col[j]) for j, value in enumerate(row)
                )
            lines.append(line)

        return "\n".join(lines)
