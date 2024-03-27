from PyQt6.QtWidgets import QDialog, QProgressBar, QFileDialog, QLineEdit, QComboBox, QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QVBoxLayout, QWidget, QHBoxLayout

class DataframeTable(QTableWidget):
    def __init__(self, data_frame, loading_bar):
        super().__init__()

        if len(data_frame.index) > 1000:
            #if the file is too large, we switch to preview mode and reduce the number of shown rows
            num_rows = 1000
        else:
            #else we use normal mode
            num_rows = len(data_frame.index)

        num_cols = len(data_frame.columns)

        self.setColumnCount(num_cols)
        self.setRowCount(num_rows)
        self.setHorizontalHeaderLabels(data_frame.columns)

        if loading_bar is not None:
            for i in range(num_rows):
                loading_bar.setValue(100 * i / num_rows)
                QApplication.processEvents()
                for j in range(num_cols):
                    self.setItem(i, j, QTableWidgetItem(str(data_frame.iat[i, j])))
        else:
            self.setRowCount(num_rows)
            for i in range(num_rows):
                for j in range(num_cols):
                    self.setItem(i, j, QTableWidgetItem(str(data_frame.iat[i, j])))

        self.resizeColumnsToContents()