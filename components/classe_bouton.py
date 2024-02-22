from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtQuick import *
from PyQt6.QtQml import *
from time import *

class Bouton(QPushButton):
    def __init__(self):
        super().__init__()

        self.btnpressed = (
            'background-color:blue; border:3px solid #8f8f91; border-radius: 6px; color:white;'
        )

        self.btnnormal = ('QPushButton::hover{background-color : #e1e1e1; border:3px #e1e1e1}QPushButton{background-color:#f0f0f0; border:3px solid #f0f0f0; border-radius: 6px; color:black;}' )

        self.setStyleSheet(self.btnnormal)
        self.pressed.connect(self.btn_pressed)
        self.released.connect(self.btn_realeased)

    def btn_pressed(self):
        self.setStyleSheet(self.btnpressed)


    def btn_realeased(self):
        self.setStyleSheet(self.btnnormal)
