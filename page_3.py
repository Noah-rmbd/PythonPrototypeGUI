from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import pandas as pd
import sys
import os

#Prochaine étape fusionner bouton et champ de drag and drop
#passer le drag and drop label en bouton
class DragAndDrop(QLabel):
    def __init__(self, page):
        super().__init__()
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("Drag a .csv file")
        widget_style_dark = (
            'background-color:#222222'
        )
        widget_style_white = (
            'background-color:#f0f0f0'
        )
        #self.setStyleSheet(widget_style)
        self.setStyleSheet(widget_style_white)


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
            file_path = event.mimeData().urls()[0].toLocalFile()
            event.accept()

            #print(event.mimeData().urls())
            if file_path[-4:]==".csv":
                print(file_path)
                text = file_path+"\nDrag a new file to change"
                self.setText(text)

            else:
                self.setText("Please drag a .csv file\nDrag a new file")

class CPage3(QWidget):
    def __init__(self, window):
        super().__init__()
        #Creating all the layouts
        page_layout = QVBoxLayout()
        title_layout = QVBoxLayout()
        add_file_layout = QHBoxLayout()
        file_layout = QVBoxLayout()

        #title widget
        title = QLabel("Page 3")
        title.setFont(QFont("Helvetica Neue", 20))
        title.setMaximumSize(100, 50)
        title.setGeometry(0, 0, 100, 50)

        #description widget
        description = QLabel("Upload the file you would like to open")
        description.setMaximumHeight(100)

        #edit_url widget
        self.edit_url = QLineEdit("")
        self.edit_url.setMaximumHeight(80)

        #action buttons widgets
        open_files = QPushButton("Open in finder")
        open_files.clicked.connect(self.browsefiles)
        drag_and_drop = DragAndDrop(self)


        #adding all the widgets to the different layouts
        title_layout.addWidget(title)
        title_layout.addWidget(description)
        add_file_layout.addWidget(self.edit_url)
        add_file_layout.addWidget(open_files)
        file_layout.addLayout(add_file_layout)
        file_layout.addWidget(drag_and_drop)

        #adding all the layouts to the page widget
        page_layout.addLayout(title_layout)
        page_layout.addLayout(file_layout)
        self.setLayout(page_layout)

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File', '/Users/noah-r/Downloads/', 'CSV files (*.csv)')
        self.edit_url.setText(fname[0])
        dataFrame = pd.read_csv(fname[0])
        print(dataFrame)