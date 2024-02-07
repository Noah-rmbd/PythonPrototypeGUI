from PyQt6.QtWidgets import QFileDialog, QLineEdit, QComboBox, QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QVBoxLayout, QWidget, QHBoxLayout

class StatsTab(QWidget):
    def __init__(self, data_frame):
        super().__init__()
        tab = QVBoxLayout()
        title = QLabel("Stats")

        self.data_frame = data_frame

        tab.addWidget(title)
        self.setLayout(tab)

    def mean(self, column):
        mean = 0
        sum = 0
        self.data_frame.iat[i, j]
