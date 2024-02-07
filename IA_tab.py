import numpy as np
from PyQt6.QtWidgets import *
from graphiques import FenGraph
from table_window import TableWindow
import pandas as pd
from classe_bouton import *
from algos_predict import cart,KNN,random_forest
import pandas as pd
import sys

class IATab(QWidget):
    def __init__(self,dataframe):
        super().__init__()
        self.dataframe = dataframe
        #self.dataframe = pd.read_csv(r'C:\Louis\Cours\Projet Peip2\PythonPrototypeGUI-main(2)\PythonPrototypeGUI-main\iris.csv')
        label=[]
        nrow = len(self.dataframe.index)

        for i in range(nrow):
            label.append(self.dataframe.iat[i,-1]) #-1 permet d'aller dans la denière colonne (où se trouve les labels)

        self.label_array = np.array(label)

        matrice = self.dataframe.to_numpy()
        self.matrice_sans_label = matrice[:,:-1]

        bouton_cart = Bouton()
        bouton_cart.setText("Utiliser l'algorithme cart")
        bouton_cart.clicked.connect(self.ouvrir_cart)

        bouton_KNN = Bouton()
        bouton_KNN.setText("Utiliser l'algorithme KNN")
        bouton_KNN.clicked.connect(self.ouvrir_KNN)

        bouton_random_forest = Bouton()
        bouton_random_forest.setText("Utiliser l'algorithme random forest")
        bouton_random_forest.clicked.connect(self.ouvrir_random_forest)

        main_layout = QVBoxLayout()

        bouton_layout = QHBoxLayout()
        bouton_layout.addWidget(bouton_cart)
        bouton_layout.addWidget(bouton_KNN)
        bouton_layout.addWidget(bouton_random_forest)

        label = QLabel()
        label.setText("Utiliser des algorithme de machine learning")

        main_layout.addWidget(label)
        main_layout.addLayout(bouton_layout)
        self.setLayout(main_layout)

    def ouvrir_cart(self):
        cart(self.matrice_sans_label,self.label_array)

    def ouvrir_KNN(self):
        KNN(self.matrice_sans_label,self.label_array)

    def ouvrir_random_forest(self):
        random_forest(self.matrice_sans_label,self.label_array)

# app = QApplication([])
# window = IATab()
# window.show()
# sys.exit(app.exec())