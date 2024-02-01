from PyQt6.QtWidgets import QLineEdit, QComboBox, QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QVBoxLayout, QWidget, QHBoxLayout

import sys
import pandas as pd

class TableWindow(QWidget):
    def __init__(self, file_url):
        super().__init__()
        self.setWindowTitle("Tableur de : "+file_url)
        self.setMinimumSize(540,360)

        content_layout = QVBoxLayout()
        menu_layout = QVBoxLayout()
        window_layout = QHBoxLayout()
        self.data_frame = pd.read_csv(file_url)

        self.label = QLabel("Another Window")
        self.table_widget = QTableWidget()
        self.Showdata()
        self.nbr_edit = QLineEdit()
        self.nbr_edit.setMaximumWidth(100)
        self.index=0
        self.combobox = QComboBox()
        self.combobox.addItems(list(self.data_frame.columns.values))
        #self.combobox.currentIndexChanged(self.changed_index)
        self.delete_button = QPushButton("Delete")
        self.delete_button.setMaximumWidth(100)
        self.delete_button.clicked.connect(self.deleteColumn)

        content_layout.addWidget(self.label)
        content_layout.addWidget(self.table_widget)
        menu_layout.addWidget(self.combobox)
        menu_layout.addWidget(self.nbr_edit)
        menu_layout.addWidget(self.delete_button)

        window_layout.addLayout(content_layout)
        window_layout.addLayout(menu_layout)

        self.setLayout(window_layout)

    def changed_index(self):
        self.index = self.combobox.currentIndex()
        print(self.index)
    def Showdata(self):
        num_rows = len(self.data_frame.index)
        num_cols = len(self.data_frame.columns)
        self.table_widget.setColumnCount(num_cols)
        self.table_widget.setRowCount(num_rows)
        self.table_widget.setHorizontalHeaderLabels(self.data_frame.columns)

        for i in range(num_rows):
            for j in range(num_cols):
                self.table_widget.setItem(i,j, QTableWidgetItem(str(self.data_frame.iat[i,j])))

        #self.table_widget.removeRow(0)
        #self.table_widget.removeColumn(0)
        self.table_widget.resizeColumnsToContents()

        #print(list(self.data_frame.columns.values))

    def deleteColumn(self):
        col_to_delete = self.combobox.currentIndex()
        self.table_widget.removeColumn(col_to_delete)
        self.combobox.removeItem(col_to_delete)