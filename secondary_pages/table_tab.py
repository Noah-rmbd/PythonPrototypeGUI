from PyQt6.QtWidgets import QDialog, QProgressBar, QFileDialog, QLineEdit, QComboBox, QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from components.dataframe_table import DataframeTable

class TableTab(QWidget):
    def __init__(self, data_frame, loading_bar):
        super().__init__()
        self.loading_bar = loading_bar

        content_layout = QVBoxLayout()
        window_layout = QHBoxLayout()

        self.data_frame = data_frame

        self.label = QLabel("File Table")
        self.table_widget = DataframeTable(self.data_frame, self.loading_bar)

        content_layout.addWidget(self.label)
        content_layout.addWidget(self.table_widget)

        window_layout.addLayout(content_layout)
        self.setLayout(window_layout)
