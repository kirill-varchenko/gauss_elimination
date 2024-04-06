from elementary_row_operations import RowSum, RowSwap, ScalarMultiplication
from matrix import Matrix


class AutoEliminator:
    def __init__(self, matrix: Matrix) -> None:
        self.matrix = matrix
        self.cur_row = 1

    def find_non_zero_element_row(self, col: int) -> int | None:
        for i in range(self.cur_row, self.matrix.rows + 1):
            if self.matrix[i, col] != 0:
                return i
        return None

    def process_col(self, col: int) -> None:
        i = self.find_non_zero_element_row(col)
        if i is None:
            # only zeros in this col below current row
            return

        if i != self.cur_row:
            # move non zero row to current position
            self.matrix.apply(RowSwap(self.cur_row, i))

        if self.matrix[self.cur_row, col] != 1:
            # normalize pivot element
            self.matrix.apply(
                ScalarMultiplication(self.cur_row, 1 / self.matrix[self.cur_row, col]),
            )

        # eliminate other values in col
        for i in range(1, self.matrix.rows + 1):
            if i == self.cur_row:
                continue
            if self.matrix[i, col] == 0:
                continue
            self.matrix.apply(RowSum(i, self.cur_row, -self.matrix[i, col]))

        self.cur_row += 1

    def eliminate(self) -> Matrix:
        for col in range(1, self.matrix.cols + 1):
            self.process_col(col)
        return self.matrix
