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



class DataTesting(QWidget):
    def __init__(self, dataframe, classifier, model_name, hyperparameters):
        super().__init__()
        X_train = dataframe[0]
        X_test = dataframe[1]
        y_train = dataframe[2]
        self.actual = dataframe[3]  # le dataframe est désormais décomposé en 4 parties: X_train, X_test, Y_train et Y_test, suite à la data_modification

        self.prediction = classifier.predict(X_test)

        self.test_button = QPushButton("Test algorithm")
        self.test_button.clicked.connect(self.heat_confusion_matrix_test)

        model_label = QLabel(f"Classifier : {model_name}")
        model_font = QFont("Helvetica Neue", 20)
        model_label.setFont(model_font)
        hyperparameters_label = QLabel(hyperparameters)
        label_layout = QHBoxLayout()
        label_layout.addWidget(model_label)
        label_layout.addWidget(hyperparameters_label)
        self.f_label = QLabel()

        self.layout = QVBoxLayout()
        self.layout.addLayout(label_layout)
        self.layout.addWidget(self.f_label)
        self.fig_layout = QHBoxLayout()
        self.layout.addLayout(self.fig_layout)
        self.layout.addWidget(self.test_button)
        self.setLayout(self.layout)

    def heat_confusion_matrix_test(self):
        try:
            fig2, ax = plt.subplots(figsize=(16, 6))
            y_actual = self.actual
            y_predicted = self.prediction
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

        except Exception as e:
            print(f"Exception during heatmap creation: {e}")
            canvas = None

        F1_score = f1_score(self.actual, self.prediction, average= 'macro')
        self.fig_layout.addWidget(canvas)
        self.f_label.setText(f"F1 score : {str(F1_score)}")
