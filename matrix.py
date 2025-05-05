class Matrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.matrix = []

    def create_from_input(self, input_data):
        for i in range(self.rows):
            row_values = list(map(float, input_data[i].strip().split()))
            if len(row_values) != self.cols:
                raise ValueError(f"Row {i+1} must have {self.cols} elements.")
            self.matrix.append(row_values)

    def add(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must be of the same dimensions to add.")
        result = Matrix(self.rows, self.cols)
        result.matrix = [
            [self.matrix[i][j] + other.matrix[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return result

    def multiply_by_constant(self, constant):
        result = Matrix(self.rows, self.cols)
        result.matrix = [
            [self.matrix[i][j] * constant for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return result

    def multiply_by_matrix(self, other):
        if self.cols != other.rows:
            raise ValueError("Number of columns in Matrix A must equal number of rows in Matrix B.")
        result = Matrix(self.rows, other.cols)
        result.matrix = [
            [
                sum(self.matrix[i][k] * other.matrix[k][j] for k in range(self.cols))
                for j in range(other.cols)
            ]
            for i in range(self.rows)
        ]
        return result

    def transpose(self):
        result = Matrix(self.cols, self.rows)
        result.matrix = [
            [self.matrix[j][i] for j in range(self.rows)]
            for i in range(self.cols)
        ]
        return result

    def determinant(self):
        if self.rows != self.cols:
            raise ValueError("Determinant can only be calculated for square matrices.")
        return self._compute_determinant(self.matrix)

    def inverse(self):
        if self.rows != self.cols:
            raise ValueError("Inverse can only be calculated for square matrices.")
        det = self._compute_determinant(self.matrix)
        if det == 0:
            raise ValueError("Matrix is singular and cannot be inverted.")

        identity = [[float(i == j) for j in range(self.cols)] for i in range(self.rows)]
        mat = [row[:] for row in self.matrix]

        for i in range(self.rows):
            if mat[i][i] == 0:
                for j in range(i+1, self.rows):
                    if mat[j][i] != 0:
                        mat[i], mat[j] = mat[j], mat[i]
                        identity[i], identity[j] = identity[j], identity[i]
                        break
                else:
                    raise ValueError("Matrix is singular and cannot be inverted.")

            factor = mat[i][i]
            mat[i] = [x / factor for x in mat[i]]
            identity[i] = [x / factor for x in identity[i]]

            for j in range(self.rows):
                if j != i:
                    factor = mat[j][i]
                    mat[j] = [a - factor * b for a, b in zip(mat[j], mat[i])]
                    identity[j] = [a - factor * b for a, b in zip(identity[j], identity[i])]

        result = Matrix(self.rows, self.cols)
        result.matrix = identity
        return result

    def _compute_determinant(self, matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        if n == 2:
            return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]

        det = 0
        for c in range(n):
            minor = [row[:c] + row[c+1:] for row in (matrix[1:])]
            det += ((-1) ** c) * matrix[0][c] * self._compute_determinant(minor)
        return det
