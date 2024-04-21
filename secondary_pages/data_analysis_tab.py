from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QDoubleValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QComboBox, QLineEdit, QPushButton, QApplication, QHBoxLayout
import pandas as pd
from sklearn.feature_selection import mutual_info_classif
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class FenData(QWidget):
    def __init__(self, dataframe_columns, dataframe_splited, next_step_bar, j_in=None):
        super().__init__()
        next_step_bar.show_status("Calculating info classifier")
        QApplication.processEvents()

        self.j = j_in
        self.seuil = 0
        self.seuil_line = None
        #self.seuil_input = QLineEdit()
        #self.seuil_input.setPlaceholderText("Valeur du seuil")

        self.index_features_to_del = None

        validator = QDoubleValidator(0.0, 1.0, 2)  # 2 décimales
        #self.seuil_input.setValidator(validator)

        window_style = (
            'background-color:white'
        )

        self.dataframe_splited = dataframe_splited

        clf = mutual_info_classif(self.dataframe_splited[0], self.dataframe_splited[2])

        self.dataframe_columns = list(dataframe_columns)
        self.dataframe_columns = dataframe_columns[:-1]

        self.feature_importance_df = pd.DataFrame({'Feature': self.dataframe_columns, 'Importance': clf})
        self.feature_importance_df = self.feature_importance_df.sort_values(by='Importance', ascending=False)

        # Display the result
        print("Feature Importances:")
        print(self.feature_importance_df)
        self.max_importance = max(list(self.feature_importance_df['Importance']))

        # Plot the bar chart
        self.figure, self.ax = plt.subplots()
        self.ax.bar(self.feature_importance_df['Feature'], self.feature_importance_df['Importance'], color="blue")
        self.ax.set_ylabel('Importance')
        self.ax.set_title('Feature Importances')

        # Embed the Matplotlib plot in the PyQt application
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet('border-radius:10px;')

        self.drop_features_button = QPushButton("Drop Features")

        #self.drop_features_button.setEnabled(False)
        self.drop_features_button.enterEvent = self.highlight_features
        self.drop_features_button.leaveEvent = self.reset_colors
        self.drop_features_button.clicked.connect(self.drop_features)

        ##############      LAYOUT      ################################################
        seuil_layout = QVBoxLayout()
        label_seuil = QLabel("Sélectionez une valeur seuil pour la conservation des données les plus importantes")

        self.slider = QSlider()
        self.slider.setToolTip("Select the threshold of feature importance")
        self.slider.setStyleSheet(window_style)
        self.slider.setOrientation(Qt.Orientation.Vertical)
        self.slider.setMinimumWidth(40)
        self.slider.setMinimum(0)
        self.slider.setMaximum(199)
        self.slider.setValue(0)
        #self.slider.setTickInterval(10)
        self.slider.setSingleStep(1)
        #self.slider.setPageStep(10)
        self.slider.valueChanged.connect(self.pr)
        #self.slider.enterEvent = self.highlight_features
        #self.slider.leaveEvent = self.reset_colors

        seuil_layout.addWidget(label_seuil)
        #seuil_layout.addWidget(self.seuil_input)
        seuil_layout.addWidget(self.slider)

        self.drop_features_button.setMinimumSize(150,150)

        label = QLabel("Select the best features")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.adjustSize()
        font = QFont("Helvetica")
        font.setPointSize(15)
        font.setBold(True)
        label.setFont(font)

        self.seuil_label = QLabel("0.00")
        self.seuil_label.setFont(QFont("Helvetica", 15))
        self.seuil_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.seuil_label.setMinimumWidth(40)
        self.seuil_label.setMaximumWidth(40)
        self.seuil_label.setStyleSheet(window_style)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 20, 30, 20)
        canvas_layout = QHBoxLayout()
        canvas_layout.setContentsMargins(0, 0, 0, 0)
        slider_layout = QVBoxLayout()

        slider_layout.addWidget(self.seuil_label)
        slider_layout.addWidget(self.slider)
        slider_layout.setContentsMargins(0, 10, 0, 0)
        slider_layout_container = QWidget()
        slider_layout_container.setStyleSheet('background-color: white; border-radius:10px;')
        slider_layout_container.setMaximumWidth(50)
        slider_layout_container.setLayout(slider_layout)
        slider_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        canvas_layout.addWidget(self.canvas)
        canvas_layout.addWidget(slider_layout_container)

        main_layout.addWidget(label)
        main_layout.addLayout(canvas_layout)
        #main_layout.addLayout(seuil_layout)
        #main_layout.addWidget(self.drop_features_button)

        next_step_bar.hide_status()

    def enable_drop_features_button(self):
        self.drop_features_button.setEnabled(True)
        self.drop_features_button.enterEvent = self.highlight_features
        self.drop_features_button.leaveEvent = self.reset_colors

    def print_seuil(self):
        #self.seuil_value = float(self.seuil)
        if self.seuil_line:  # Vérifiez si une ligne précédente existe
            self.seuil_line.remove()  # Supprimez la ligne précédente
        self.seuil_line = self.ax.axhline(y=self.seuil, color='r', linestyle='-')  # Ajoutez une nouvelle ligne
        self.canvas.draw()

    def drop_features(self):
        #self.save_seuil()
        if self.seuil != "":
            try:
                name_features_to_del = self.feature_importance_df[self.feature_importance_df['Importance'] <= self.seuil][
                    'Feature'].tolist()
                self.index_features_to_del = [list(self.dataframe_columns).index(i) for i in name_features_to_del]
                self.index_features_to_del.sort(reverse=True)
                print("Voila les features à supprimer", name_features_to_del, self.index_features_to_del)
                self.print_seuil()
                self.drop_features_button.setEnabled(False)

            except Exception as e:
                print(f"exeption in drop features: {e}")

    def highlight_features(self, event):
        #self.save_seuil()
        for i, importance in enumerate(self.feature_importance_df['Importance']):
            if importance < self.seuil:
                self.ax.patches[i].set_facecolor('r')
        self.canvas.draw()

    def reset_colors(self, event):
        for patch in self.ax.patches:
            patch.set_facecolor('b')
        self.canvas.draw()

    '''
    def save_seuil(self):
        #self.seuil = self.seuil_input.text()
        seuil_correct = ""

        for i in self.seuil:
            if i == ",":
                seuil_correct += "."
            else:
                seuil_correct += i

        if seuil_correct == "":
            self.seuil = 0
        else:
            self.seuil = float(seuil_correct)

        # Sauvegardez la valeur du seuil ici
        print("Valeur du seuil sauvegardée :", self.seuil)'''

    def highlight(self):
        for i, importance in enumerate(self.feature_importance_df['Importance']):
            if importance < self.seuil:
                self.ax.patches[i].set_facecolor('r')
        self.canvas.draw()

    def reset(self):
        for patch in self.ax.patches:
            patch.set_facecolor('b')
        self.canvas.draw()

    def pr(self):
        self.reset()
        importance = round(float(self.max_importance*self.slider.value()/200), 3)
        self.seuil = importance
        self.seuil_label.setText(str(importance)[:-1])
        self.print_seuil()
        self.highlight()


