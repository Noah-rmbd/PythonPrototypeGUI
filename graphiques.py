import sys
import pandas as pd

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout,QApplication
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

class FenGraph(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graphique")
        self.setGeometry(400, 150, 800, 600)

        # Load data from Excel file
        self.donnee = pd.read_excel('test.xlsx')
        self.columns = list(self.donnee.columns)

        # Create Matplotlib figure and axis
        self.figure = Figure(figsize=(8, 5))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasQTAgg(self.figure) #ce qui permet de gérer l'affichage du graphique

        # ComboBox pour la sélection de la colonne(abscisse)
        self.column_combo_abs = QComboBox(self)
        self.column_combo_abs.addItems(self.columns)

        # ComboBox pour la sélection de la colonne (ordonnée)
        self.column_combo_ord = QComboBox(self)
        self.column_combo_ord.addItems(self.columns)

        # Create button to update the plot
        self.update_button = QPushButton("Update Plot", self)
        self.update_button.clicked.connect(self.update_plot)

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

        layout.addWidget(self.update_button)
 #############################################################################

        # Initial plot with all columns
        self.update_plot()

    def update_plot(self):
        selected_abs_col = self.column_combo_abs.currentText()
        selected_ord_col = self.column_combo_ord.currentText()

        self.ax.clear()

        # Plot the selected column
        self.ax.plot(self.donnee[selected_abs_col],self.donnee[selected_ord_col])
        self.ax.legend()
        self.canvas.draw()

# app = QApplication([])
# window = FenGraph()
# window.show()
# sys.exit(app.exec())






