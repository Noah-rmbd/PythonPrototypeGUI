from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtQuick import *
from PyQt6.QtQml import *
from time import *

class FenPhoto(QDialog):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("La Fenêtre de la photo")
        layout.addWidget(label)
        self.setGeometry(400,400,200,200)
        self.setLayout(layout)


        # Charger l'image avec QPixmap
        pixmap = QPixmap(r'C:\Louis\Cours\Projet Peip2\eolienne.jpg') #on utilise r pour faire une chaîne brute et éviter les problèmes avec les backslash

        label_image = QLabel()
        # Afficher l'image dans le QLabel
        label_image.setPixmap(pixmap)

        # Ajouter l'image au layout
        layout.addWidget(label_image)

