from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from page_1 import CPage1
from page_3 import CPage3
from navigation_bar import NavBar

import sys
from page2 import *
from main_page import *


class Window(QWidget):
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
        main_container = QHBoxLayout()
        self.page = MainPage(self)
        main_container.addWidget(self.page)
        self.setLayout(main_container)



app = QApplication([])
window = Window()
window.show()
sys.exit(app.exec())

