from secondary_pages.photo import FenPhoto
from secondary_pages.graphs_tab import *
from components.classe_bouton import Bouton


class Page2(QWidget):
    def __init__(self,window):
        super().__init__()
        # on met un self car on va appeler ce gros widget dans le main

        title = QLabel("Ouverture de nouveaux onglets")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter) #gérer l'alignement du texte
        title.setFont(QFont("Helvetica Neue", 20))

        btn1 = Bouton()
        btn1.setText("Ouvrir une photo")

        btn1.setMinimumSize(100, 200)

        page2_layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        boutons_layout = QHBoxLayout()

        self.setLayout(page2_layout) #on met le layout de page 2 avec setLayout

        page2_layout.addLayout(title_layout)
        page2_layout.addLayout(boutons_layout) #on ajoute le bouton_layout avec addLayout

        title_layout.addWidget(title)

        boutons_layout.addWidget(btn1)

        btn1.clicked.connect(self.ouvrir_photo)

    def ouvrir_photo(self):
        fenetre_photo = FenPhoto()
        fenetre_photo.exec()

    def ouvrir_graph(self):
        self.fenetre_graph = FenGraph()
        self.fenetre_graph.show() #il faut ajouter self devant pour pas que la fenêtre se ferme automatiquement



