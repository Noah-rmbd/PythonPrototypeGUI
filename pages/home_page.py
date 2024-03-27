from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

import os
#Prochaine étape fusionner bouton et champ de drag and drop
#passer le drag and drop label en bouton


class DragAndDrop(QPushButton):
    #"main_window" argument is coming from "main.py" file, it is required in order to switch from home page to file page
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setAcceptDrops(True)
        self.setText("Drag a .csv or .xlsx file")

        self.setMinimumHeight(150)
        self.btnpressed = (
            'background-color:blue; border:3px solid #8f8f91; border-radius: 6px; color:white;'
        )

        self.btnnormal = (
            'QPushButton::hover{background-color : #C4C4C4; border:3px #e1e1e1}QPushButton{background-color:#f0f0f0; border:3px solid #f0f0f0; border-radius: 6px; color:black;}')

        self.setStyleSheet(self.btnnormal)
        self.pressed.connect(self.btn_pressed)
        self.released.connect(self.btn_realeased)

    def btn_pressed(self):
        self.setStyleSheet(self.btnpressed)

    def btn_realeased(self):
        self.setStyleSheet(self.btnnormal)


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            self.file_path = event.mimeData().urls()[0].toLocalFile()
            event.accept()

            #print(event.mimeData().urls())
            if self.file_path[-4:] == ".csv" or self.file_path[-5:] == ".xlsx":
                print(self.file_path)
                text = self.file_path+"\nOr\nDrag a new file to change"
                self.setText(text)
                self.main_window.open_file_page(self.file_path)
            else:
                self.setText("Please drag a .csv or .xlsx file\nDrag a new file")
                print(self.file_path)


class HomePage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        # Creating all the layouts
        page_layout = QVBoxLayout()
        url_layout = QHBoxLayout()
        self.file_layout = QVBoxLayout()

        # title widget
        title = QLabel("Accueil")
        title.setFont(QFont("Helvetica Neue", 40))
        title.setGeometry(0, 0, 200, 200)

        # description widget
        description = QLabel("Upload the file you would like to open")
        description.setMaximumHeight(100)

        # edit_url widget
        self.edit_url = QLineEdit("")
        self.edit_url.setMaximumHeight(80)
        self.edit_url.returnPressed.connect(self.openwindow)

        # action buttons widgets
        open_files = QPushButton("Open in finder")
        open_files.clicked.connect(self.browsefiles)
        drag_and_drop = DragAndDrop(self.main_window)
        drag_and_drop.clicked.connect(self.browsefiles)

        # adding all the widgets to the different layouts
        url_layout.addWidget(self.edit_url)
        url_layout.addWidget(open_files)

        # Charger l'image avec QPixmap
        pixmap_poly = QPixmap(
            r'logos_et_images/logo_polytech.png')  # on utilise r pour faire une chaîne brute et éviter les problèmes avec les backslash

        label_image_poly = QLabel()
        label_image_poly.setMaximumHeight(150)
        label_image_poly.setPixmap(pixmap_poly)

        pixmap_laris = QPixmap(
            r'logos_et_images/logo_laris.png')

        label_image_laris = QLabel()
        label_image_laris.setMaximumHeight(150)
        label_image_laris.setPixmap(pixmap_laris)

        image_layout = QHBoxLayout()
        ##########################################
        page_layout.addWidget(title)
        ##########################################
        self.file_layout.addWidget(drag_and_drop)
        label = QLabel("Vous pouvez aussi copier l'url:")
        self.file_layout.addWidget(label)
        self.file_layout.addLayout(url_layout)

        image_layout.addWidget(label_image_poly)
        image_layout.addWidget(label_image_laris)
        # adding all the layouts to the page widget
        page_layout.addLayout(self.file_layout)
        page_layout.addLayout(image_layout)

        self.setLayout(page_layout)

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File', '/Users/noah-r/Downloads/', 'CSV, XLSX files (*.csv *.xlsx)')
        if fname != ('',''):
            self.edit_url.setText(fname[0])
            self.openwindow()

    def openwindow(self):
        if os.path.isfile(self.edit_url.text()):
            if self.edit_url.text()[-4:] == ".csv" or self.edit_url.text()[-5:] == ".xlsx":
                self.main_window.open_file_page(self.edit_url.text())

    def large_file(self):
        self.bar = QProgressBar()
        self.file_layout.addWidget(self.bar)
