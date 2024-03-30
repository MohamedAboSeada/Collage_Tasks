import sys
from PyQt5.QtCore import Qt, QAbstractTableModel, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog,QMessageBox, QFileDialog, QHBoxLayout, QVBoxLayout, QComboBox, QPushButton, QTableView
from PyQt5.uic import loadUi
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class DataFrameModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            else:
                return str(section + 1)  # Return row numbers for vertical headers

class ChooseDialog(QDialog):
    dataReturned = pyqtSignal(str)

    def __init__(self, col_labels):
        super().__init__()
        loadUi('ui/analysis.ui', self)
        self.col_labels = col_labels
        self.populateCombo()
        self.conf.clicked.connect(self.confirm)

    def populateCombo(self):
        for label in self.col_labels:
            self.cols_box.addItem(label)

    def confirm(self):
        data = self.cols_box.currentText()
        self.dataReturned.emit(data)
        self.close()

class PlotWin(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('ui/design.ui', self)
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.plot_grid.addWidget(self.canvas)
        
        # intilize axes
        self.ax = self.figure.add_subplot(111)
        self.ax.plot(1,1)
        self.canvas.draw()
        
        self.df = None
        
        self.open_file.clicked.connect(self.openFile)
        self.start_analysis.clicked.connect(self.choose_column)
        self.save_pl.clicked.connect(self.save_plot)
    
    def choose_column(self):
        self.ch = ChooseDialog(self.df.columns)
        self.ch.dataReturned.connect(self.analyse)
        self.ch.exec_()

    def analyse(self, col_label):
        class_number = 10
        col = self.df[col_label]
        try:
            classes = pd.cut(col, class_number)
            class_freq = classes.value_counts().sort_index()
            relative_freq = class_freq * 100 / col.count()
        except Exception:
            QMessageBox.warning(self, "Warning", "Work only with numeric values !", QMessageBox.Ok)
        else:
            self.populate_freq(class_freq, relative_freq.sort_index())    
            self.plot_freq(col_label)
            self.save_pl.setEnabled(True)

    def populate_freq(self, class_freq, relative_freq):
        data_frame = pd.DataFrame({'classes': class_freq.index, 'frequancy': class_freq.values, 'relative freq': relative_freq})
        model = DataFrameModel(data_frame)
        self.freq_dist.setModel(model)

    def openFile(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "Open CSV file", "", "CSV file (*.csv);;All Files (*)", options=options)
        if file:
            self.start_analysis.setEnabled(True)
            try:
                self.setWindowTitle(f"Probability Project - {file}")
                self.populate(file)
            except Exception as e:
                print(e)

    def populate(self, file_name):
        self.df = pd.read_csv(file_name)
        model = DataFrameModel(self.df)
        self.pre_data.setModel(model)

    def plot_freq(self,name):
        self.figure.clear()  # Clear the previous plot
        ax = self.figure.add_subplot(111)
        
        # Plot histogram
        ax.hist(self.df[name], bins=10,histtype="barstacked")  # Assuming 'age' is the column you want to plot
        
        # Set labels and title
        ax.set_xlabel(name)
        ax.set_ylabel('Frequency')
        
        # Draw the plot on the canvas
        self.canvas.draw()
        
    def save_plot(self):
        # save fig
        from random import randint
        try: 
            self.figure.savefig(f'images/plot{randint(10000,92137213)}.png')
        except Exception as e:
            print(e)
        else:
            QMessageBox.information(self,"info",f"image saved successfully!")

def main():
    app = QApplication(sys.argv)
    plotwin = PlotWin()
    plotwin.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
