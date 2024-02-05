from PyQt6.QtWidgets import QFileDialog, QLineEdit, QComboBox, QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from graphiques import FenGraph
import sys
import pandas as pd


class TableWindow(QWidget):
    def __init__(self, data_frame):
        super().__init__()
        #self.setWindowTitle("Tableur de : "+file_url)
        #self.setMinimumSize(540,360)
        #self.graph = FenGraph(file_url)
        #self.graph.show()

        content_layout = QVBoxLayout()
        menu_layout = QVBoxLayout()
        window_layout = QHBoxLayout()

        self.data_frame = data_frame

        self.label = QLabel("File Table")
        self.table_widget = QTableWidget()
        self.Showdata()
        self.insert_after = QPushButton("Insert column after")
        self.insert_name = QLineEdit()
        self.index=0
        self.combobox = QComboBox()
        self.combobox.addItems(list(self.data_frame.columns.values))
        self.save_button = QPushButton("Export to CSV")
        self.delete_button = QPushButton("Delete column")
        self.delete_button.setMaximumWidth(200)
        self.insert_name.setMaximumWidth(200)
        self.delete_button.clicked.connect(self.deleteColumn)
        self.insert_after.clicked.connect(self.insertColumn)
        self.save_button.clicked.connect(self.saveToCsv)

        content_layout.addWidget(self.label)
        content_layout.addWidget(self.table_widget)
        menu_layout.addWidget(self.combobox)
        menu_layout.addWidget(self.insert_after)
        menu_layout.addWidget(self.insert_name)
        menu_layout.addWidget(self.delete_button)
        menu_layout.addWidget(self.save_button)

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

        self.table_widget.resizeColumnsToContents()

    def deleteColumn(self):
        col_to_delete = self.combobox.currentIndex()
        self.data_frame = self.data_frame.drop(self.data_frame.columns[col_to_delete], axis=1)
        self.combobox.removeItem(col_to_delete)
        self.Showdata()

    def saveToCsv(self):
        path = QFileDialog.getSaveFileName(self, 'Save File', '/Users/noah-r/Downloads/')[0]
        path = path+'.csv'
        self.data_frame.to_csv(path)

    def insertColumn(self):
        col_to_insert = self.combobox.currentIndex()+1
        name = self.insert_name.text()
        if name not in self.data_frame.columns:
            self.label.setText("File Table")
            self.data_frame.insert(col_to_insert, name, list(range(150)), True)
            self.combobox.insertItem(col_to_insert, name)
            self.Showdata()
        else:
            self.label.setText("Please choose a different name")
