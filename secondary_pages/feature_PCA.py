from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPainter, QPen, QBrush, QColor, QDoubleValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSlider, QLabel, QComboBox, QApplication, QLineEdit
from sklearn.decomposition import PCA
from sklearn.decomposition import PCA
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import sys


class FenPCA(QWidget):
    def __init__(self, dataframe_splited):
        super().__init__()

        try:
            self.dataframe_splited = dataframe_splited
            # Séparer les caractéristiques des labels
            self.X_train = self.dataframe_splited[0]
            self.X_test = self.dataframe_splited[1]

            self.nb_components = np.shape(self.X_train)[1]
            self.seuil = self.nb_components
            self.seuil_line = None
            self.pct_variance_to_keep = 0.99999

            # Appliquer l'algorithme PCA sur les caractéristiques
            pca = PCA()
            pca.fit(self.X_train)

            # Créer la figure matplotlib
            self.figure = plt.figure()
            self.ax = self.figure.add_subplot(111)
            self.ax.plot(np.cumsum(pca.explained_variance_ratio_))
            self.threshold_list = np.cumsum(pca.explained_variance_ratio_)

           #Pour avoir des nombres entiers sur l'axe des abscisse
            x_ticks_positions = np.arange(0, len(pca.explained_variance_ratio_), step=1)
            # Définir les labels des ticks de l'axe des abscisses (convertis en entiers)
            x_ticks_labels = [int(x+1) for x in x_ticks_positions]

            plt.xticks(x_ticks_positions, x_ticks_labels)

            self.ax.set_xlabel("Nombre de composantes principales")
            self.ax.set_ylabel("Pourcentage d'information conservé")
            self.ax.set_title("Pourcentage d'information conservé en fonction du nombre de PC")

            # Ajouter la figure à un widget FigureCanvas
            self.canvas = FigureCanvas(self.figure)

            #Page title
            label = QLabel("Select the principle components")
            label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            label.adjustSize()
            font = QFont("Helvetica")
            font.setPointSize(15)
            font.setBold(True)
            label.setFont(font)

            #Generate the slider
            self.slider = QSlider()
            self.slider.setToolTip("Select the threshold of PCA")
            self.slider.setOrientation(Qt.Orientation.Horizontal)
            self.slider.setMinimumWidth(40)
            self.slider.setMinimum(0)
            self.slider.setMaximum(self.nb_components-1)
            self.slider.setValue(0)
            self.slider.setSingleStep(1)
            self.slider.valueChanged.connect(self.slider_update)


            ########## LAYOUT ###################
            label_seuil = QLabel()
            seuil_layout = QVBoxLayout()
            seuil_layout.setContentsMargins(0, 0, 0, 0)
            seuil_layout.addWidget(label_seuil)
            # seuil_layout.addWidget(self.seuil_input)
            seuil_layout.addWidget(self.slider)

            # Créer le layout vertical
            layout = QVBoxLayout(self)
            layout.addWidget(label)
            layout.setContentsMargins(30, 20, 30, 20)
            layout.addWidget(self.canvas)
            layout.addLayout(seuil_layout)


        except Exception as e:
            print(f"exeption dans FenPCA: {e}")

    def slider_update(self):
        print(self.slider.value())
        self.seuil = self.slider.value()
        self.print_seuil()
        self.apply_pca()

    def apply_pca(self):
        try:
            self.pct_variance_to_keep = float(self.threshold_list[self.seuil]-0.005)

        except Exception as e:
            print(f'exeption in apply_pca : {e}')

    def print_seuil(self):
        if self.seuil_line:  # Vérifiez si une ligne précédente existe
            self.seuil_line.remove()  # Supprimez la ligne précédente
        self.seuil_line = self.ax.axvline(x=self.seuil, color='r', linestyle='-')  # Ajoutez une nouvelle ligne
        self.canvas.draw()
