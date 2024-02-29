from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from pages.file_page import FileWindow
from pages.home_page import HomePage

import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application")
        self.setWindowIcon(QIcon("icon.png"))

        self.setMinimumSize(540,360)
        self.setGeometry(200,100,1080,720)

        window_style = (
            'background-color:white'
        )
        self.setStyleSheet(window_style)

        #The window (main_container) is composed of the nav bar and the content (main_content)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_container = QHBoxLayout(central_widget)

        self.stacked_pages()
        main_container.addLayout(self.stacked_pages)

        file_menu = self.menuBar().addMenu("&File")
        new_action = QAction("Open", self)
        save_action = QAction("Save as", self)
        new_action.triggered.connect(self.open_new_file)

        file_menu.addAction(new_action)
        file_menu.addAction(save_action)
        save_action.setDisabled(True)


    def stacked_pages(self):
        self.stacked_pages = QStackedLayout()

        self.home_page = HomePage(self)
        self.stacked_pages.addWidget(self.home_page)

    def open_file_page(self, file_url):
        self.setStyleSheet("")
        if self.stacked_pages.currentIndex() == 1:
            self.stacked_pages.removeWidget(self.file_page)
        self.file_page = FileWindow(file_url)
        self.stacked_pages.addWidget(self.file_page)
        self.stacked_pages.setCurrentIndex(1)

    def open_new_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File', '/Users/noah-r/Downloads/',
                                            'CSV, XLSX files (*.csv *.xlsx)')
        if fname != ('', ''):
            file_url = fname[0]
            self.open_file_page(file_url)

'''
    def createMenuBar(self):
        print("ok")
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
'''

app = QApplication([])
window = Window()
window.show()
sys.exit(app.exec())
