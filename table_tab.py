from PyQt6.QtWidgets import QFileDialog, QLineEdit, QComboBox, QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtGui import QKeySequence
from PyQt6.QtCore import Qt
from sklearn import preprocessing
import numpy as np

class TableWindow(QWidget):
    def __init__(self, data_frame):
        super().__init__()

        content_layout = QVBoxLayout()
        menu_layout = QVBoxLayout()
        selected_col_layout = QVBoxLayout()
        add_col_layout = QVBoxLayout()
        modify_col_layout = QVBoxLayout()
        export_changes_layout = QVBoxLayout()
        window_layout = QHBoxLayout()

        self.data_frame = data_frame
        self.df_versions = []
        self.df_versions.append(self.data_frame.copy())
        self.df_index_current_version = 0

        self.label = QLabel("File Table")
        self.table_widget = QTableWidget()
        self.table_widget.cellChanged.connect(self.get_selected_item_position)
        self.Showdata()
        self.insert_after = QPushButton("Insert column before")

        text_selected_col = QLabel("Selected column")
        text_new_col = QLabel("New column name : ")
        text_selected_col.setMaximumHeight(20)
        text_new_col.setMaximumHeight(20)

        self.insert_name = QLineEdit()
        self.index = 0
        self.combobox = QComboBox()
        self.combobox.addItems(list(self.data_frame.columns.values))
        self.save_changes = QPushButton("Update graphs/tabs/..")
        self.save_button = QPushButton("Export to CSV")
        self.normalize_button = QPushButton("Normalize column")
        self.delete_button = QPushButton("Delete column")
        self.back_button = QPushButton("Back")

        self.back_button.setMaximumWidth(200)
        self.save_changes.setMaximumWidth(200)
        self.delete_button.setMaximumWidth(200)
        self.normalize_button.setMaximumWidth(200)
        self.insert_name.setMaximumWidth(200)
        self.insert_name.setPlaceholderText("Enter the name here")

        self.delete_button.clicked.connect(self.deleteColumn)
        self.normalize_button.clicked.connect(self.normalizeColumn)
        self.insert_after.clicked.connect(self.insertColumn)
        self.save_button.clicked.connect(self.saveToCsv)
        self.back_button.clicked.connect(self.change_df_version)

        content_layout.addWidget(self.label)
        content_layout.addWidget(self.table_widget)
        selected_col_layout.addWidget(text_selected_col)
        selected_col_layout.addWidget(self.combobox)
        add_col_layout.addWidget(text_new_col)
        add_col_layout.addWidget(self.insert_name)
        add_col_layout.addWidget(self.insert_after)
        modify_col_layout.addLayout(add_col_layout)
        modify_col_layout.addWidget(self.normalize_button)
        modify_col_layout.addWidget(self.delete_button)
        export_changes_layout.addWidget(self.back_button)
        export_changes_layout.addWidget(self.save_changes)
        export_changes_layout.addWidget(self.save_button)

        menu_layout.addLayout(selected_col_layout)
        menu_layout.addLayout(modify_col_layout)
        menu_layout.addLayout(export_changes_layout)

        window_layout.addLayout(content_layout)
        window_layout.addLayout(menu_layout)

        self.setLayout(window_layout)

        self.table_widget.cellChanged.connect(self.get_selected_item_position)

    def keyPressEvent(self, event):
        if event.key() == 16777238:
            self.undo_function()
        else:
            super().keyPressEvent(event)

    def undo_function(self):
        # Your undo function implementation

        self.change_df_version()

    def is_float(self, input_str):
        try:
            float(input_str)
            return True  # Input is a valid float
        except ValueError:
            return False  # Input is not a valid float
    def get_selected_item_position(self):
        selected_item = self.table_widget.currentItem()
        selected_column = self.table_widget.currentColumn()
        selected_row = self.table_widget.currentRow()
        if selected_item is not None:
            if (selected_column+1) != len(self.data_frame.columns) :
                if self.is_float(selected_item.text()):
                    self.data_frame.iat[selected_row,selected_column] = float(selected_item.text())
                    #print("Tout va bien")

                else:
                    print("This isn't digit")

            else:
                self.data_frame.iat[selected_row,selected_column] = str(selected_item.text())








    def changed_index(self):
        self.index = self.combobox.currentIndex()
        #print(self.index)

    def Showdata(self):
        #self.table_widget.cellChanged.disconnect(self.get_selected_item_position)
        num_rows = len(self.data_frame.index)
        num_cols = len(self.data_frame.columns)
        self.table_widget.setColumnCount(num_cols)
        self.table_widget.setRowCount(num_rows)
        self.table_widget.setHorizontalHeaderLabels(self.data_frame.columns)

        for i in range(num_rows):
            for j in range(num_cols):
                self.table_widget.setItem(i,j, QTableWidgetItem(str(self.data_frame.iat[i,j])))

        self.table_widget.resizeColumnsToContents()
        #self.table_widget.cellChanged.connect(self.get_selected_item_position)

    def deleteColumn(self):
        self.table_widget.cellChanged.disconnect(self.get_selected_item_position)
        col_to_delete = self.combobox.currentIndex()
        self.data_frame = self.data_frame.drop(self.data_frame.columns[col_to_delete], axis=1)
        self.combobox.removeItem(col_to_delete)
        self.Showdata()
        self.table_widget.cellChanged.connect(self.get_selected_item_position)

        self.df_versions.append(self.data_frame.copy())

    def saveToCsv(self):
        path = QFileDialog.getSaveFileName(self, 'Save File', '/Users/noah-r/Downloads/')[0]
        path = path+'.csv'
        self.data_frame.to_csv(path)

    def insertColumn(self):
        self.table_widget.cellChanged.disconnect(self.get_selected_item_position)
        col_to_insert = self.combobox.currentIndex()
        name = self.insert_name.text()
        if name not in self.data_frame.columns and name!='':
            self.label.setText("File Table")
            self.data_frame.insert(col_to_insert, name, list(range(150)), True)
            self.combobox.insertItem(col_to_insert, name)
            self.Showdata()
        else:
            self.label.setText("Please choose a different name")
        self.table_widget.cellChanged.connect(self.get_selected_item_position)

        self.df_versions.append(self.data_frame.copy())

    def normalizeColumn(self):
        index_col_to_normalize = self.combobox.currentIndex()
        col_name = self.data_frame.columns[index_col_to_normalize]
        if col_name != self.data_frame.columns[-1] :
            array = list(self.data_frame[col_name])  #preprocessing.normalize needs a double list

            min_val = min(array)
            max_val = max(array)

            # Normalize the data
            normalized_arr = [(x - min_val) / (max_val - min_val) for x in array]

            self.data_frame[col_name] = normalized_arr
            self.df_versions.append(self.data_frame.copy())
            self.Showdata()
        else:
            print("Can't normalize label columns")

    def change_df_version(self):
        if len(self.df_versions) > 1:
            self.df_versions.pop()
            self.data_frame = self.df_versions[-1].copy()
            self.Showdata()

        self.combobox.clear()
        self.combobox.addItems(list(self.data_frame.columns.values))

