from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPainter, QPen, QBrush, QColor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSlider, QLabel, QComboBox, QApplication
from sklearn.decomposition import PCA
from sklearn.decomposition import PCA
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import sys

class Slider(QSlider):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setOrientation(Qt.Orientation.Horizontal)
        print("cul")
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(50)
        self.setTickInterval(10)
        self.setSingleStep(1)
        self.setPageStep(10)

    '''
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # Dessiner le fond de la barre spider
        painter.setBrush(QBrush(QColor("white")))
        painter.drawRect(self.rect())

        # Dessiner la ligne centrale
        pen = QPen(QColor("black"))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(self.width() / 2, 0, self.width() / 2, self.height())

        # Dessiner les lignes des graduations
        pen.setWidth(1)
        painter.setPen(pen)
        for i in range(1, 11):
            x = self.width() / 2 + (i - 5) * self.width() / 10
            painter.drawLine(x, self.height() - 5, x, self.height())
            painter.drawText(x - 5, self.height() + 15, str(i * 10))

        # Dessiner le curseur de la barre spider
        pen.setWidth(3)
        painter.setPen(pen)
        brush = QBrush(QColor("red"))
        painter.setBrush(brush)
        x = self.width() / 2 + (self.value() - 50) * self.width() / 100
        painter.drawEllipse(x - 5, self.height() - 15, 10, 10)
    '''

class FenPCA(QWidget):
    def __init__(self, dataframe_splited):
        super().__init__()

        self.dataframe_splited = dataframe_splited

        # Séparer les caractéristiques des labels
        self.X_train = self.dataframe_splited[0]
        self.X_test = self.dataframe_splited[1]

        print(self.X_train, self.X_test)

        # Appliquer l'algorithme PCA sur les caractéristiques
        pca = PCA()
        pca.fit(self.X_train)

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

    def pr(self):
        print(self.slider.value())

    def enable_pca_button(self):
        self.pca_button.setEnabled(True)
    def apply_pca(self):
        try:
            # Récupérer le pourcentage d'information à conserver sélectionné dans la combo box
            pct_variance_to_keep = float(self.pca_combo.currentText())

            # Appliquer l'algorithme PCA sur les caractéristiques en conservant le pourcentage d'information sélectionné
            pca = PCA(n_components=pct_variance_to_keep)
            self.X_train = pca.fit_transform(self.X_train)
            self.X_test = pca.fit_transform(self.X_test)

            print("X_train_pca", self.X_train)
            print("X_test_pca", self.X_test)


            # Concaténer les composantes principales avec les labels
            #self.dataframe_pca = pd.concat([pd.DataFrame(X_pca), self.dataframe.iloc[:, -1]], axis=1)

            # Afficher les résultats
            #print("Dataframe après application de la PCA :")
            #print(self.dataframe_pca.head())

        except Exception as e:
            print(f'exeption in apply_pca : {e}')
