from PyQt6.QtWidgets import QFileDialog, QLineEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from sklearn.model_selection import train_test_split
from components.dataframe_table import DataframeTable
import pandas as pd
import numpy as np

class DataModification(QWidget):
    def __init__(self, data_frame, normal_visualization, next_step_bar):
        super().__init__()

        self.content_layout = QVBoxLayout()
        menu_layout = QVBoxLayout()
        selected_col_layout = QVBoxLayout()
        add_col_layout = QVBoxLayout()
        modify_col_layout = QVBoxLayout()
        split_layout = QHBoxLayout()
        export_changes_layout = QVBoxLayout()
        window_layout = QHBoxLayout()

        self.data_frame = data_frame
        self.next_step_bar = next_step_bar
        self.normal_visualization = normal_visualization
        self.data_frame_is_splited = False
        self.df_versions = []
        self.df_versions.append(self.data_frame.copy())
        self.df_index_current_version = 0

        self.label = QLabel("File Table")
        #self.table_widget.cellChanged.connect(self.get_selected_item_position)
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
        self.standardize_button = QPushButton("Standardize column")
        self.delete_button = QPushButton("Delete column")
        self.back_button = QPushButton("Back")
        self.split_button = QPushButton("Split data")
        self.split_combo = QComboBox()

        self.split_combo.addItem("20 %")
        self.split_combo.addItem("30 %")
        self.split_combo.addItem("40 %")
        self.split_combo.addItem("50 %")

        self.combobox.setMaximumWidth(200)
        self.back_button.setMaximumWidth(200)
        self.save_changes.setMaximumWidth(200)
        self.save_button.setMaximumWidth(200)
        self.delete_button.setMaximumWidth(200)
        self.normalize_button.setMaximumWidth(200)
        self.standardize_button.setMaximumWidth(200)
        self.insert_name.setMaximumWidth(200)
        self.insert_name.setPlaceholderText("Enter the name here")

        self.delete_button.clicked.connect(self.deleteColumn)
        self.normalize_button.clicked.connect(self.normalizeColumn)
        self.standardize_button.clicked.connect(self.standardizeColumn)
        self.insert_after.clicked.connect(self.insertColumn)
        self.save_button.clicked.connect(self.saveToCsv)
        self.back_button.clicked.connect(self.change_df_version)
        self.split_button.clicked.connect(self.split_data)

        #self.content_layout.addWidget(self.label)
        #self.content_layout.addWidget(self.table_widget)
        selected_col_layout.addWidget(text_selected_col)
        selected_col_layout.addWidget(self.combobox)
        add_col_layout.addWidget(text_new_col)
        add_col_layout.addWidget(self.insert_name)
        add_col_layout.addWidget(self.insert_after)
        add_col_layout.addWidget(self.delete_button)
        modify_col_layout.addLayout(split_layout)
        split_layout.addWidget(self.split_button)
        split_layout.addWidget(self.split_combo)
        modify_col_layout.addWidget(self.normalize_button)
        modify_col_layout.addWidget(self.standardize_button)
        export_changes_layout.addWidget(self.back_button)
        export_changes_layout.addWidget(self.save_changes)
        export_changes_layout.addWidget(self.save_button)

        self.normalize_button.setEnabled(False)
        self.standardize_button.setEnabled(False)

        menu_layout.addLayout(selected_col_layout)
        menu_layout.addLayout(add_col_layout)
        menu_layout.addLayout(modify_col_layout)
        menu_layout.addLayout(export_changes_layout)

        window_layout.addLayout(self.content_layout)
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

                else:
                    print("This isn't digit")

            else:
                self.data_frame.iat[selected_row,selected_column] = str(selected_item.text())

    def changed_index(self):
        self.index = self.combobox.currentIndex()

    def Showdata(self):
        for i in reversed(range(self.content_layout.count())):
            self.content_layout.itemAt(i).widget().setParent(None)

        self.next_step_bar.show_loading("Refreshing table preview")
        self.table_widget = DataframeTable(self.data_frame, self.next_step_bar.loading_bar)
        self.content_layout.addWidget(self.table_widget)
        self.next_step_bar.hide_loading()

    def Showdata_splited(self, df_training, df_testing):
        for i in reversed(range(self.content_layout.count())):
            self.content_layout.itemAt(i).widget().setParent(None)

        table_1_label = QLabel("Training data")
        table_2_label = QLabel("Testing data")

        self.next_step_bar.show_loading("Training data preview")
        table_1 = DataframeTable(df_training, self.next_step_bar.loading_bar)
        self.next_step_bar.hide_loading()

        self.next_step_bar.show_loading("Testing data preview")
        table_2 = DataframeTable(df_testing, self.next_step_bar.loading_bar)
        self.next_step_bar.hide_loading()

        self.content_layout.addWidget(table_1_label)
        self.content_layout.addWidget(table_1)
        self.content_layout.addWidget(table_2_label)
        self.content_layout.addWidget(table_2)

    def split_data(self):
        self.next_step_bar.show_status("Splitting data ...")
        test_size = float(self.split_combo.currentText()[:2]) / 100
        label = []
        nrow = len(self.data_frame.index)

        for i in range(nrow):
            label.append(
                self.data_frame.iat[i, -1])  # -1 permet d'aller dans la denière colonne (où se trouve les labels)

        label_array = np.array(label)  # Numpy array that contains labels

        data = self.data_frame.to_numpy()
        data_without_label = data[:, :-1]  # Numpy array that contains data frame values without label

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(data_without_label, label_array, test_size=test_size,
                                                            random_state=42)

        self.splited_mode()
        self.split_button.setEnabled(False)

        training_numpy = np.insert(self.X_train, 4, self.y_train, axis=1)
        testing_numpy = np.insert(self.X_test, 4, self.y_test, axis=1)
        df_training = pd.DataFrame(training_numpy, columns=self.data_frame.columns)
        df_testing = pd.DataFrame(testing_numpy, columns=self.data_frame.columns)

        self.next_step_bar.hide_status()
        self.Showdata_splited(df_training, df_testing)

    def deleteColumn(self):
        #self.table_widget.cellChanged.disconnect(self.get_selected_item_position, table_widget)
        col_to_delete = self.combobox.currentIndex()
        self.data_frame = self.data_frame.drop(self.data_frame.columns[col_to_delete], axis=1)
        self.table_widget.removeColumn(col_to_delete)
        print(col_to_delete)
        self.combobox.removeItem(col_to_delete)
        #self.Showdata()
        #self.table_widget.cellChanged.connect(self.get_selected_item_position)

        self.df_versions.append(self.data_frame.copy())
        print(self.data_frame)

    def saveToCsv(self):
        path = QFileDialog.getSaveFileName(self, 'Save File', '/Users/noah-r/Downloads/')[0]
        path = path+'.csv'
        self.data_frame.to_csv(path)

    def insertColumn(self):
        #self.table_widget.cellChanged.disconnect(self.get_selected_item_position)
        col_to_insert = self.combobox.currentIndex()
        name = self.insert_name.text()
        if name not in self.data_frame.columns and name!='':
            self.label.setText("File Table")
            self.data_frame.insert(col_to_insert, name, list(range(150)), True)
            self.combobox.insertItem(col_to_insert, name)
            self.Showdata()
        else:
            self.label.setText("Please choose a different name")
        #self.table_widget.cellChanged.connect(self.get_selected_item_position)

        self.df_versions.append(self.data_frame.copy())

    def normalizeColumn(self):
        col_names = self.data_frame.columns[:-1]

        for i in col_names:
            array = list(self.data_frame[i])
            index_column = list(self.data_frame.columns).index(i)
            train_column = self.X_train[:, index_column]
            list_train = train_column.tolist()

            min_val = min(list_train)
            max_val = max(list_train)

            # Normalize the data
            normalized_arr = [(x - min_val) / (max_val - min_val) for x in array]

            self.data_frame[i] = normalized_arr
        self.df_versions.append(self.data_frame.copy())
        self.split_data()

        self.normalize_button.setEnabled(False)
        self.standardize_button.setEnabled(False)
        self.Showdata()

    def mean(self, column):
        sum = 0
        num_rows = len(column)
        for i in column:
            sum += float(i)
        mean = sum/num_rows
        return mean

    def sd(self, column):
        mean = self.mean(column)
        num_rows = len(column)
        sum = 0
        for i in column:
            sum += abs(float(i-mean))
        sd = sum/num_rows
        sd = pow(sd, 1/2)
        return sd

    def standardizeColumn(self):
        col_names = self.data_frame.columns[:-1]
        print(self.data_frame)
        for i in col_names:
            array = list(self.data_frame[i])

            index_column = list(self.data_frame.columns).index(i)
            train_column = self.X_train[:, index_column]
            array_train = train_column.tolist()
            print(array, array_train, "index", index_column)

            mean = self.mean(array_train)
            std_dev = self.sd(array_train)

            standardized_arr = [(x - mean) / std_dev for x in array]

            self.data_frame[i] = standardized_arr

        self.df_versions.append(self.data_frame.copy())
        self.split_data()
        self.normalize_button.setEnabled(False)
        self.standardize_button.setEnabled(False)
        self.Showdata()


    def change_df_version(self):
        print("Retour, voici valeur de data is splited : ",self.data_frame_is_splited)
        if self.data_frame_is_splited:
            self.unsplited_mode()
            self.Showdata()

        if len(self.df_versions) > 1:
            self.df_versions.pop()
            self.data_frame = self.df_versions[-1].copy()
            self.Showdata()
            print("Retour",self.data_frame)

        self.combobox.clear()
        self.combobox.addItems(list(self.data_frame.columns.values))

    def splited_mode(self):
        self.normalize_button.setEnabled(True)
        self.standardize_button.setEnabled(True)
        self.insert_after.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.insert_name.setEnabled(False)
        self.combobox.setEnabled(False)
        self.split_combo.setEnabled(False)
        self.save_changes.setEnabled(False)
        self.normalize_button.setEnabled(True)
        self.standardize_button.setEnabled(True)

        self.data_frame_is_splited = True

    def unsplited_mode(self):
        self.normalize_button.setEnabled(False)
        self.standardize_button.setEnabled(False)
        self.insert_after.setEnabled(True)
        self.delete_button.setEnabled(True)
        self.insert_name.setEnabled(True)
        self.combobox.setEnabled(True)
        self.split_combo.setEnabled(True)
        self.save_changes.setEnabled(True)
        self.split_button.setEnabled(True)

        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None
        self.data_frame_is_splited = False
