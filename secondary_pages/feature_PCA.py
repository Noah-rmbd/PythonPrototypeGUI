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
    def __init__(self,dataframe_splited):
        super().__init__()

        try:
            self.dataframe_splited = dataframe_splited
            #self.dataframe_splited = pd.read_csv("C:\Louis\Cours\Projet Peip2\PythonPrototypeGUI-main(6)\PythonPrototypeGUI-main\iris.csv")
            # Séparer les caractéristiques des labels
            self.X_train = self.dataframe_splited[0]
            self.X_test = self.dataframe_splited[1]

            self.nb_components = np.shape(self.X_train)[1]
            print("nb_component:",self.nb_components)

            print(self.X_train, self.X_test)

            # Appliquer l'algorithme PCA sur les caractéristiques
            pca = PCA()
            pca.fit(self.X_train)

            # Créer la figure matplotlib
            self.figure = plt.figure()
            self.ax = self.figure.add_subplot(111)
            self.ax.plot(np.cumsum(pca.explained_variance_ratio_))

           #Pour avoir des nombres entiers sur l'axe des abscisse
            x_ticks_positions = np.arange(1, len(pca.explained_variance_ratio_), step=1)
            # Définir les labels des ticks de l'axe des abscisses (convertis en entiers)
            x_ticks_labels = [int(x) for x in x_ticks_positions]

            plt.xticks(x_ticks_positions, x_ticks_labels)

            self.ax.set_xlabel("Nombre de composantes principales")
            self.ax.set_ylabel("Pourcentage d'information conservé")
            self.ax.set_title("Pourcentage d'information conservé en fonction du nombre de PC")

            # Ajouter la figure à un widget FigureCanvas
            self.canvas = FigureCanvas(self.figure)

            self.pca_lineedit = QLineEdit()
            self.pca_lineedit.setPlaceholderText("Pourcentage d'information à conserver (ex: 0.99)")
            self.pca_lineedit.setValidator(QDoubleValidator())  # Assure que seul un nombre décimal est entré

            # Connecter un signal pour détecter les changements dans le texte
            self.pca_lineedit.textChanged.connect(self.enable_pca_button)

            # Ajouter le bouton pour appliquer la PCA

            self.pca_button = QPushButton("Apply PCA")
            self.pca_button.setEnabled(False)
            self.pca_button.clicked.connect(self.apply_pca)

            self.slider = QSlider()
            self.slider.setToolTip("Select the threshold of PCA")
            self.slider.setOrientation(Qt.Orientation.Horizontal)
            self.slider.setMinimumWidth(40)
            self.slider.setMinimum(0)
            self.slider.setMaximum(self.nb_components)
            self.slider.setValue(0)
            # self.slider.setTickInterval(10)
            self.slider.setSingleStep(1)
            # self.slider.setPageStep(10)
            self.slider.valueChanged.connect(self.pr)
            # self.slider.enterEvent = self.highlight_features
            # self.slider.leaveEvent = self.reset_colors

            # Ajouter le bouton pour appliquer la PCA

            self.pca_button = QPushButton("Apply PCA")
            self.pca_button.setEnabled(False)
            self.pca_button.clicked.connect(self.apply_pca)

            ########## LAYOUT ###################
            label_seuil = QLabel()
            seuil_layout = QVBoxLayout()
            seuil_layout.addWidget(label_seuil)
            # seuil_layout.addWidget(self.seuil_input)
            seuil_layout.addWidget(self.slider)

            # Créer le layout vertical
            layout = QVBoxLayout(self)
            layout.addWidget(self.canvas)
            layout.addWidget(self.pca_lineedit)
            layout.addLayout(seuil_layout)

            layout.addWidget(self.pca_button)


        except Exception as e:
            print(f"exeption dans FenPCA: {e}")

    def pr(self):
        print(self.slider.value())

    def enable_pca_button(self):
        self.pca_button.setEnabled(True)
    def apply_pca(self):
        try:
            # Récupérer le pourcentage d'information à conserver entré dans le QLineEdit
            pct_variance_to_keep_str = self.pca_lineedit.text()

            # Remplacer la virgule par un point pour s'assurer que le float est bien formé
            pct_variance_to_keep_str = pct_variance_to_keep_str.replace(',', '.')

            # Convertir le pourcentage en float
            pct_variance_to_keep = float(pct_variance_to_keep_str)

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

