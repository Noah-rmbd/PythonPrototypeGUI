from PyQt6.QtWidgets import QApplication, QFileDialog, QLineEdit, QComboBox, QFrame,  QPushButton, QDialog, QTableWidget, QTableWidgetItem, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, Normalizer, MinMaxScaler
from components.dataframe_table import DataframeTable
import pandas as pd
import numpy as np

class DataModification(QWidget):
    def __init__(self, data_frame, normal_visualization, next_step_bar):
        super().__init__()

        self.data_frame = data_frame
        self.next_step_bar = next_step_bar

        self.content_layout = QVBoxLayout()
        menu_layout = QVBoxLayout()
        del_col_layout = QVBoxLayout()
        preprocessing_layout = QVBoxLayout()
        split_layout = QHBoxLayout()
        split_step_layout = QVBoxLayout()
        export_changes_layout = QVBoxLayout()
        window_layout = QHBoxLayout()


        menu_layout_container = QWidget()
        menu_layout_container.setLayout(menu_layout)
        menu_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        menu_layout.setSpacing(15)

        self.Showdata()

        content_layout_container = QWidget()
        content_layout_container.setLayout(self.content_layout)

        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.setSpacing(0)

        menu_layout.setContentsMargins(20, 20, 30, 0)
        self.content_layout.setContentsMargins(30, 20, 20, 10)

        menu_font = QFont('Helvetica', 13)
        menu_font.setBold(True)

        self.normal_visualization = normal_visualization
        self.data_frame_is_splited = False
        self.df_versions = []
        self.df_versions.append(self.data_frame.copy())
        self.df_index_current_version = 0

        self.label = QLabel("File Table")

        text_selected_col = QLabel("1 - Delete column")
        text_selected_col.setFont(menu_font)
        text_selected_col.setMaximumHeight(20)

        split_label = QLabel("2 - Split data")
        split_label.setFont(menu_font)
        split_label.setMaximumHeight(20)

        preprocessing_label = QLabel("3 - Transform data")
        preprocessing_label.setFont(menu_font)
        preprocessing_label.setMaximumHeight(20)

        self.insert_name = QLineEdit()
        self.index = 0
        self.combobox = QComboBox()
        self.combobox.addItems(list(self.data_frame.columns.values))
        self.save_button = QPushButton("Export to CSV")
        self.normalize_button = QPushButton("Normalize column")
        self.standardize_button = QPushButton("Standardize column")
        self.delete_button = QPushButton("Delete column")
        self.back_button = QPushButton("Back")
        self.split_button = QPushButton("Split data")
        self.split_combo = QComboBox()

        self.split_button.setToolTip("Split data in two parts, one for training, the other for testing")
        self.split_combo.setToolTip("Select the percentage of data used for testing")

        self.split_combo.addItem("20 %")
        self.split_combo.addItem("30 %")
        self.split_combo.addItem("40 %")
        self.split_combo.addItem("50 %")

        self.combobox.setMaximumWidth(200)
        self.back_button.setMaximumWidth(200)
        self.save_button.setMaximumWidth(200)
        self.delete_button.setMaximumWidth(200)
        self.normalize_button.setMaximumWidth(200)
        self.standardize_button.setMaximumWidth(200)
        self.insert_name.setMaximumWidth(200)
        self.insert_name.setPlaceholderText("Enter the name here")

        self.delete_button.clicked.connect(self.deleteColumn)
        self.normalize_button.clicked.connect(self.normalizeColumn)
        self.standardize_button.clicked.connect(self.standardizeColumn)
        self.save_button.clicked.connect(self.saveToCsv)
        self.back_button.clicked.connect(self.change_df_version)
        self.split_button.clicked.connect(self.split_data)

        del_col_layout.addWidget(text_selected_col)
        del_col_layout.addWidget(self.combobox)
        del_col_layout.addWidget(self.delete_button)
        del_col_layout.setSpacing(10)


        split_step_layout.addWidget(split_label)
        split_step_layout.addLayout(split_layout)
        split_step_layout.setSpacing(10)
        split_layout.setContentsMargins(0, 0, 0, 0)
        split_layout.addWidget(self.split_button)
        split_layout.addWidget(self.split_combo)

        preprocessing_layout.addWidget(preprocessing_label)
        preprocessing_layout.addWidget(self.normalize_button)
        preprocessing_layout.addWidget(self.standardize_button)
        preprocessing_layout.setSpacing(10)

        export_changes_layout.addWidget(self.back_button)
        export_changes_layout.addWidget(self.save_button)
        export_changes_layout.setSpacing(10)

        self.normalize_button.setEnabled(False)
        self.standardize_button.setEnabled(False)
        self.back_button.setEnabled(False)

        menu_layout.addLayout(del_col_layout)
        menu_layout.addWidget(QFrame(frameShape=QFrame.Shape.HLine))
        menu_layout.addLayout(split_step_layout)
        menu_layout.addWidget(QFrame(frameShape=QFrame.Shape.HLine))
        menu_layout.addLayout(preprocessing_layout)
        menu_layout.addWidget(QFrame(frameShape=QFrame.Shape.HLine))
        menu_layout.addLayout(export_changes_layout)

        window_layout.addWidget(content_layout_container)
        window_layout.addWidget(QFrame(frameShape=QFrame.Shape.VLine))
        window_layout.addWidget(menu_layout_container)

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
        self.table_widget.setStyleSheet(" ")
        self.content_layout.addWidget(self.table_widget)
        self.next_step_bar.hide_loading()

    def Showdata_splited(self, df_training, df_testing):
        menu_font = QFont('Helvetica', 13)
        menu_font.setBold(True)
        for i in reversed(range(self.content_layout.count())):
            self.content_layout.itemAt(i).widget().setParent(None)

        table_1_label = QLabel("Training data")
        table_2_label = QLabel("Testing data")

        table_1_label.setFont(menu_font)
        table_2_label.setFont(menu_font)

        self.next_step_bar.show_loading("Training data preview")
        table_1 = DataframeTable(df_training, self.next_step_bar.loading_bar)
        self.next_step_bar.hide_loading()

        self.next_step_bar.show_loading("Testing data preview")
        table_2 = DataframeTable(df_testing, self.next_step_bar.loading_bar)
        self.next_step_bar.hide_loading()

        self.content_layout.addWidget(table_1_label)
        self.content_layout.addWidget(table_1)
        self.content_layout.addWidget(QFrame(frameShape=QFrame.Shape.HLine))
        self.content_layout.addWidget(table_2_label)
        self.content_layout.addWidget(table_2)

    def split_data(self):
        self.next_step_bar.show_status("Splitting data ...")

        #select the label column in a dialog window
        label_dialog = LabelDialog(self.data_frame.columns)
        result = label_dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            #create the label_index variable that will be used in data_analysis_tab
            self.label_col_name = label_dialog.label_combo_box.currentText()#self.data_frame.columns[-self.label_col_index]
            self.label_col_index = list(self.data_frame.columns).index(self.label_col_name)  # label_dialog.label_combo_box.currentIndex()
            print(self.label_col_index, self.label_col_name)

            #get the size of the testing_dataframe
            test_size = float(self.split_combo.currentText()[:2]) / 100

            #create a numpy array that contains the label column
            label_array = self.data_frame[self.label_col_name].values

            #create a numpy array that contains other columns of the df
            data_without_label = self.data_frame.to_numpy()
            data_without_label = np.delete(data_without_label, self.label_col_index, axis=1)

            #split data in four numpy arrays (train or test)*(content or label)
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(data_without_label, label_array, test_size=test_size,
                                                                random_state=42)

            self.splited_mode() #disable other buttons and enable standardization and normalization buttons
            self.back_button.setEnabled(True)

            #create two numpy arrays that contains the training or testing dataframe, add to X values the label column at "label_index+1" position
            training_numpy = np.insert(self.X_train, self.label_col_index, self.y_train, axis=1)
            testing_numpy = np.insert(self.X_test, self.label_col_index, self.y_test, axis=1)

            #convert the two numpy arrays in pandas dataframe
            df_training = pd.DataFrame(training_numpy, columns=self.data_frame.columns)
            df_testing = pd.DataFrame(testing_numpy, columns=self.data_frame.columns)

            self.Showdata_splited(df_training, df_testing) #show the two dataframes
        self.next_step_bar.hide_status()  # hide the working status alert

    def deleteColumn(self):
        col_to_delete = self.combobox.currentIndex()
        self.data_frame = self.data_frame.drop(self.data_frame.columns[col_to_delete], axis=1)
        self.table_widget.removeColumn(col_to_delete)

        self.combobox.removeItem(col_to_delete)

        self.df_versions.append(self.data_frame.copy())
        self.back_button.setEnabled(True)

    def saveToCsv(self):
        path = QFileDialog.getSaveFileName(self, 'Save File', '/Users/noah-r/Downloads/')[0]
        path = path+'.csv'
        self.data_frame.to_csv(path)

    def normalizeColumn(self):
        self.df_scaler(MinMaxScaler())

    def standardizeColumn(self):
        self.df_scaler(StandardScaler())

    def df_scaler(self, scaler):
        col_names = list(self.data_frame.columns)
        col_names.remove(self.label_col_name)

        self.next_step_bar.show_loading("Standardizing columns : ")

        for i in col_names:
            # transforme la colonne i du df en un array numpy de format (-1, 1)
            array = list(self.data_frame[i])
            array = np.asarray(array)
            array = array.reshape(-1, 1)

            # transforme la colonne i des données d'entrainnement du df en un array numpy de format (-1, 1)
            index_column_X = col_names.index(i)  # get the index of the column in the X arrays
            self.next_step_bar.loading_bar.setValue(int(100 * (index_column_X + 1) / len(col_names)))
            QApplication.processEvents()

            train_column = self.X_train[:, index_column_X]  # get a numpy array of X training values
            train_column = train_column.reshape(-1, 1)

            test_column = self.X_test[:, index_column_X]  # get a numpy array of X testing values
            test_column = test_column.reshape(-1, 1)

            # create Sklearn scaler that uses standardization
            scaler = scaler

            scaler.fit(train_column)

            standardized_arr = scaler.transform(array)  # standardize the entire column of the df
            standardized_train = scaler.transform(train_column)  # standardize training values of the column
            standardized_test = scaler.transform(test_column)  # standardize testing values of the column

            standardized_train = standardized_train.reshape(
                -1, )  # reshape these values so that they can fit in X_train
            standardized_test = standardized_test.reshape(-1, )  # reshape these values so that they can fit in X_test

            # replace the original values by the standardized ones
            self.data_frame[i] = standardized_arr
            self.X_train[:, index_column_X] = standardized_train
            self.X_test[:, index_column_X] = standardized_test

        # save the new version of the df
        self.df_versions.append(self.data_frame.copy())

        training_numpy = np.insert(self.X_train, self.label_col_index, self.y_train, axis=1)
        testing_numpy = np.insert(self.X_test, self.label_col_index, self.y_test, axis=1)

        # convert the two numpy arrays in pandas dataframe
        df_training = pd.DataFrame(training_numpy, columns=self.data_frame.columns)
        df_testing = pd.DataFrame(testing_numpy, columns=self.data_frame.columns)

        # disable the normalization and standardization buttons
        self.normalize_button.setEnabled(False)
        self.standardize_button.setEnabled(False)

        self.next_step_bar.hide_loading()
        # updates the table preview
        self.Showdata_splited(df_training, df_testing)


    def change_df_version(self):
        print("Retour, voici valeur de data is splited : ",self.data_frame_is_splited)
        if self.data_frame_is_splited:
            self.unsplited_mode()
            self.Showdata()

            if len(self.df_versions) == 1:
                self.back_button.setEnabled(False)

        if len(self.df_versions) > 1:
            self.df_versions.pop()
            self.data_frame = self.df_versions[-1].copy()
            self.Showdata()
            print("Retour",self.data_frame)

            if len(self.df_versions) == 1:
                self.back_button.setEnabled(False)

        self.combobox.clear()
        self.combobox.addItems(list(self.data_frame.columns.values))

    def splited_mode(self):
        self.normalize_button.setEnabled(True)
        self.standardize_button.setEnabled(True)
        self.delete_button.setEnabled(False)
        self.insert_name.setEnabled(False)
        self.combobox.setEnabled(False)
        self.split_combo.setEnabled(False)
        self.split_button.setEnabled(False)
        self.normalize_button.setEnabled(True)
        self.standardize_button.setEnabled(True)

        self.data_frame_is_splited = True

    def unsplited_mode(self):
        self.normalize_button.setEnabled(False)
        self.standardize_button.setEnabled(False)
        self.delete_button.setEnabled(True)
        self.insert_name.setEnabled(True)
        self.combobox.setEnabled(True)
        self.split_combo.setEnabled(True)
        self.split_button.setEnabled(True)

        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None
        self.data_frame_is_splited = False

class LabelDialog(QDialog):
    def __init__(self, list_columns):
        super().__init__()

        texte = QLabel("Selectionnez la colonne à prédire :")

        # Créer une QComboBox
        self.label_combo_box = QComboBox()
        print(list_columns)
        list_columns = list(list_columns)
        list_columns.reverse()
        print(list_columns)
        self.label_combo_box.addItems(list_columns)

        # Créer un bouton "OK"
        self.button = QPushButton('OK')
        self.button.clicked.connect(self.accept)

        # Créer un layout vertical et ajouter la QComboBox et le bouton
        layout = QVBoxLayout()
        layout.addWidget(texte)
        layout.addWidget(self.label_combo_box)
        layout.addWidget(self.button)
        self.setLayout(layout)
