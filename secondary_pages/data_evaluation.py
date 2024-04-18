import numpy as np
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

import seaborn as sns

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from sklearn import metrics
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, cross_val_score

from components.classe_bouton import *

class DataEvaluation(QWidget):
    def __init__(self, dataframe_splited):
        super().__init__()
        label = QLabel("Fin du logiciel, merci de l'avoir utilisé")

        X_train = dataframe_splited[0]
        X_test = dataframe_splited[1]
        y_train = dataframe_splited[2]
        y_test = dataframe_splited[3]

        classifier_1 = DecisionTreeClassifier()
        classifier_2 = KNeighborsClassifier()
        classifier_3 = RandomForestClassifier()
        classifier_4 = MLPClassifier()

        classifier_1.fit(X_train, y_train)
        classifier_2.fit(X_train, y_train)
        classifier_3.fit(X_train, y_train)
        classifier_4.fit(X_train, y_train)

        predict1 = classifier_1.predict(X_test)
        predict2 = classifier_2.predict(X_test)
        predict3 = classifier_3.predict(X_test)
        predict4 = classifier_4.predict(X_test)

        liste = [predict1,predict2,predict3,predict4]

        main_layout = QVBoxLayout()

        for i in liste:
            canva = self.heat_confusion_matrix_test(y_test, i)
            main_layout.addWidget(canva)

        main_layout.addWidget(label)

        self.setLayout(main_layout)

    def heat_confusion_matrix_test(self, y_actual, y_predicted):

        fig2, ax = plt.subplots(figsize=(16, 6))
        cm = confusion_matrix(y_actual, y_predicted)
        sns.heatmap(cm,
                    annot=True,
                    fmt='g',
                    xticklabels=np.unique(y_actual),
                    yticklabels=np.unique(y_actual)
                    )

        plt.ylabel('Prediction', fontsize=13)
        plt.xlabel('Actual', fontsize=13)

        plt.title('Testing Confusion Matrix', fontsize=17)

        # Ajouter la figure à la mise en page canvas_layout
        canvas = FigureCanvasQTAgg(fig2)

        return canvas