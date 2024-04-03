from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QApplication
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
    def __init__(self):
        super().__init__()

        self.dataframe = pd.read_csv(r'C:\Louis\Cours\Projet Peip2\PythonPrototypeGUI-main(3)\PythonPrototypeGUI-main\iris.csv')

        # Séparer les caractéristiques des labels
        X = self.dataframe.iloc[:, :-1]
        y = self.dataframe.iloc[:, -1]

        # Appliquer l'algorithme PCA sur les caractéristiques
        pca = PCA()
        pca.fit(X)

        # Créer la figure matplotlib
        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111)
        self.ax.plot(np.cumsum(pca.explained_variance_ratio_))
        self.ax.set_xlabel("Nombre de composantes principales")
        self.ax.set_ylabel("Pourcentage d'information conservé")
        self.ax.set_title("Pourcentage d'information conservé en fonction du nombre de PC")

        # Ajouter la figure à un widget FigureCanvas
        self.canvas = FigureCanvas(self.figure)

        # Ajouter la combo box pour sélectionner le pourcentage d'information à conserver
        self.pca_combo = QComboBox()
        self.pca_combo.setPlaceholderText("Pourcentage d'information à conserver")
        self.pca_combo.addItem("0.99")
        self.pca_combo.addItem("0.95")
        self.pca_combo.addItem("0.9")
        self.pca_combo.addItem("0.85")
        self.pca_combo.addItem("0.8")
        self.pca_combo.currentIndexChanged.connect(self.enable_pca_button)

        # Ajouter le bouton pour appliquer la PCA

        self.pca_button = QPushButton("Apply PCA")
        self.pca_button.setEnabled(False)
        self.pca_button.clicked.connect(self.apply_pca)



        ########## LAYOUT ###################
        # Créer le layout vertical
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        layout.addWidget(self.pca_combo)
        layout.addWidget(self.pca_button)

    def enable_pca_button(self):
        self.pca_button.setEnabled(True)
    def apply_pca(self):
        try:
            # Récupérer le pourcentage d'information à conserver sélectionné dans la combo box
            pct_variance_to_keep = float(self.pca_combo.currentText())

            # Appliquer l'algorithme PCA sur les caractéristiques en conservant le pourcentage d'information sélectionné
            pca = PCA(n_components=pct_variance_to_keep)
            X_pca = pca.fit_transform(self.dataframe.iloc[:, :-1])

            # Concaténer les composantes principales avec les labels
            self.dataframe_pca = pd.concat([pd.DataFrame(X_pca), self.dataframe.iloc[:, -1]], axis=1)

            # Afficher les résultats
            print("Dataframe après application de la PCA :")
            print(self.dataframe_pca.head())

        except Exception as e:
            print(f'exeption in apply_pca : {e}')

try:
    app = QApplication([])
    window = FenPCA()
    window.show()
    sys.exit(app.exec())
except Exception as e:
    print(f"Exeption: {e}")