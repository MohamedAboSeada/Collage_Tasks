import sys
import re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from LinearSolvingAlgorithms import LinearAlgorithms as LA
from LinearSolvingAlgorithms import MatrixOperations as MO
# Main Form Window Class
class Main_form(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('AppUi/mainform.ui', self)
        self.sub_forms = []

        # hide some frames at the start of the program
        self.frame_2.hide()
        self.warn1.hide()
        self.op_group.hide()

        # Conecting slots and signlas
        self.WayOne.clicked.connect(self.show_frame1)
        self.SolveTwo.clicked.connect(self.show_frame2)
        self.Generate.clicked.connect(self.show_Generate_equations)
        self.generate_2.clicked.connect(self.show_Generate_mat)
        self.op_button.clicked.connect(self.show_op_group)
        
        # Connect operations buttons with the dialog
        self.add.clicked.connect(lambda : self.show_operation_dialog('Addition'))
        self.sub.clicked.connect(lambda : self.show_operation_dialog('Subtraction'))
        self.mul.clicked.connect(lambda : self.show_operation_dialog('Multiplication'))

    # show equations frame
    def show_frame1(self):
        self.frame.show()
        self.frame_2.hide()
        self.op_group.hide()

    # show matrix based frame
    def show_frame2(self):
        self.frame.hide()
        self.frame_2.show()
        self.op_group.hide()

    def show_op_group(self):
        self.frame_2.hide()
        self.frame.hide()
        self.op_group.show()
    
    def show_operation_dialog(self,op):
        self.opd = operations_dialog(op)
        self.sub_forms.append(self.opd)
        self.opd.show()

    # show the Generate matrix window with solve
    def show_Generate_mat(self):
        self.generate_mat = Generate_mat()
        self.generate_mat.create_matrix(
            int(self.comboBox.currentText()), int(self.comboBox_2.currentText()))
        self.generate_mat.show()
        self.sub_forms.append(self.generate_mat)

    # show generate matrix window with solve
    def show_Generate_equations(self):
        self.generate_equations = Generate_equations()
        try:
            self.generate_equations.createLineEdits(self.numberEqs.text())
        except:
            self.warn1.show()
        else:
            self.warn1.hide()
            self.generate_equations.show()
            self.sub_forms.append(self.generate_equations)

    # this function closes all sub opened forms when the main form closed
    def closeEvent(self, event):
        for sub_form in self.sub_forms:
            sub_form.close()
        event.accept()
        
# Generate Matrix Dialog class to make object from it
class Generate_mat(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('AppUi/generate_mat.ui', self)
        self.sub_forms = []
        self.matrix = []
        self.pushButton.clicked.connect(self.solve)
        self.warn.hide()
    # create a matrix layout to make user enter the values
    # depend on given rows and cols in combo boxs

    def create_matrix(self, rows, cols):
        for i in range(rows):
            for j in range(cols):
                self.ele = QLineEdit()
                self.ele.setPlaceholderText(f"e:{i+1},{j+1}")
                self.gridLayout.addWidget(self.ele, i, j)

    # check all the inputs after solve
    def checkAllInputs(self):
        allChecked = True
        for i in range(self.gridLayout.rowCount()):
            row = []
            for j in range(self.gridLayout.columnCount()):
                item = self.gridLayout.itemAtPosition(i, j)
                widget = item.widget()
                if (len(widget.text().strip()) == 0):
                    allChecked = False
                    break
                else:
                    if (int(widget.text().strip()) != 0):
                        row.append(int(widget.text().strip()))
                    else:
                        row.append(0)

            self.matrix.append(row)
        return allChecked

    # when hit solve button the solve dialog show up to view the solve
    def solve(self):
        if (self.checkAllInputs()):
            self.steps_window = Steps_dialog()
            self.steps_window.get_matrix(self.matrix)
            self.steps_window.show()
            self.sub_forms.append(self.steps_window)
            self.warn.hide()
        else:
            self.warn.show()

    # this function closes all sub opened forms when the main form closed
    def closeEvent(self, event):
        for sub_form in self.sub_forms:
            sub_form.close()
        event.accept()
# Generate equations Dialog for enter equation and generate matrix from it


class Generate_equations(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('AppUi/generate_eq.ui', self)
        self.sub_forms = []
        self.matrix = []
        self.pushButton.clicked.connect(self.solve)
        self.help_btn.clicked.connect(self.help)
        self.warn.hide()

    # generate some line edits for the number of equations
    def createLineEdits(self, number):
        for i in range(int(number)):
            self.eq = QLineEdit()
            self.eq.setPlaceholderText(f"equation {i+1}")
            self.verticalLayout_3.addWidget(self.eq)

    # check all line edits before solve
    def checkAll(self):
        allChecked = True
        for i in range(self.verticalLayout_3.count()):
            item = self.verticalLayout_3.itemAt(i)
            widget = item.widget()
            row = []
            if (len(widget.text().strip()) == 0):
                allChecked = False
                break
            else:
                row = re.findall(r'[-+]?\d+', widget.text().strip())
                for i in range(len(row)):
                    row[i] = int(row[i])
            self.matrix.append(row)
        return allChecked

    # view the solve window that show the solve of the given equations
    def solve(self):
        if (self.checkAll()):
            self.steps_window = Steps_dialog()
            self.steps_window.get_matrix(self.matrix)
            self.steps_window.show()
            self.sub_forms.append(self.steps_window)
            self.warn.hide()
        else:
            self.warn.show()
            
    def help(self):
        self.helpd = help_dialog()
        self.sub_forms.append(self.helpd)
        self.helpd.show()
        
    def closeEvent(self, event):
        for sub_form in self.sub_forms:
            sub_form.close()
        event.accept()

# steps dialog (solve dialog) That shows the steps and the operation
# that done on the matrix and the solve vector for the linear system

class Steps_dialog(QDialog):
    def __init__(self, parent=None, matrix=None):
        super().__init__(parent)
        loadUi('AppUi/steps.ui', self)
        self.matrix = []
        self.steps = []
        self.operations = []
        self.start = 0
        self.solve_vector.hide()
        self.Indecator.hide()
        self.next_step.clicked.connect(self.show_next)
        self.last_step.clicked.connect(self.show_last)
        self.skip_all.clicked.connect(self.skip_all_steps)
        self.first_step.clicked.connect(self.show_first_step)
        
    def get_matrix(self,matrix):
        self.matrix = matrix
        self.show_step(self.matrix)
        self.perform_rref_and_return_steps()
        self.start = 0
        self.show_op()
    
    def show_op(self):
        if (self.operations[self.start].get('row1') == None and self.operations[self.start].get('row2') == None and self.operations[self.start].get('factor') == None):
            self.operations_label.setText(
                f"{self.operations[self.start].get('operation')}")
        elif (self.operations[self.start].get('row2') == None):
            self.operations_label.setText(
                f"{self.operations[self.start].get('operation')} : {self.operations[self.start].get('factor')} * R{self.operations[self.start].get('row1')}")
        elif (self.operations[self.start].get('factor') == None):
            self.operations_label.setText(
                f"{self.operations[self.start].get('operation')} : R{self.operations[self.start].get('row1')} <-> R{self.operations[self.start].get('row2')}")
        else:
            self.operations_label.setText(
                f"{self.operations[self.start].get('operation')} : {self.operations[self.start].get('factor')} * R{self.operations[self.start].get('row1')} + R{self.operations[self.start].get('row2')}")
    
    # perform rref on the fetced matrix to get steps
    def perform_rref_and_return_steps(self):
        la = LA(self.matrix)
        self.steps = la.steps
        self.operations = la.operations
        
        if (la.has_sols):
            self.Indecator.show()
            self.Indecator.setText("Status : This Matrix Has only one solution")
        else:
            self.next_step.setEnabled(False)
            self.last_step.setEnabled(False)
            self.skip_all.setEnabled(False)
            self.first_step.setEnabled(False)
            if (la.last_ele == 0):
                self.Indecator.show()
                self.Indecator.setText("Status : This Matrix Has infinity number of solutions")
            else:
                self.Indecator.show()
                self.Indecator.setText("Status : This Matrix Has no solutions")

    # show the original matrix inside the grid widget
    def show_step(self, step):

        # delete any thing in grid layout
        for i in range(self.gridLayout.rowCount()):
            for j in range(self.gridLayout.columnCount()):
                item = self.gridLayout.itemAtPosition(i, j)
                if item is not None:
                    widget = item.widget()
                    if widget is not None:
                        widget.setParent(None)

        # show the step
        for i in range(len(step)):
            for j in range(len(step[0])):
                self.element = QLabel()
                self.element.setAlignment(Qt.AlignCenter)
                self.element.setStyleSheet("""
						font-size: 25px;
						font-weight: bold;
					""")
                self.element.setText(f"{step[i][j]:0.2f}")
                self.gridLayout.addWidget(self.element, i, j)
                
    def show_solve(self):
        sols = []    
        if(self.start == len(self.steps) - 1):
            last_col_index = len(self.steps[self.start][0]) - 1
            for i in range(len(self.steps[self.start])):
                item = self.gridLayout.itemAtPosition(i,last_col_index)
                widget = item.widget()
                widget.setStyleSheet("""font-size:25px;font-weight:bold;background-color: green;color:#fff;""")
                sols.append(widget.text())
        
        
        text = ""       
        for index,i in enumerate(sols):
            if(index < len(sols)-1):
                var = f"x{index+1} = {i} | "
            else:
                var = f"x{index+1} = {i}"
            text += var
            
        self.solve_vector.setText(text)
        self.solve_vector.show()
            
    def show_next(self):
        self.last_step.setEnabled(True)
        if self.start < len(self.steps) - 1:
            self.start += 1
            
            self.show_op()
            self.show_step(self.steps[self.start])
            if(self.start == len(self.steps) - 1):
                self.next_step.setEnabled(False)
        self.show_solve()

    def show_last(self):
        self.next_step.setEnabled(True)
        if self.start > 0:
            self.start -= 1
            self.show_step(self.steps[self.start])
            self.show_op()
            self.solve_vector.hide()
            if(self.start == 0):
                self.last_step.setEnabled(False)                
    
    def show_first_step(self):
        self.next_step.setEnabled(True)
        self.start = 0
        self.show_step(self.steps[self.start])
        self.show_op()
        self.last_step.setEnabled(False)
        self.solve_vector.hide()
        
    def skip_all_steps(self):
        self.last_step.setEnabled(True)
        self.start = len(self.steps) - 1
        self.show_step(self.steps[self.start])
        self.show_op()
        self.show_solve()
        self.next_step.setEnabled(False)
        self.solve_vector.show()
        
class help_dialog(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        loadUi('AppUi/help.ui',self)        

class operations_dialog(QDialog):
    def __init__(self,op,parent=None):
        super().__init__(parent)
        loadUi('AppUi/opeartion_dialog.ui',self)
        self.operation = op 
        self.setWindowTitle(f"Operation - {op}") 
        self.generate_btn.clicked.connect(self.create_matrix_inputs)
    
    def create_matrix_inputs(self):
        inputs_number = int(self.mat_number.text())
        
        if(self.matrix_inputs.count() != 0):
            for i in range(self.matrix_inputs.count()):
                item = self.matrix_inputs.itemAt(i)
                widget = item.widget()
                widget.deleteLater()

        for i in range(inputs_number):
            self.matrixLine = QLineEdit()
            self.matrixLine.setPlaceholderText(f"mat {i+1}")
            self.matrix_inputs.addWidget(self.matrixLine)


def main():
    app = QApplication(sys.argv)
    main = Main_form()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
