from PyQt6.QtWidgets import *
from graphs_tab import FenGraph
from table_tab import TableWindow
from stats_tab import StatsTab
import pandas as pd
from data_analysis_tab import FenData

class FileWindow(QWidget):
    def __init__(self, file_url):
        QWidget.__init__(self)
        self.setWindowTitle("Fichier : "+file_url)

        layout = QGridLayout()
        self.setLayout(layout)

        if file_url[-4:] == ".csv":
            self.data_frame = pd.read_csv(file_url)
        else:
            self.data_frame = pd.read_excel(file_url)

        self.tab_table = TableWindow(self.data_frame)
        self.tab_graph = FenGraph(self.tab_table.data_frame)
        self.tab_stats = StatsTab(self.tab_table.data_frame)
        self.tab_data_analysis = FenData(self.tab_table.data_frame)

        self.tab_table.insert_after.clicked.connect(self.update_tabs)
        self.tab_table.delete_button.clicked.connect(self.update_tabs)

        self.tabwidget = QTabWidget()
        self.tabwidget.addTab(self.tab_table, "Tableau")
        self.tabwidget.addTab(self.tab_graph, "Graphique")
        self.tabwidget.addTab(self.tab_stats,"Stats")
        self.tabwidget.addTab(self.tab_data_analysis, "Analyse de données")
        layout.addWidget(self.tabwidget, 0, 0)

    def update_tabs(self):
        self.tab_graph = FenGraph(self.tab_table.data_frame)
        self.tab_stats = StatsTab(self.tab_table.data_frame)
        self.tabwidget.removeTab(2)
        self.tabwidget.removeTab(1)
        self.tabwidget.addTab(self.tab_graph, "Graphique")
        self.tabwidget.addTab(self.tab_stats, "Stats")
        

