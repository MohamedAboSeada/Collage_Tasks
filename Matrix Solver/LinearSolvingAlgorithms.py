class LinearAlgorithms:
    def __init__(self, matrix):
        self.matrix = matrix
        self.operations = []
        self.has_sols = True
        self.last_ele = 0
        self.steps = self.reduced_row_echelon_form(self.matrix)
        if self.check_has_sols():
            self.has_sols = True
        else:
            self.has_sols = False

    def add_op(self, operation=None, row1=None, row2=None, factor=None):
        op = {'operation': operation, 'row1': row1,
              'row2': row2, 'factor': factor}
        self.operations.append(op)

    def check_has_sols(self):
        last_row = self.matrix[-1]
        count_zeros = 0
        for i in range(len(last_row)-1):
            if last_row[i] == 0:
                count_zeros += 1
        if count_zeros == len(last_row) - 1 and last_row[-1] != 0 or last_row[-1] == 0:
            self.last_ele = last_row[-1]
            return False
        else:
            return True

    def reduced_row_echelon_form(self, matrix):
        steps = []
        rows = len(matrix)
        cols = len(matrix[0])
        lead = 0

        for r in range(rows):

            if lead >= cols:
                break

            i = r
            while i < rows and matrix[i][lead] == 0:
                i += 1
                if i < rows:
                    matrix[i], matrix[r] = matrix[r], matrix[i]
                    self.add_op("Swap", row1=i+1, row2=r+2)

            # Add this line outside the while loop to handle the case when i == rows
            if i < rows:
                matrix[i], matrix[r] = matrix[r], matrix[i]
                self.add_op("Swap", row1=i+1, row2=r+2)

            if matrix not in steps:
                steps.append([row.copy() for row in matrix])

            pivot = matrix[r][lead]
            if pivot != 0:
                matrix[r] = [elem / float(pivot) for elem in matrix[r]]
                if matrix not in steps:
                    steps.append([row.copy() for row in matrix])
                self.add_op("Scale", row1=r+1, factor=f"{1/pivot:0.2f}")

            for i_row in range(rows):
                if i_row != r:
                    factor = matrix[i_row][lead]
                    matrix[i_row] = [i_elem - factor * r_elem for r_elem,
                                     i_elem in zip(matrix[r], matrix[i_row])]
                    if matrix not in steps:
                        steps.append([row.copy() for row in matrix])
                    self.add_op("Scale + add", row1=r+1,
                                row2=i_row+1, factor=f"{-factor:0.2f}")

            lead += 1

        return steps

class MatrixOperations:
    @staticmethod
    def addition_subtraction(ope,mat1,mat2):
        # check it 2 is able to be added or sub
        row1,row2 = len(mat1),len(mat2)
        col1,col2 = len(mat1[0]),len(mat2[0])
        result = []
        if(row1 == row2 and col1 == col2):
            if(ope == '+'):
                for i in range(row1):
                    row = []
                    for j in range(col1):
                        row.append(mat1[i][j] + mat2[i][j])
                    result.append(row)
            elif(ope == '-'):
                for i in range(row1):
                    row = []
                    for j in range(col1):
                        row.append(mat1[i][j] - mat2[i][j])
                    result.append(row)
        return result
        
    # not working 
    @staticmethod
    def mul(mat1,mat2):
        m = len(mat1)
        n = len(mat1[0])
        b = len(mat2[0])

        result = []

        if(len(mat1[0]) == len(mat2)):
            
            for i in range(m):
                for j in range(b):
                    row = []
                    for k in range(n):
                        row.append(mat1[i][k] * mat2[k][j])
                    result.append(row)

        return result

    @staticmethod
    def transpose(mat):
        result = []
        for i in range(len(mat)):
            row = []
            for j in range(len(mat[0])):
                row.append(mat[j][i])
            result.append(row)
        return result