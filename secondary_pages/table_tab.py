from PyQt6.QtWidgets import QFileDialog, QLineEdit, QComboBox, QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QVBoxLayout, QWidget, QHBoxLayout


class TableTab(QWidget):
    def __init__(self, data_frame):
        super().__init__()

        content_layout = QVBoxLayout()
        window_layout = QHBoxLayout()

        self.data_frame = data_frame

        self.label = QLabel("File Table")
        self.table_widget = QTableWidget()

        self.Showdata()

        content_layout.addWidget(self.label)
        content_layout.addWidget(self.table_widget)

        window_layout.addLayout(content_layout)
        self.setLayout(window_layout)

    def Showdata(self):
        num_rows = len(self.data_frame.index)
        num_cols = len(self.data_frame.columns)
        self.table_widget.setColumnCount(num_cols)
        self.table_widget.setRowCount(num_rows)
        self.table_widget.setHorizontalHeaderLabels(self.data_frame.columns)

        for i in range(num_rows):
            for j in range(num_cols):
                self.table_widget.setItem(i,j, QTableWidgetItem(str(self.data_frame.iat[i,j])))

        self.table_widget.resizeColumnsToContents()
