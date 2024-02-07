from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from table_window import TableWindow
from file_window import FileWindow
from classe_bouton import Bouton
import pandas as pd
import sys
import os

#Prochaine étape fusionner bouton et champ de drag and drop
#passer le drag and drop label en bouton

class DragAndDrop(Bouton):
    def __init__(self, page):
        super().__init__()
        self.setAcceptDrops(True)
        self.setText("Drag a .csv or .xlsx file")
        widget_style_dark = (
            'background-color:#222222'
        )
        widget_style_white = (
            'background-color:#f0f0f0'
        )
        #self.setStyleSheet(widget_style)
        self.setStyleSheet(widget_style_white)
        self.setGeometry(0,0,400,400)
        self.setMinimumHeight(400)


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
            if self.file_path[-4:]==".csv" or self.file_path[-5:]==".xlsx":
                print(self.file_path)
                text = self.file_path+"\nOr\nDrag a new file to change"
                self.setText(text)
                self.file_window = FileWindow(self.file_path)
                self.file_window.show()

            else:
                self.setText("Please drag a .csv or .xlsx file\nDrag a new file")
                print(self.file_path)



class MainPage(QWidget):
    def __init__(self, window):
        super().__init__()
        #Creating all the layouts
        page_layout = QVBoxLayout()
        url_layout = QHBoxLayout()
        file_layout = QVBoxLayout()

        #title widget
        title = QLabel("Accueil")
        title.setFont(QFont("Helvetica Neue", 40))
        title.setGeometry(0,0, 200, 200)

        #description widget
        description = QLabel("Upload the file you would like to open")
        description.setMaximumHeight(100)

        #edit_url widget
        self.edit_url = QLineEdit("")
        self.edit_url.setMaximumHeight(80)
        self.edit_url.returnPressed.connect(self.openwindow)

        #action buttons widgets
        open_files = QPushButton("Open in finder")
        open_files.clicked.connect(self.browsefiles)
        drag_and_drop = DragAndDrop(self)
        drag_and_drop.clicked.connect(self.browsefiles)


        #adding all the widgets to the different layouts



        url_layout.addWidget(self.edit_url)
        url_layout.addWidget(open_files)


    ##########################################
        page_layout.addWidget(title)
    ##########################################
        file_layout.addWidget(drag_and_drop)
        label = QLabel("Vous pouvez aussi copier l'url:")
        file_layout.addWidget(label)
        file_layout.addLayout(url_layout)

        #adding all the layouts to the page widget

        page_layout.addLayout(file_layout)
        self.setLayout(page_layout)

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File', '/Users/noah-r/Downloads/', 'CSV, XLSX files (*.csv *.xlsx)')
        if fname!=('','') :
            self.edit_url.setText(fname[0])
            self.openwindow()

    def openwindow(self):
        if os.path.isfile(self.edit_url.text()):
            if self.edit_url.text()[-4:]==".csv" or self.edit_url.text()[-5:]==".xlsx":
                self.file_window = FileWindow(self.edit_url.text())
                self.file_window.show()
