from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSlider, QLabel, QComboBox, QApplication
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class FenPCA(QWidget):
    def __init__(self, dataframe_splited):
        super().__init__()

        layout = QVBoxLayout(self)
        self.dataframe_splited = dataframe_splited

        # Séparer les caractéristiques des labels
        self.X_train = self.dataframe_splited[0]
        self.X_test = self.dataframe_splited[1]

        print(np.shape(self.X_train), np.shape(self.X_test))
        nb_components = np.shape(self.X_train)[1]
        self.pct_variance_to_keep = 1

        if nb_components != 1:
            # Appliquer l'algorithme PCA sur les caractéristiques
            pca = PCA()
            pca.fit(self.X_train)

            # Créer la figure matplotlib
            self.figure = plt.figure()
            self.ax = self.figure.add_subplot(111)
            self.ax.plot(np.cumsum(pca.explained_variance_ratio_))
            self.ax.set_xlabel("Nombre de composantes principales")
            self.ax.set_ylabel("Pourcentage d'information conservé")
            self.ax.set_title("Pourcentage d'information conservé en fonction du nombre de PC")

            # Ajouter la figure à un widget FigureCanvas
            self.canvas = FigureCanvas(self.figure)

            # Ajouter la combo box pour sélectionner le pourcentage d'information à conserver
            self.pca_combo = QComboBox()
            self.pca_combo.setPlaceholderText("Pourcentage d'information à conserver")
            self.pca_combo.addItem("0.99")
            self.pca_combo.addItem("0.95")
            self.pca_combo.addItem("0.9")
            self.pca_combo.addItem("0.85")
            self.pca_combo.addItem("0.8")
            self.pca_combo.currentIndexChanged.connect(self.enable_pca_button)


            # Ajouter le bouton pour appliquer la PCA

            self.pca_button = QPushButton("Apply PCA")
            self.pca_button.setEnabled(False)
            self.pca_button.clicked.connect(self.apply_pca)



            ########## LAYOUT ###################
            # Créer le layout vertical
            layout.addWidget(self.canvas)
            layout.addWidget(self.pca_combo)

            layout.addWidget(self.pca_button)

        else:
            no_pca_label = QLabel("There is only one component left, PCA step isn't needed")
            layout.addWidget(no_pca_label)

        self.setLayout(layout)

    def pr(self):
        print(self.slider.value())

    def enable_pca_button(self):
        self.pca_button.setEnabled(True)
    def apply_pca(self):
        try:
            # Récupérer le pourcentage d'information à conserver sélectionné dans la combo box
            self.pct_variance_to_keep = float(self.pca_combo.currentText())

            # Appliquer l'algorithme PCA sur les caractéristiques en conservant le pourcentage d'information sélectionné
            pca = PCA(n_components=self.pct_variance_to_keep)
            self.X_train = pca.fit_transform(self.dataframe_splited[0])
            self.X_test = pca.fit_transform(self.dataframe_splited[1])

            print(np.shape(self.X_train), np.shape(self.X_test))

            # Concaténer les composantes principales avec les labels
            #self.dataframe_pca = pd.concat([pd.DataFrame(X_pca), self.dataframe.iloc[:, -1]], axis=1)

            # Afficher les résultats
            #print("Dataframe après application de la PCA :")
            #print(self.dataframe_pca.head())

        except Exception as e:
            print(f'exeption in apply_pca : {e}')

