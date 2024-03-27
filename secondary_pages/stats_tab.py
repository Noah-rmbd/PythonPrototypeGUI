from PyQt6.QtWidgets import QFileDialog, QLineEdit, QComboBox, QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QVBoxLayout, QWidget, QHBoxLayout
import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT

class StatsTab(QWidget):
    def __init__(self, data_frame, normal_visualization):
        print("Voici le bool light_mode des statistiques", normal_visualization)
        super().__init__()
        tab = QVBoxLayout()
        title = QLabel("Stats")

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

        if normal_visualization:
            # statistics aren't calculated with light mode
            self.calculate_statistics(index_float_cols)

        fig, ax = plt.subplots(figsize=(100, 100))

        self.canvas = FigureCanvasQTAgg(fig)

        # Store heatmap object in a variable to easily access it when you want to include more features (such as title).
        # Set the range of values to be displayed on the colormap from -1 to 1, and set the annotation to True to display the correlation values on the heatmap.
        heatmap = sns.heatmap(self.data_frame.corr(), vmin=-1, vmax=1, annot=normal_visualization)
        # Give a title to the heatmap. Pad defines the distance of the title from the top of the heatmap.
        heatmap.set_title('Correlation Heatmap from stats', fontdict={'fontsize': 12}, pad=12)

        tab.addWidget(self.canvas)

        if normal_visualization:
            #statistics aren't calculated with light mode
            tab.addWidget(self.stats_widget)

        self.setLayout(tab)

    def calculate_statistics(self, index_cols):
        number_of_cols = len(index_cols)
        means = []
        sd = []
        print(index_cols)
        for i in range(number_of_cols):
            #print("Calculate the mean of", list(self.data_frame.columns)[index_cols[i]], " : ", 2*i+1, "/", 2*number_of_cols)
            means.append(self.mean(index_cols[i]))
            #print("Calculate the sd of", list(self.data_frame.columns)[index_cols[i]], " : ", 2*i+2, "/", 2*number_of_cols)
            sd.append(self.sd(index_cols[i], means[i]))
            self.stats_widget.setItem(0, i, QTableWidgetItem(str(round(means[i], 4))))
            self.stats_widget.setItem(1, i, QTableWidgetItem(str(round(sd[i], 4))))

    def mean(self, column):
        sum = 0
        num_rows = len(self.data_frame.index)

        for i in range(0, num_rows):
            #print(i)
            sum += float(self.data_frame.iat[i, column])

        mean = sum/num_rows
        return mean

    def sd(self, column, mean):
        num_rows = len(self.data_frame.index)
        sum = 0
        for i in range(0, num_rows):
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
