from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtQuick import *
from PyQt6.QtQml import *
from time import *
from photo import FenPhoto
from graphiques import *
from classe_bouton import Bouton


import sys
import os

class Page2(QWidget):
    def __init__(self,window):
        super().__init__()
        # on met un self car on va appeler ce gros widget dans le main

        title = QLabel("Ouverture de nouveaux onglets")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter) #gérer l'alignement du texte
        title.setFont(QFont("Helvetica Neue", 20))

        btn1 = Bouton()
        btn1.setText("Ouvrir une photo")

        #btn2 = Bouton()
        #btn2.setText("Afficher un graphique")

        btn1.setMinimumSize(100, 200)
        #btn2.setMinimumSize(100, 200)

        page2_layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        boutons_layout = QHBoxLayout()

        self.setLayout(page2_layout) #on met le layout de page 2 avec setLayout

        page2_layout.addLayout(title_layout)
        page2_layout.addLayout(boutons_layout) #on ajoute le bouton_layout avec addLayout

        title_layout.addWidget(title)

        boutons_layout.addWidget(btn1)
        #boutons_layout.addWidget(btn2)

        btn1.clicked.connect(self.ouvrir_photo)
        #btn2.clicked.connect(self.ouvrir_graph)

    def ouvrir_photo(self):
        fenetre_photo = FenPhoto()
        fenetre_photo.exec()

    #def ouvrir_additionneur(self):
        #fenetre_additionneur = FenAdditionneur()
        #fenetre_additionneur.exec()

    def ouvrir_graph(self):
        self.fenetre_graph = FenGraph()
        self.fenetre_graph.show() #il faut ajouter self devant pour pas que la fenêtre se ferme automatiquement

    # class DisplayImageWidget(QWidget):
    #     def __init__(self):
    #         super(DisplayImageWidget, self).__init__()
    #         self.image = cv2.imread('2.png')
    #         self.convert = QImage(self.image, self.image.shape[1], self.image.shape[0], self.image.strides[0],
    #                               QImage.Format.Format_BGR888)
    #         self.frame = QLabel()
    #         self.frame.setPixmap(QPixmap.fromImage(self.convert))
    #
    #         self.layout = QHBoxLayout(self)
    #         self.layout.addWidget(self.frame)
    #


