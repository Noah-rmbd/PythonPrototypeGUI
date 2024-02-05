from PyQt6.QtWidgets import *
from graphiques import FenGraph
from table_window import TableWindow
import pandas as pd

class FileWindow(QWidget):
    def __init__(self, file_url):
        QWidget.__init__(self)
        self.setWindowTitle("Fichier : "+file_url)

        layout = QGridLayout()
        self.setLayout(layout)

        if file_url[-4:]==".csv" :
            self.data_frame = pd.read_csv(file_url)
        else :
            self.data_frame = pd.read_excel(file_url)

        self.tab_table = TableWindow(self.data_frame)
        self.tab_graph = FenGraph(self.tab_table.data_frame)

        self.tab_table.insert_after.clicked.connect(self.update_graph)
        self.tab_table.delete_button.clicked.connect(self.update_graph)

        self.tabwidget = QTabWidget()
        self.tabwidget.addTab(self.tab_table, "Tableau")
        self.tabwidget.addTab(self.tab_graph, "Graphique")
        layout.addWidget(self.tabwidget, 0, 0)

    def update_graph(self):
        self.tab_graph = FenGraph(self.tab_table.data_frame)
        self.tabwidget.removeTab(1)
        self.tabwidget.addTab(self.tab_graph, "Graphique")
        #self.tab_graph = FenGraph(self.tab_table.data_frame)
        #print(self.tab_table.data_frame)


