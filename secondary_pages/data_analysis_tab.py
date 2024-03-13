
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout,QApplication
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import sys
class FenData(QWidget):
    def __init__(self,dataframe):
        super().__init__()

        #self.dataframe = pd.read_csv(r'C:\Louis\Cours\Projet Peip2\PythonPrototypeGUI-main(3)\PythonPrototypeGUI-main\iris.csv')
        self.dataframe = dataframe

        X = self.dataframe.iloc[:, :-1]
        y = self.dataframe.iloc[:, -1]

        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

        clf = DecisionTreeClassifier()
        clf.fit(X_train, y_train)

        feature_importances = clf.feature_importances_
        feature_importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': feature_importances})
        feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

        # Display the result
        print("Feature Importances:")
        print(feature_importance_df)

        # Plot the bar chart
        self.figure, self.ax = plt.subplots()
        self.ax.bar(feature_importance_df['Feature'], feature_importance_df['Importance'])
        self.ax.set_ylabel('Importance')
        self.ax.set_title('Feature Importances')

        # Embed the Matplotlib plot in the PyQt application
        self.canvas = FigureCanvas(self.figure)

        ##############      LAYOUT      ################################################
        layout = QVBoxLayout(self)
        label = QLabel("Analyse de données")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.adjustSize()
        font = QFont()
        font.setPointSize(30)
        label.setFont(font)
        layout.addWidget(label)
        layout.addWidget(self.canvas)

# app = QApplication([])
# window = FenData()
# window.show()
# sys.exit(app.exec())
