
import sys
import pandas as pd

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout,QApplication
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import seaborn as sns


class FenGraph(QWidget):
    def __init__(self, data_frame):
        super().__init__()
        #self.setWindowTitle("Graphique")
        #self.setGeometry(400, 150, 800, 600)

        # Load data from Excel file
        self.donnee = data_frame

        self.columns = list(self.donnee.columns)
        print("graph",self.columns)

        # Create Matplotlib figure and axis
        self.figure = Figure(figsize=(8, 5))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasQTAgg(self.figure) #ce qui permet de gérer l'affichage du graphique

        # ComboBox pour la sélection de la colonne(abscisse)
        self.column_combo_abs = QComboBox(self)
        self.column_combo_abs.clear()
        self.column_combo_abs.addItems(self.columns)
        print("OK")

        # ComboBox pour la sélection de la colonne (ordonnée)
        self.column_combo_ord = QComboBox(self)
        self.column_combo_ord.clear()
        self.column_combo_ord.addItems(self.columns)


        #choix du type de graphique
        self.choose_graph_type = QComboBox(self)
        self.choose_graph_type.addItem("Nuage de point")
        self.choose_graph_type.addItem("Courbe")
        self.choose_graph_type.addItem("Histogramme")
        self.choose_graph_type.addItem("Boîte à moustaches")

        self.choose_graph_type.currentIndexChanged.connect(self.update_plot_based_on_selection)
        self.column_combo_abs.currentIndexChanged.connect(self.update_plot_based_on_selection)
        self.column_combo_ord.currentIndexChanged.connect(self.update_plot_based_on_selection)

        toolbar = NavigationToolbar2QT(self.canvas)

##############      LAYOUT      ################################################
        layout = QVBoxLayout(self)
        label = QLabel("Afficher des graphiques")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.adjustSize()
        font = QFont()
        font.setPointSize(30)
        label.setFont(font)
        layout.addWidget(label)
        layout.addWidget(self.choose_graph_type)
        layout.addWidget(self.canvas)
        layout.addWidget(toolbar)

        layout_btn_abs = QHBoxLayout(self)
        abs_label = QLabel("Choisissez la variable en abscisse : ")
        layout_btn_abs.addWidget(abs_label)
        layout_btn_abs.addWidget(self.column_combo_abs)

        layout_btn_ord = QHBoxLayout(self)
        ord_label = QLabel("Choississez la variable en ordonnée : ")
        layout_btn_ord.addWidget(ord_label)
        layout_btn_ord.addWidget(self.column_combo_ord)

        layout.addLayout(layout_btn_abs)
        layout.addLayout(layout_btn_ord)


 #############################################################################

        # Initial plot with all columns
        self.update_plot_based_on_selection()

    def update_plot_based_on_selection(self):
        selected_abs_col = self.column_combo_abs.currentText()
        selected_ord_col = self.column_combo_ord.currentText()

        try:
            if self.choose_graph_type.currentText() == "Nuage de point":
                self.scatter_plot(selected_abs_col, selected_ord_col)
                self.column_combo_ord.setEnabled(True)

            elif self.choose_graph_type.currentText() == "Courbe":
                self.courbe_plot(selected_abs_col, selected_ord_col)
                self.column_combo_ord.setEnabled(True)

            elif self.choose_graph_type.currentText() == "Histogramme":
                self.histo_plot(selected_abs_col)
                self.column_combo_ord.setEnabled(False)

            elif self.choose_graph_type.currentText() == "Boîte à moustaches":
                self.box_plot(self.donnee)
                self.column_combo_ord.setEnabled(True)

        except Exception as e:
            print(f"Exception: {e}")


    def scatter_plot(self, abs_col, ord_col):
        self.ax.clear()
        self.ax.scatter(self.donnee[abs_col], self.donnee[ord_col])
        self.ax.legend()
        self.canvas.draw()

    def courbe_plot(self, abs_col, ord_col):
        self.ax.clear()

        sorted_data = self.donnee.sort_values(by=abs_col) #permet de trier les données pour print dans le bon ordre
        self.ax.plot(sorted_data[abs_col], sorted_data[ord_col])


        self.ax.legend()
        self.canvas.draw()

    def histo_plot(self, abs_col):
        self.ax.clear()

        sorted_data = self.donnee.sort_values(by=abs_col)  # permet de trier les données pour print dans le bon ordre
        self.ax.hist(sorted_data[abs_col], bins='auto', density=True) #bins gère la hauteur des barres de l'histo
        self.ax.set_ylabel('Fréquence')

        self.ax.legend()
        self.canvas.draw()

    def box_plot(self, data):
        self.ax.clear()
        self.ax.boxplot(data)

        self.ax.legend()
        self.canvas.draw()



    # def box_plot (self, abs_col, ord_col):
    #     self.ax.clear()
    #     self.ax.sns.boxplot(x=[abs_col],y=[ord_col])
    #
    #     self.ax.legend()
    #     self.canvas.draw()



    # def box_plot (self,donnee, abs_col, ord_col):
    #     sns.boxplot(x=donnee[abs_col],y=donnee[ord_col])
