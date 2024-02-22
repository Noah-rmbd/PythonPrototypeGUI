from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from table_window import TableWindow
from file_window import FileWindow
import pandas as pd
import sys
import os

#Prochaine étape fusionner bouton et champ de drag and drop
#passer le drag and drop label en bouton
class DragAndDrop(QPushButton):
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
        self.setMinimumHeight(150)


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
        self.edit_url.returnPressed.connect(self.openwindow)

        #action buttons widgets
        open_files = QPushButton("Open in finder")
        open_files.clicked.connect(self.browsefiles)
        drag_and_drop = DragAndDrop(self)
        drag_and_drop.clicked.connect(self.browsefiles)


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
        fname = QFileDialog.getOpenFileName(self, 'Open File', '/Users/noah-r/Downloads/', 'CSV, XLSX files (*.csv *.xlsx)')
        if fname!=('','') :
            self.edit_url.setText(fname[0])
            self.openwindow()

    def openwindow(self):
        if os.path.isfile(self.edit_url.text()):
            if self.edit_url.text()[-4:]==".csv" or self.edit_url.text()[-5:]==".xlsx":
                self.file_window = FileWindow(self.edit_url.text())
                self.file_window.show()
