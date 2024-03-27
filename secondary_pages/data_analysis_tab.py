import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout,QApplication
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import sys

class FenData(QWidget):
    def __init__(self,j_in=None):
        super().__init__()

        self.j = j_in
        self.seuil_value = None
        self.seuil_line = None
        self.seuil_combo = QComboBox()

        self.dataframe = pd.read_csv(r'C:\Louis\Cours\Projet Peip2\PythonPrototypeGUI-main(3)\PythonPrototypeGUI-main\iris.csv')
        #self.dataframe = dataframe
        print(self.dataframe)

        X = self.dataframe.iloc[:, :-1]
        y = self.dataframe.iloc[:, -1]

        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

        clf = DecisionTreeClassifier()
        clf.fit(X_train, y_train)

        feature_importances = clf.feature_importances_
        self.feature_importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': feature_importances})
        self.feature_importance_df = self.feature_importance_df.sort_values(by='Importance', ascending=False)

        # Display the result
        print("Feature Importances:")
        print(self.feature_importance_df)

        # Plot the bar chart
        self.figure, self.ax = plt.subplots()
        self.ax.bar(self.feature_importance_df['Feature'], self.feature_importance_df['Importance'],color="blue")
        self.ax.set_ylabel('Importance')
        self.ax.set_title('Feature Importances')

        # Embed the Matplotlib plot in the PyQt application
        self.canvas = FigureCanvas(self.figure)


        self.drop_features_button = QPushButton("Drop Features")

        self.drop_features_button.setEnabled(False)
        self.seuil_combo.currentIndexChanged.connect(self.enable_drop_features_button)
        self.drop_features_button.clicked.connect(self.drop_features)
        self.drop_features_button.enterEvent = None
        self.drop_features_button.leaveEvent = None

        ##############      LAYOUT      ################################################
        seuil_layout=QVBoxLayout()
        label_seuil = QLabel("Sélectionez une valeur seuil pour la conservation des données les plus importantes")

        self.seuil_combo.setPlaceholderText("Valeur du seuil")
        self.seuil_combo.addItem("0.5")
        self.seuil_combo.addItem("0.4")
        self.seuil_combo.addItem("0.3")
        self.seuil_combo.addItem("0.25")
        self.seuil_combo.addItem("0.2")
        self.seuil_combo.addItem("0.15")
        self.seuil_combo.addItem("0.1")
        self.seuil_combo.addItem("0.05")
        self.seuil_combo.addItem("0.03")
        self.seuil_combo.addItem("0.01")
        self.seuil_combo.addItem("0.00")

        self.seuil_combo.currentIndexChanged.connect(self.print_seuil)

        seuil_layout.addWidget(label_seuil)
        seuil_layout.addWidget(self.seuil_combo)

        self.drop_features_button.setMinimumSize(150,150)

        layout_info_gain = QVBoxLayout(self)
        label = QLabel("Selection des caractéristiques")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.adjustSize()
        font = QFont()
        font.setPointSize(30)
        label.setFont(font)
        layout_info_gain.addWidget(label)
        layout_info_gain.addWidget(self.canvas)
        layout_info_gain.addLayout(seuil_layout)
        layout_info_gain.addWidget(self.drop_features_button)




    def enable_drop_features_button(self):
        self.drop_features_button.setEnabled(True)
        self.drop_features_button.enterEvent = self.highlight_features
        self.drop_features_button.leaveEvent = self.reset_colors
    def print_seuil(self):
        self.seuil_value = float(self.seuil_combo.currentText())
        if self.seuil_line:  # Vérifiez si une ligne précédente existe
            self.seuil_line.remove()  # Supprimez la ligne précédente
        self.seuil_line = self.ax.axhline(y=self.seuil_value, color='r', linestyle='-')  # Ajoutez une nouvelle ligne
        self.canvas.draw()

    def drop_features(self):
        try:
            important_features = self.feature_importance_df[self.feature_importance_df['Importance'] >= self.seuil_value][
                'Feature']
            self.dataframe_droped = self.dataframe[important_features]

            # self.j=4
            # # Ajoutez la colonne de labels au DataFrame filtré
            # if self.j is not None:
            #     labels_column_name = self.dataframe.columns[self.j]
            #     self.dataframe_droped.loc[:, labels_column_name] = self.dataframe[labels_column_name]
            # #loc permet d'accéder aux valeurs de la colonne du label

            print("Dataframe après suppression des colonnes :")
            print(self.dataframe_droped.head())
        except Exception as e:
            print (f"exeption in drop features: {e}")

    def highlight_features(self, event):
        for i, importance in enumerate(self.feature_importance_df['Importance']):
            if importance < self.seuil_value:
                self.ax.patches[i].set_facecolor('r')
        self.canvas.draw()

    def reset_colors(self, event):
        for patch in self.ax.patches:
            patch.set_facecolor('b')
        self.canvas.draw()


# try:
#     app = QApplication([])
#     window = FenData()
#     window.show()
#     sys.exit(app.exec())
# except Exception as e:
#     print(f"Exeption: {e}")
