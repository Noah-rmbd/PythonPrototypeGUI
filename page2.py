
from photo import FenPhoto
from graphiques import *
from classe_bouton import Bouton


import sys
import os

class Page2(QWidget):
    def __init__(self,window):
        super().__init__()

        title = QLabel("Ouverture de nouveaux onglets")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter) #gérer l'alignement du texte
        title.setFont(QFont("Helvetica Neue", 20))

        btn1 = Bouton()
        btn1.setText("Ouvrir une photo")

        btn2 = Bouton()
        btn2.setText("Afficher un graphique")

        btn1.setMinimumSize(100, 200)
        btn2.setMinimumSize(100, 200)

        page2_layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        boutons_layout = QHBoxLayout()

        self.setLayout(page2_layout) #on met le layout de page 2 avec setLayout

        page2_layout.addLayout(title_layout)
        page2_layout.addLayout(boutons_layout) #on ajoute le bouton_layout avec addLayout

        title_layout.addWidget(title)

        boutons_layout.addWidget(btn1)
        boutons_layout.addWidget(btn2)
        btn2.clicked.connect(self.ouvrir_graph)

    
    def ouvrir_graph(self):
        self.fenetre_graph = FenGraph()
        self.fenetre_graph.show() #il faut ajouter self devant pour pas que la fenêtre se ferme automatiquement

    
