import pandas as pd
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import csv

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
        self.setToolTip("Drag and drop the file you would like to open")

        self.setMinimumHeight(150)
        self.btnpressed = (
            'background-color:blue; border:3px solid #8f8f91; border-radius: 6px; color:white;'
        )

        self.btnnormal = (
            'QPushButton::hover{background-color : #C4C4C4; border:3px #e1e1e1}QPushButton{background-color:white; border:3px solid white; border-radius: 10px; color:black;}')
        ##f0f0f0
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
            if self.file_path[-4:] == ".csv" or self.file_path[-5:] == ".xlsx" or self.file_path[-8:] == ".parquet":
                #print(self.file_path)
                text = self.file_path+"\nOr\nDrag a new file to change"
                self.setText(text)
                self.main_window.open_file_page(self.file_path)
            else:
                self.setText("Please drag a .csv, .xlsx or .parquet file\nDrag a new file")
                #print(self.file_path)


class HomePage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        # Creating all the layouts
        page_layout = QVBoxLayout()
        url_layout = QHBoxLayout()
        self.file_layout = QVBoxLayout()

        page_layout.setContentsMargins(30, 90, 30, 20)
        page_layout.setSpacing(40)

        # title widget
        title_font = QFont("Helvetica Neue", 40)
        title_font.setBold(True)
        title = QLabel("Welcome to Fault Predictor Pro 2024")
        title.setFont(title_font)
        title.setGeometry(0, 0, 5630, 3648)
        title.setMaximumWidth(1800)
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setAlignment(Qt.AlignmentFlag.AlignBottom)
        title.setContentsMargins(20, 0, 0, 15)
        title.setStyleSheet('color:white; border-radius:10px; border: 0px solid black; background-image:url("resources/home_image.png");background-repeat: no-repeat; background-position: center;')

        # WARNING:
        warning = QLabel("Warning, your dataset must be labelled")
        warning.setStyleSheet("font-weight: bold; color: red;")
        warning.setMaximumHeight(30)
        font_warning = QFont("Helvetica Neue", 20)
        warning.setFont(font_warning)
        warning.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # description widget
        description = QLabel("Upload the file you would like to open")
        description.setMaximumHeight(100)

        # edit_url widget
        self.edit_url = QLineEdit("")
        self.edit_url.setPlaceholderText("Or enter the url here")
        self.edit_url.setMaximumHeight(80)
        self.edit_url.returnPressed.connect(self.openwindow)

        # action buttons widgets
        open_files = QPushButton("Open in finder")
        open_files.clicked.connect(self.browsefiles)
        drag_and_drop = DragAndDrop(self.main_window)
        drag_and_drop.clicked.connect(self.browsefiles)

        # adding all the widgets to the different layouts
        action_layout = QVBoxLayout()
        action_layout.setSpacing(20)

        url_layout.addWidget(self.edit_url)
        url_layout.addWidget(open_files)

        #Recently opened
        self.recently_opened_layout = self.show_recently_opened()

        # Charger l'image avec QPixmap
        pixmap_poly = QPixmap("resources/logo_polytech.png")
        # on utilise r pour faire une chaîne brute et éviter les problèmes avec les backslash
        label_image_poly = QLabel()
        label_image_poly.setPixmap(pixmap_poly)
        label_image_poly.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_image_poly.setGeometry(0, 0, 150, 150)
        label_image_poly.setMaximumHeight(150)

        pixmap_laris = QPixmap("resources/logo_laris.png")

        label_image_laris = QLabel()
        label_image_laris.setPixmap(pixmap_laris)
        label_image_laris.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_image_laris.setGeometry(0, 0, 254, 152)
        label_image_laris.setMaximumHeight(152)

        self.bar = QProgressBar()

        image_layout = QHBoxLayout()
        ##########################################
        page_layout.addWidget(title)
        ##########################################

        action_layout.addWidget(drag_and_drop)
        #action_layout.addLayout(url_layout)
        action_layout.addWidget(warning)

        image_layout.addWidget(label_image_poly)
        image_layout.addWidget(label_image_laris)
        # adding all the layouts to the page widget

        page_layout.addLayout(action_layout)
        page_layout.addLayout(self.file_layout)
        self.file_layout.addWidget(self.bar)
        self.file_layout.addLayout(self.recently_opened_layout)
        self.bar.hide()
        page_layout.addLayout(image_layout)

        self.setLayout(page_layout)

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File', '/Users/noah-r/Downloads/', 'CSV, XLSX files (*.csv *.xlsx *.parquet)')
        if fname != ('',''):
            self.edit_url.setText(fname[0])
            self.openwindow()

    def openwindow(self):
        if os.path.isfile(self.edit_url.text()):
            if self.edit_url.text()[-4:] == ".csv" or self.edit_url.text()[-5:] == ".xlsx" or self.edit_url.text()[-8:] == ".parquet":
                self.main_window.open_file_page(self.edit_url.text())

    def show_recently_opened(self):
        self.recently_opened_df = pd.read_csv('resources/data.csv')
        num_rows = len(self.recently_opened_df)
        recently_opened_layout = QVBoxLayout()
        recently_opened_layout.setContentsMargins(0, 0, 0, 0)
        recently_opened_layout.setSpacing(0)

        if num_rows != 0:
            recently_opened_layout.addWidget(QFrame(frameShape=QFrame.Shape.HLine))
            recently_opened_layout.setSpacing(0)
            for i in range(num_rows):
                url = self.recently_opened_df['file.url'][i]
                date = str(self.recently_opened_df['date'][i])
                button_widget = self.create_link_button(url, date)
                recently_opened_layout.addWidget(button_widget)
                recently_opened_layout.addWidget(QFrame(frameShape=QFrame.Shape.HLine))

        return recently_opened_layout

    def create_link_button(self, url, date):
        button_widget = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)
        date_label = QLabel(date)
        button = QPushButton(url)
        button.clicked.connect(lambda: self.main_window.open_file_page(url))
        button.setMaximumHeight(20)
        date_label.setMaximumHeight(20)
        button_widget.setMaximumHeight(20)

        button_layout.addWidget(button)
        button_layout.addWidget(date_label)
        button_widget.setLayout(button_layout)
        button_widget.setStyleSheet('border: 0px solid black;')
        return button_widget

    def update_recently_opened(self):
        for i in reversed(range(self.recently_opened_layout.count())):
            self.recently_opened_layout.itemAt(i).widget().setParent(None)
        self.file_layout.removeItem(self.recently_opened_layout)
        self.recently_opened_layout = self.show_recently_opened()
        self.file_layout.insertLayout(self.file_layout.count()-2, self.recently_opened_layout)
        print('updating recently opened')

    def show_bar(self):
        self.bar.show()

    def hide_bar(self):
        self.bar.hide()
