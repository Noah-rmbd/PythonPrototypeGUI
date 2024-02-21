from PyQt6.QtWidgets import *
from secondary_pages.graphs_tab import FenGraph
from secondary_pages.table_tab import TableWindow
from secondary_pages.stats_tab import StatsTab
from secondary_pages.IA_tab import IATab
import pandas as pd

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
        self.tab_IA = IATab(self.tab_table.data_frame)

        self.tab_table.insert_after.clicked.connect(self.update_tabs)
        self.tab_table.delete_button.clicked.connect(self.update_tabs)
        self.tab_table.save_button.clicked.connect(self.update_tabs)
        self.tab_table.save_changes.clicked.connect(self.update_tabs)
        self.tab_table.normalize_button.clicked.connect(self.update_tabs)
        self.tab_table.back_button.clicked.connect(self.update_tabs)


        self.tabwidget = QTabWidget()
        self.tabwidget.addTab(self.tab_table, "Tableau")
        self.tabwidget.addTab(self.tab_graph, "Graphique")
        self.tabwidget.addTab(self.tab_stats,"Stats")
        self.tabwidget.addTab(self.tab_IA, "IA")
        layout.addWidget(self.tabwidget, 0, 0)




    def update_tabs(self):
        self.data_frame = self.tab_table.data_frame.copy()
        #print(self.data_frame)
        self.tab_graph = FenGraph(self.data_frame)
        self.tab_stats = StatsTab(self.data_frame)


        self.tabwidget.removeTab(3)
        self.tabwidget.removeTab(2)
        self.tabwidget.removeTab(1)

        self.tabwidget.addTab(self.tab_graph, "Graphique")
        self.tabwidget.addTab(self.tab_stats, "Stats")
        self.tabwidget.addTab(self.tab_IA, "IA")
