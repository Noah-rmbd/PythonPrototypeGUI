from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class NavBar(QVBoxLayout):
    def __init__(self, window):
        super().__init__()

        title = QLabel("Menu", window)
        title.setFont(QFont("Helvetica Neue", 20))
        title.setMaximumSize(100, 50)
        title.setGeometry(0, 0, 100, 50)

        self.btn = NavButton("Button 1")
        self.btn2 = NavButton("Button 2")
        self.btn3 = NavButton("Button 3")

        self.menu_nbr = 1
        self.btn.setStyleSheet(self.btn.btn_clicked)

        self.btn.clicked.connect(self.clicked_1)
        self.btn2.clicked.connect(self.clicked_2)
        self.btn3.clicked.connect(self.clicked_3)


        self.addWidget(title)
        self.addWidget(self.btn)
        self.addWidget(self.btn2)
        self.addWidget(self.btn3)


    def clicked_1(self):
        self.btn.setStyleSheet(self.btn.btn_clicked)
        self.btn2.setStyleSheet(self.btn.btn_normal)
        self.btn3.setStyleSheet(self.btn.btn_normal)
        self.menu_nbr = 1

    def clicked_2(self):
        self.btn.setStyleSheet(self.btn.btn_normal)
        self.btn2.setStyleSheet(self.btn.btn_clicked)
        self.btn3.setStyleSheet(self.btn.btn_normal)
        self.menu_nbr = 2

    def clicked_3(self):
        self.btn.setStyleSheet(self.btn.btn_normal)
        self.btn2.setStyleSheet(self.btn.btn_normal)
        self.btn3.setStyleSheet(self.btn.btn_clicked)
        self.menu_nbr = 3

class NavButton(QPushButton):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setMaximumSize(100, 200)
        self.setMinimumSize(100, 80)
        self.btn_clicked = (
            'background-color:blue; border:3px solid #8f8f91; border-radius: 6px; color:white;'
        )
        self.btn_normal = (
            'QPushButton::hover{background-color : #e1e1e1; border:3px #e1e1e1}QPushButton{background-color:#f0f0f0; border:3px solid #f0f0f0; border-radius: 6px; color:black;}'
        )
        self.setStyleSheet(self.btn_normal)
