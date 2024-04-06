from fractions import Fraction

from auto_eliminator import AutoEliminator
from elementary_row_operations import RowSum, RowSwap, ScalarMultiplication
from matrix import Matrix


def input_matrix(extend: bool = True) -> Matrix:
    print("Input matrix (blank line for done):")
    i = 1
    items: list[list[Fraction]] = []
    while True:
        line = input(f"Row {i} > ")
        if not line.strip():
            break
        new_items = [Fraction(item) for item in line.split()]
        if i > 1 and len(items[-1]) != len(new_items):
            print("Column number doesn't match. Try again.")
            continue
        items.append(new_items)
        i += 1

    return Matrix(items, extend=extend)


def display_matrix(matrix: Matrix) -> None:
    print()
    print(matrix)
    print()


def perform_operations(matrix: Matrix) -> Matrix:
    print("Input row operations: P, D, T, undo or auto")
    n_op = 1
    while True:
        op = None
        line = input(f"Op {n_op} > ")
        match line.split():
            case ["undo"]:
                if n_op > 1:
                    matrix.undo()
                    display_matrix(matrix)
                    n_op -= 1
            case ["auto"]:
                auto_eliminator = AutoEliminator(matrix)
                auto_eliminator.eliminate()
                display_matrix(matrix)
                break
            case ["P", i, j]:
                op = RowSwap(int(i), int(j))
            case ["D", i, r]:
                op = ScalarMultiplication(int(i), Fraction(r))
            case ["T", i, j]:
                op = RowSum(int(i), int(j))
            case ["T", i, j, s]:
                op = RowSum(int(i), int(j), Fraction(s))
            case []:
                break
            case _:
                print("Unknown operation.")
                print("Input row operations: P, D, T or undo")

        if op is not None:
            matrix.apply(op)
            display_matrix(matrix)
            n_op += 1

    return matrix


def display_history(matrix: Matrix) -> None:
    for i, op in enumerate(matrix.history, start=1):
        print(i, op)


def main():
    matrix = input_matrix()
    print("Your matrix:")
    display_matrix(matrix)

    matrix = perform_operations(matrix)
    display_history(matrix)


if __name__ == "__main__":
    main()
