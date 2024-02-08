import numpy as np
from PyQt6.QtWidgets import *
from graphiques import FenGraph
from table_window import TableWindow
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from classe_bouton import *
from algos_predict import plot_algorithm_result


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
        bouton_cart.setMinimumHeight(150)
        bouton_cart.clicked.connect(self.ouvrir_cart)

        bouton_KNN = Bouton()
        bouton_KNN.setText("Utiliser l'algorithme KNN")
        bouton_KNN.setMinimumHeight(150)
        bouton_KNN.clicked.connect(self.ouvrir_KNN)

        bouton_random_forest = Bouton()
        bouton_random_forest.setText("Utiliser l'algorithme random forest")
        bouton_random_forest.setMinimumHeight(150)
        bouton_random_forest.clicked.connect(self.ouvrir_random_forest)

        main_layout = QVBoxLayout()

        bouton_layout = QHBoxLayout()
        bouton_layout.addWidget(bouton_cart)
        bouton_layout.addWidget(bouton_KNN)
        bouton_layout.addWidget(bouton_random_forest)

        label = QLabel()
        label.setText("Utiliser des algorithmes de machine learning")

        main_layout.addWidget(label)
        main_layout.addLayout(bouton_layout)
        self.setLayout(main_layout)

    def ouvrir_cart(self):
        plot_algorithm_result(DecisionTreeClassifier, self.matrice_sans_label,self.label_array, "Cart Algorithm")

    def ouvrir_KNN(self):
        plot_algorithm_result(KNeighborsClassifier,self.matrice_sans_label,self.label_array,"KNN Algorithm")

    def ouvrir_random_forest(self):
        plot_algorithm_result(RandomForestClassifier,self.matrice_sans_label,self.label_array, "Random Forest Algorithm")

