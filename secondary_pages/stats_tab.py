from PyQt6.QtWidgets import QFileDialog, QLineEdit, QComboBox, QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QVBoxLayout, QWidget, QHBoxLayout
import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT

class StatsTab(QWidget):
    def __init__(self, data_frame):
        super().__init__()
        tab = QVBoxLayout()

        self.data_frame = data_frame
        name_cols = list(self.data_frame.columns)
        index_float_cols = []
        cols_to_be_deleted = []

        for col in range(len(name_cols)):
            if not self.is_float(self.data_frame.iat[0, col]):
                cols_to_be_deleted.append(name_cols[col])

            else:
                index_float_cols.append(col)

        for col in cols_to_be_deleted:
            if col in name_cols:
                name_cols.remove(col)

        self.stats_widget = QTableWidget()

        self.stats_widget.setColumnCount(len(name_cols))
        self.stats_widget.setRowCount(2)
        self.stats_widget.setHorizontalHeaderLabels(name_cols)
        self.stats_widget.setVerticalHeaderLabels(["Mean", "Sd"])
        self.stats_widget.setMinimumHeight(85)

        for element in cols_to_be_deleted:
            self.data_frame = self.data_frame.drop(element, axis=1)


        self.calculate_statistics(index_float_cols, name_cols)

        fig, ax = plt.subplots(figsize=(100, 100))

        self.canvas = FigureCanvasQTAgg(fig)

        # Store heatmap object in a variable to easily access it when you want to include more features (such as title).
        # Set the range of values to be displayed on the colormap from -1 to 1, and set the annotation to True to display the correlation values on the heatmap.
        heatmap = sns.heatmap(self.data_frame.corr(), vmin=-1, vmax=1, annot=len(name_cols)<=15)
        # Give a title to the heatmap. Pad defines the distance of the title from the top of the heatmap.
        heatmap.set_title('Correlation Heatmap from stats', fontdict={'fontsize': 12}, pad=12)

        tab.addWidget(self.canvas)
        tab.addWidget(self.stats_widget)

        self.setLayout(tab)

    def calculate_statistics(self, index_cols, name_cols):
        number_of_cols = len(index_cols)
        means = []
        sd = []
        num_rows = len(self.data_frame.index)
        for i in range(len(name_cols)):
            #converts column into numpy array
            array = np.array(self.data_frame[name_cols[i]].values)

            #calculate mean and sd of the column
            means.append(self.data_frame[name_cols[i]].sum()/num_rows)
            sd.append(np.std(array))

            #add these values to the stats table
            self.stats_widget.setItem(0, i, QTableWidgetItem(str(round(means[i], 4))))
            self.stats_widget.setItem(1, i, QTableWidgetItem(str(round(sd[i], 4))))

    def is_float(self, input_str):
        try:
            float(input_str)
            return True  # Input is a valid float
        except ValueError:
            return False  # Input is not a valid float
