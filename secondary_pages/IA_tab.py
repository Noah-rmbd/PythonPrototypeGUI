import numpy as np
from PyQt6.QtWidgets import *
from secondary_pages.graphs_tab import FenGraph
from secondary_pages.table_tab import TableWindow
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from components.classe_bouton import *
from components.algos_predict import plot_algorithm_result

import pandas as pd
import sys


class IATab(QWidget):
    def __init__(self, dataframe):
        super().__init__()
        self.dataframe = dataframe
        # self.dataframe = pd.read_csv(r'C:\Louis\Cours\Projet Peip2\PythonPrototypeGUI-main(2)\PythonPrototypeGUI-main\iris.csv')
        label = []
        nrow = len(self.dataframe.index)

        for i in range(nrow):
            label.append(
                self.dataframe.iat[i, -1])  # -1 permet d'aller dans la denière colonne (où se trouve les labels)

        self.label_array = np.array(label)

        matrice = self.dataframe.to_numpy()
        self.matrice_sans_label = matrice[:, :-1]

        self.algo_type_combo = QComboBox(self)
        self.algo_type_combo.addItem("Choisissez un algorithme")
        self.algo_type_combo.addItem("CART")
        self.algo_type_combo.addItem("KNN")
        self.algo_type_combo.addItem("Random Forest")

        self.algo_type_combo.currentIndexChanged.connect(self.update_based_on_selection)

        self.main_layout = QVBoxLayout()
        test_size_layout = QHBoxLayout()
        self.main_layout.addWidget(self.algo_type_combo)

        label = QLabel()
        label.setText("Utiliser des algorithmes de machine learning")

        text_test_size = QLabel("Select the percentage of items used for testing model :")

        self.test_size_box = QComboBox()
        self.test_size_box.setMaximumWidth(100)
        self.test_size_box.addItem("20 %")
        self.test_size_box.addItem("30 %")
        self.test_size_box.addItem("40 %")
        self.test_size_box.addItem("50 %")

        self.main_layout.addWidget(label)
        test_size_layout.addWidget(text_test_size)
        test_size_layout.addWidget(self.test_size_box)
        self.main_layout.addLayout(test_size_layout)

        self.main_layout.addWidget(self.algo_type_combo)
        self.setLayout(self.main_layout)

    def ouvrir_cart(self):
        test_size = float(self.test_size_box.currentText()[:2]) / 100
        canvas = plot_algorithm_result(DecisionTreeClassifier, self.matrice_sans_label, self.label_array, "Cart Algorithm",
                              test_size)

        self.main_layout.addWidget(canvas[0])
        self.main_layout.addWidget(canvas[1])


    def ouvrir_KNN(self):
        test_size = float(self.test_size_box.currentText()[:2]) / 100
        plot_algorithm_result(KNeighborsClassifier, self.matrice_sans_label, self.label_array, "KNN Algorithm",
                              test_size)

    def ouvrir_random_forest(self):
        test_size = float(self.test_size_box.currentText()[:2]) / 100
        plot_algorithm_result(RandomForestClassifier, self.matrice_sans_label, self.label_array,
                              "Random Forest Algorithm", test_size)

    def update_based_on_selection(self):
        try:
            if self.algo_type_combo.currentText() == "CART":
                self.ouvrir_cart()

            elif self.algo_type_combo.currentText() == "KNN":
                self.ouvrir_KNN()

            elif self.algo_type_combo.currentText() == "Random Forest":
                self.ouvrir_random_forest()

        except Exception as e:
            print(f"Exception: {e}")