from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QDoubleValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QApplication
import pandas as pd
from sklearn.feature_selection import mutual_info_classif
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class FenData(QWidget):
    def __init__(self, dataframe_columns, dataframe_splited, next_step_bar, j_in=None):
        super().__init__()
        next_step_bar.show_status("Calculating info classifier")
        QApplication.processEvents()

        self.j = j_in
        self.seuil_value = None
        self.seuil_line = None
        self.seuil_input = QLineEdit()
        self.seuil_input.setPlaceholderText("Valeur du seuil")

        self.index_features_to_del = None

        validator = QDoubleValidator(0.0, 1.0, 2)  # 2 décimales
        self.seuil_input.setValidator(validator)

        self.dataframe_splited = dataframe_splited

        clf = mutual_info_classif(self.dataframe_splited[0], self.dataframe_splited[2])

        self.dataframe_columns = list(dataframe_columns)
        self.dataframe_columns = dataframe_columns[:-1]

        self.feature_importance_df = pd.DataFrame({'Feature': self.dataframe_columns, 'Importance': clf})
        self.feature_importance_df = self.feature_importance_df.sort_values(by='Importance', ascending=False)

        # Display the result
        print("Feature Importances:")
        print(self.feature_importance_df)

        # Plot the bar chart
        self.figure, self.ax = plt.subplots()
        self.ax.bar(self.feature_importance_df['Feature'], self.feature_importance_df['Importance'], color="blue")
        self.ax.set_ylabel('Importance')
        self.ax.set_title('Feature Importances')

        # Embed the Matplotlib plot in the PyQt application
        self.canvas = FigureCanvas(self.figure)

        self.drop_features_button = QPushButton("Drop Features")

        #self.drop_features_button.setEnabled(False)
        self.drop_features_button.enterEvent = self.highlight_features
        self.drop_features_button.leaveEvent = self.reset_colors
        self.drop_features_button.clicked.connect(self.drop_features)

        ##############      LAYOUT      ################################################
        seuil_layout = QVBoxLayout()
        label_seuil = QLabel("Sélectionez une valeur seuil pour la conservation des données les plus importantes")

        seuil_layout.addWidget(label_seuil)
        seuil_layout.addWidget(self.seuil_input)

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

        next_step_bar.hide_status()

    def enable_drop_features_button(self):
        self.drop_features_button.setEnabled(True)
        self.drop_features_button.enterEvent = self.highlight_features
        self.drop_features_button.leaveEvent = self.reset_colors

    def print_seuil(self):
        self.seuil_value = float(self.seuil)
        if self.seuil_line:  # Vérifiez si une ligne précédente existe
            self.seuil_line.remove()  # Supprimez la ligne précédente
        self.seuil_line = self.ax.axhline(y=self.seuil, color='r', linestyle='-')  # Ajoutez une nouvelle ligne
        self.canvas.draw()

    def drop_features(self):
        self.save_seuil()
        if self.seuil != "":
            try:
                name_features_to_del = self.feature_importance_df[self.feature_importance_df['Importance'] <= self.seuil][
                    'Feature'].tolist()
                self.index_features_to_del = [list(self.dataframe_columns).index(i) for i in name_features_to_del]
                self.index_features_to_del.sort(reverse=True)
                print("Voila les features à supprimer", name_features_to_del, self.index_features_to_del)
                self.print_seuil()
                self.drop_features_button.setEnabled(False)

            except Exception as e:
                print(f"exeption in drop features: {e}")

    def highlight_features(self, event):
        self.save_seuil()
        for i, importance in enumerate(self.feature_importance_df['Importance']):
            if importance < self.seuil:
                self.ax.patches[i].set_facecolor('r')
        self.canvas.draw()

    def reset_colors(self, event):
        for patch in self.ax.patches:
            patch.set_facecolor('b')
        self.canvas.draw()

    def save_seuil(self):
        self.seuil = self.seuil_input.text()
        seuil_correct = ""

        for i in self.seuil:
            if i == ",":
                seuil_correct += "."
            else:
                seuil_correct += i

        if seuil_correct == "":
            self.seuil = 0
        else:
            self.seuil = float(seuil_correct)

        # Sauvegardez la valeur du seuil ici
        print("Valeur du seuil sauvegardée :", self.seuil)
