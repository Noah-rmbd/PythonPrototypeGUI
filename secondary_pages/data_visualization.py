from PyQt6.QtWidgets import QFileDialog, QLineEdit, QComboBox, QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QTabWidget, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtGui import QFont
from secondary_pages.graphs_tab import FenGraph
from secondary_pages.table_tab import TableTab
from secondary_pages.stats_tab import StatsTab


class DataVisualization(QTabWidget):
    def __init__(self, data_frame, loading_bar):
        super().__init__()
        self.data_frame = data_frame

        self.setContentsMargins(30, 20, 30, 30)

        tab_table = TableTab(self.data_frame, loading_bar)
        tab_graph = FenGraph(self.data_frame)
        tab_stats = StatsTab(self.data_frame)


        self.addTab(tab_table, "Table")
        self.addTab(tab_graph, "Graphs")
        self.addTab(tab_stats, "Stats")

        self.table_widget = tab_table.table_widget
        self.setTabPosition(QTabWidget.TabPosition.South)
