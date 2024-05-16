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

        self.seuil = 0
        self.seuil_line = None
        self.index_features_to_del = None

        ##Data manipulation
        self.dataframe_splited = dataframe_splited

        clf = mutual_info_classif(self.dataframe_splited[0], self.dataframe_splited[2])
        next_step_bar.hide_status()

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

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 20, 30, 20)
        self.setLayout(self.main_layout)
        self.generate_ui()

    def generate_ui(self):
        window_style = 'background-color:white'

        ##Page elements
        label = QLabel("Select the best features")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.adjustSize()
        font = QFont("Helvetica")
        font.setPointSize(15)
        font.setBold(True)
        label.setFont(font)

        self.slider = QSlider()
        self.slider.setToolTip("Select the threshold of feature importance")
        self.slider.setStyleSheet(window_style)
        self.slider.setOrientation(Qt.Orientation.Vertical)
        self.slider.setMinimumWidth(40)
        self.slider.setMinimum(0)
        self.slider.setMaximum(199)
        self.slider.setValue(0)
        self.slider.setSingleStep(1)
        self.slider.valueChanged.connect(self.slider_update)

        self.seuil_label = QLabel("0.00")
        self.seuil_label.setFont(QFont("Helvetica", 15))
        self.seuil_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.seuil_label.setMinimumWidth(40)
        self.seuil_label.setMaximumWidth(40)
        self.seuil_label.setStyleSheet(window_style)

        '''delete_button = QPushButton()
        delete_button.setMaximumWidth(40)
        delete_button.setMinimumWidth(40)
        delete_button.setMaximumHeight(60)
        delete_button.setMinimumHeight(60)
        delete_button.setStyleSheet("background-image:url(logos_et_images/delete-2.png); border-radius:10px; background-repeat: no-repeat; background-position: center;")
        delete_button.clicked.connect(self.drop_features)'''

        ##############      LAYOUT      ################################################
        seuil_layout = QVBoxLayout()
        label_seuil = QLabel("Sélectionez une valeur seuil pour la conservation des données les plus importantes")

        seuil_layout.addWidget(label_seuil)
        seuil_layout.addWidget(self.slider)

        canvas_layout = QHBoxLayout()
        canvas_layout.setContentsMargins(0, 0, 0, 0)
        slider_layout = QVBoxLayout()

        slider_layout.addWidget(self.seuil_label)
        slider_layout.addWidget(self.slider)
        #slider_layout.addWidget(delete_button)
        slider_layout.setContentsMargins(0, 10, 0, 0)
        slider_layout_container = QWidget()
        slider_layout_container.setStyleSheet('background-color: white; border-radius:10px;')
        slider_layout_container.setMaximumWidth(50)
        slider_layout_container.setLayout(slider_layout)
        slider_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        canvas_layout.addWidget(self.canvas)
        canvas_layout.addWidget(slider_layout_container)

        self.main_layout.addWidget(label)
        self.main_layout.addLayout(canvas_layout)


    def print_seuil(self):
        if self.seuil_line:  # Vérifiez si une ligne précédente existe
            self.seuil_line.remove()  # Supprimez la ligne précédente
        self.seuil_line = self.ax.axhline(y=self.seuil, color='r', linestyle='-')  # Ajoutez une nouvelle ligne
        self.canvas.draw()

    def drop_features(self):
        if self.seuil != "":
            try:
                name_features_to_del = self.feature_importance_df[self.feature_importance_df['Importance'] <= self.seuil][
                    'Feature'].tolist()
                self.index_features_to_del = [list(self.dataframe_columns).index(i) for i in name_features_to_del]
                self.index_features_to_del.sort(reverse=True)
                print("Voila les features à supprimer", name_features_to_del, self.index_features_to_del)
                self.print_seuil()

            except Exception as e:
                print(f"exeption in drop features: {e}")


    def highlight_features(self):
        for i, importance in enumerate(self.feature_importance_df['Importance']):
            if importance < self.seuil:
                self.ax.patches[i].set_facecolor('r')
        self.canvas.draw()

    def reset_colors(self):
        for patch in self.ax.patches:
            patch.set_facecolor('b')
        self.canvas.draw()

    def slider_update(self):
        self.reset_colors()
        importance = round(float(self.max_importance*self.slider.value()/200), 3)
        self.seuil = importance
        self.seuil_label.setText(str(importance)[:-1])
        self.print_seuil()
        self.drop_features()
        self.highlight_features()
