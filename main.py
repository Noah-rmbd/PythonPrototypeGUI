from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from pages.page_1 import CPage1
from pages.page2 import Page2
from pages.page_3 import CPage3
from components.navigation_bar import NavBar

import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application")
        self.setWindowIcon(QIcon("icon.png"))

        self.setMaximumSize(1080,720)
        self.setMinimumSize(540,360)
        self.setGeometry(200,100,1080,720)

        window_style = (
            'background-color:white'
        )
        self.setStyleSheet(window_style)

        #The window (main_container) is composed of the nav bar and the content (main_content)
        main_container = QHBoxLayout()

        self.bar = NavBar(self)
        self.stacked_pages()
        self.bar.btn.clicked.connect(self.switch_pages)
        self.bar.btn2.clicked.connect(self.switch_pages)
        self.bar.btn3.clicked.connect(self.switch_pages)

        main_container.addLayout(self.bar)
        main_container.addLayout(self.stacked_pages)

        self.switch_pages()
        self.setLayout(main_container)

    def stacked_pages(self):
        self.stacked_pages = QStackedLayout()

        self.page1 = CPage1(self)

        self.page2 = Page2(self)

        self.page3 = CPage3(self)

        self.stacked_pages.addWidget(self.page1)
        self.stacked_pages.addWidget(self.page2)
        self.stacked_pages.addWidget(self.page3)

    def switch_pages(self):
        self.stacked_pages.setCurrentIndex(self.bar.menu_nbr-1)


app = QApplication([])
window = Window()
window.show()
sys.exit(app.exec())
