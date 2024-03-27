from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import pandas as pd
import time
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

        if file_url[-4:] == ".csv":
            self.data_frame = pd.read_csv(file_url)
        else:
            self.data_frame = pd.read_excel(file_url)

        if len(self.data_frame.index) >= 1000:
            #if the file is too large, home_page will get a loading bar to inform user
            question = QMessageBox.question(
                self,
                'Confirmation',
                "Souhaitez-vous l'intégralité des fonctionnalités ? (cette opération peut prendre du temps)",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if question == QMessageBox.StandardButton.Yes:
                self.home_page.large_file()
                self.file_page = FileWindow(self.data_frame, self.home_page.bar, True)
            else:
                self.home_page.large_file()
                self.file_page = FileWindow(self.data_frame, self.home_page.bar, False)

        else: #else there is no bar
            self.file_page = FileWindow(self.data_frame, None, True)

        self.stacked_pages.addWidget(self.file_page)
        self.stacked_pages.setCurrentIndex(1)

    def open_new_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File', '/Users/noah-r/Downloads/',
                                            'CSV, XLSX files (*.csv *.xlsx)')
        if fname != ('', ''):
            file_url = fname[0]
            self.open_file_page(file_url)


app = QApplication([])
window = Window()
window.show()
sys.exit(app.exec())