from PyQt6.QtWidgets import QFileDialog, QLineEdit, QComboBox, QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtGui import QKeySequence
from PyQt6.QtCore import Qt
from sklearn import preprocessing
import numpy as np

class TableWindow(QWidget):
    def __init__(self, data_frame):
        super().__init__()

        content_layout = QVBoxLayout()
        menu_layout = QVBoxLayout()
        selected_col_layout = QVBoxLayout()
        add_col_layout = QVBoxLayout()
        modify_col_layout = QVBoxLayout()
        export_changes_layout = QVBoxLayout()
        window_layout = QHBoxLayout()

        self.data_frame = data_frame
        self.df_versions = []
        self.df_versions.append(self.data_frame.copy())
        self.df_index_current_version = 0

        self.label = QLabel("File Table")
        self.table_widget = QTableWidget()
        self.table_widget.cellChanged.connect(self.get_selected_item_position)
        self.Showdata()
        self.insert_after = QPushButton("Insert column before")

        text_selected_col = QLabel("Selected column")
        text_new_col = QLabel("New column name : ")
        text_selected_col.setMaximumHeight(20)
        text_new_col.setMaximumHeight(20)

        self.insert_name = QLineEdit()
        self.index = 0
        self.combobox = QComboBox()
        self.combobox.addItems(list(self.data_frame.columns.values))
        self.save_changes = QPushButton("Update graphs/tabs/..")
        self.save_button = QPushButton("Export to CSV")
        self.normalize_button = QPushButton("Normalize column")
        self.delete_button = QPushButton("Delete column")
        self.back_button = QPushButton("Back")

        self.back_button.setMaximumWidth(200)
        self.save_changes.setMaximumWidth(200)
        self.delete_button.setMaximumWidth(200)
        self.normalize_button.setMaximumWidth(200)
        self.insert_name.setMaximumWidth(200)
        self.insert_name.setPlaceholderText("Enter the name here")

        self.delete_button.clicked.connect(self.deleteColumn)
        self.normalize_button.clicked.connect(self.normalizeColumn)
        self.insert_after.clicked.connect(self.insertColumn)
        self.save_button.clicked.connect(self.saveToCsv)
        self.back_button.clicked.connect(self.change_df_version)

        content_layout.addWidget(self.label)
        content_layout.addWidget(self.table_widget)
        selected_col_layout.addWidget(text_selected_col)
        selected_col_layout.addWidget(self.combobox)
        add_col_layout.addWidget(text_new_col)
        add_col_layout.addWidget(self.insert_name)
        add_col_layout.addWidget(self.insert_after)
        modify_col_layout.addLayout(add_col_layout)
        modify_col_layout.addWidget(self.normalize_button)
        modify_col_layout.addWidget(self.delete_button)
        export_changes_layout.addWidget(self.back_button)
        export_changes_layout.addWidget(self.save_changes)
        export_changes_layout.addWidget(self.save_button)

        menu_layout.addLayout(selected_col_layout)
        menu_layout.addLayout(modify_col_layout)
        menu_layout.addLayout(export_changes_layout)

        window_layout.addLayout(content_layout)
        window_layout.addLayout(menu_layout)

        self.setLayout(window_layout)

        self.table_widget.cellChanged.connect(self.get_selected_item_position)

    def keyPressEvent(self, event):
        if event.key() == 16777238:
            self.undo_function()
        else:
            super().keyPressEvent(event)

    def undo_function(self):
        # Your undo function implementation

        self.change_df_version()

    def is_float(self, input_str):
        try:
            float(input_str)
            return True  # Input is a valid float
        except ValueError:
            return False  # Input is not a valid float
    def get_selected_item_position(self):
        selected_item = self.table_widget.currentItem()
        selected_column = self.table_widget.currentColumn()
        selected_row = self.table_widget.currentRow()
        if selected_item is not None:
            if (selected_column+1) != len(self.data_frame.columns) :
                if self.is_float(selected_item.text()):
                    self.data_frame.iat[selected_row,selected_column] = float(selected_item.text())
                    #print("Tout va bien")

                else:
                    print("This isn't digit")

            else:
                self.data_frame.iat[selected_row,selected_column] = str(selected_item.text())








    def changed_index(self):
        self.index = self.combobox.currentIndex()
        #print(self.index)

    def Showdata(self):
        #self.table_widget.cellChanged.disconnect(self.get_selected_item_position)
        num_rows = len(self.data_frame.index)
        num_cols = len(self.data_frame.columns)
        self.table_widget.setColumnCount(num_cols)
        self.table_widget.setRowCount(num_rows)
        self.table_widget.setHorizontalHeaderLabels(self.data_frame.columns)

        for i in range(num_rows):
            for j in range(num_cols):
                self.table_widget.setItem(i,j, QTableWidgetItem(str(self.data_frame.iat[i,j])))

        self.table_widget.resizeColumnsToContents()
        #self.table_widget.cellChanged.connect(self.get_selected_item_position)

    def deleteColumn(self):
        self.table_widget.cellChanged.disconnect(self.get_selected_item_position)
        col_to_delete = self.combobox.currentIndex()
        self.data_frame = self.data_frame.drop(self.data_frame.columns[col_to_delete], axis=1)
        self.combobox.removeItem(col_to_delete)
        self.Showdata()
        self.table_widget.cellChanged.connect(self.get_selected_item_position)

        self.df_versions.append(self.data_frame.copy())

    def saveToCsv(self):
        path = QFileDialog.getSaveFileName(self, 'Save File', '/Users/noah-r/Downloads/')[0]
        path = path+'.csv'
        self.data_frame.to_csv(path)

    def insertColumn(self):
        self.table_widget.cellChanged.disconnect(self.get_selected_item_position)
        col_to_insert = self.combobox.currentIndex()
        name = self.insert_name.text()
        if name not in self.data_frame.columns and name!='':
            self.label.setText("File Table")
            self.data_frame.insert(col_to_insert, name, list(range(150)), True)
            self.combobox.insertItem(col_to_insert, name)
            self.Showdata()
        else:
            self.label.setText("Please choose a different name")
        self.table_widget.cellChanged.connect(self.get_selected_item_position)

        self.df_versions.append(self.data_frame.copy())

    def normalizeColumn(self):
        index_col_to_normalize = self.combobox.currentIndex()
        col_name = self.data_frame.columns[index_col_to_normalize]
        if col_name != self.data_frame.columns[-1] :
            array = list(self.data_frame[col_name])  #preprocessing.normalize needs a double list

            min_val = min(array)
            max_val = max(array)

            # Normalize the data
            normalized_arr = [(x - min_val) / (max_val - min_val) for x in array]

            self.data_frame[col_name] = normalized_arr
            self.df_versions.append(self.data_frame.copy())
            self.Showdata()
        else:
            print("Can't normalize label columns")

    def change_df_version(self):
        if len(self.df_versions) > 1:
            self.df_versions.pop()
            self.data_frame = self.df_versions[-1].copy()
            self.Showdata()

        self.combobox.clear()
        self.combobox.addItems(list(self.data_frame.columns.values))

