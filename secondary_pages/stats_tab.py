from PyQt6.QtWidgets import QFileDialog, QLineEdit, QComboBox, QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QVBoxLayout, QWidget, QHBoxLayout
import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT

class StatsTab(QWidget):
    def __init__(self, data_frame):
        super().__init__()
        tab = QVBoxLayout()
        title = QLabel("Stats")

        self.data_frame = data_frame
        name_cols = list(self.data_frame.columns)
        index_cols = [i for i in range(len(name_cols))]
        cols_to_be_deleted = []

        for col in index_cols:
            if not self.is_float(self.data_frame.iat[0, col]):
                cols_to_be_deleted.append(name_cols[col])
                index_cols.remove(col)

        for col in cols_to_be_deleted:
            if col in name_cols:
                name_cols.remove(col)



        self.stats_widget = QTableWidget()

        self.stats_widget.setColumnCount(len(name_cols))
        self.stats_widget.setRowCount(2)
        self.stats_widget.setHorizontalHeaderLabels(name_cols)
        self.stats_widget.setVerticalHeaderLabels(["Mean", "Sd"])
        #print(self.data_frame.columns)

        for j in index_cols:
            self.stats_widget.setItem(0, j, QTableWidgetItem(str(round(self.mean(j),4))))
            self.stats_widget.setItem(1, j, QTableWidgetItem(str(round(self.sd(j), 4))))
            #print(self.mean(j))
        #print(self.data_frame.iat[0,1])

        tab.addWidget(title)
        tab.addWidget(self.stats_widget)
        self.setLayout(tab)

        fig, ax = plt.subplots(figsize=(16, 6))

        self.canvas = FigureCanvasQTAgg(fig)

        self.data_frame = self.data_frame.drop(self.data_frame.columns[-1], axis=1)
        # Store heatmap object in a variable to easily access it when you want to include more features (such as title).
        # Set the range of values to be displayed on the colormap from -1 to 1, and set the annotation to True to display the correlation values on the heatmap.
        heatmap = sns.heatmap(self.data_frame.corr(), vmin=-1, vmax=1, annot=True)
        # Give a title to the heatmap. Pad defines the distance of the title from the top of the heatmap.
        heatmap.set_title('Correlation Heatmap from stats', fontdict={'fontsize': 12}, pad=12)

        tab.addWidget(self.canvas)


    def mean(self, column):
        sum = 0
        num_rows = len(self.data_frame.index)
        for i in range(num_rows):
            sum += float(self.data_frame.iat[i, column])

        mean = sum/num_rows
        return mean

    def sd(self, column):
        mean = self.mean(column)
        num_rows = len(self.data_frame.index)
        sum = 0
        for i in range(num_rows):
            sum += abs(float(self.data_frame.iat[i, column])-mean)
        sd = sum/num_rows
        sd = pow(sd, 1/2)
        return sd

    def is_float(self, input_str):
        try:
            float(input_str)
            return True  # Input is a valid float
        except ValueError:
            return False  # Input is not a valid float
