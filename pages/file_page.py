from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
import sys
from PyQt6.QtGui import *
from secondary_pages.data_visualization import DataVisualization
from secondary_pages.data_modification import DataModification
from secondary_pages.data_analysis_tab import FenData
from secondary_pages.IA_tab import IATab

from components.progress_bar import ProgressBar

import pandas as pd

class FileWindow(QWidget):
    def __init__(self, file_url):
        QWidget.__init__(self)

        layout = QVBoxLayout()
        self.progress_bar = ProgressBar()
        self.next_step_bar = QHBoxLayout()
        self.content_layout = QStackedLayout()

        next_btn_style = (
            'QPushButton::disabled{background-color : #e1e1e1; border:3px #e1e1e1}QPushButton::hover{background-color : #e1e1e1; border:1px solid #000000}QPushButton{background-color:#ffffff; border:1px solid #000000; color:black;}')
        self.next_button = QPushButton("Next step ->")
        self.prev_button = QPushButton("<- Prev step")

        self.next_button.setMinimumSize(100, 40)
        self.next_button.setStyleSheet(next_btn_style)
        self.next_button.clicked.connect(self.switch_step)

        self.prev_button.setMinimumSize(100, 40)
        self.prev_button.setStyleSheet(next_btn_style)
        self.prev_button.clicked.connect(self.previous_step)
        self.prev_button.hide()

        if file_url[-4:] == ".csv":
            self.data_frame = pd.read_csv(file_url)
        else:
            self.data_frame = pd.read_excel(file_url)

        #list_steps = []
        self.nbr_step = 0

        data_visualization = DataVisualization(self.data_frame)
        #list_steps.append(list_steps)

        self.data_frame_splited = []
        self.percentage_splited = 20

        self.content_layout.addWidget(data_visualization)

        self.next_step_bar.addWidget(self.prev_button)
        self.next_step_bar.addWidget(self.next_button)
        self.next_step_bar.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout.addLayout(self.progress_bar)
        layout.addLayout(self.content_layout)
        layout.addLayout(self.next_step_bar)

        layout.setSpacing(0)
        self.setLayout(layout)

    def switch_step(self):
        if self.nbr_step == 0:
            self.data_modification = DataModification(self.data_frame)
            self.data_modification.split_button.clicked.connect(self.enable_button)
            self.data_modification.back_button.clicked.connect(self.disable_button)

            self.content_layout.addWidget(self.data_modification)

            self.nbr_step += 1
            self.progress_bar.step2_button.setEnabled(True)
            self.next_button.setEnabled(False)
            self.content_layout.setCurrentIndex(self.nbr_step)

            self.prev_button.show()

        elif self.nbr_step == 1:
            self.data_frame = self.data_modification.data_frame
            self.data_frame_splited = [self.data_modification.X_train, self.data_modification.X_test,
                                       self.data_modification.y_train, self.data_modification.y_test]
            self.percentage_splited = int(self.data_modification.split_combo.currentText()[:2]) / 100

            self.data_analysis = FenData(self.data_frame)
            self.content_layout.addWidget(self.data_analysis)

            self.nbr_step += 1
            self.progress_bar.step3_button.setEnabled(True)
            self.content_layout.setCurrentIndex(self.nbr_step)

            print(self.percentage_splited)

        elif self.nbr_step == 2:
            self.data_training = IATab(self.data_frame)
            self.content_layout.addWidget(self.data_training)

            self.nbr_step += 1
            self.progress_bar.step4_button.setEnabled(True)
            self.content_layout.setCurrentIndex(self.nbr_step)


    def previous_step(self):
        if self.nbr_step == 1:
            self.content_layout.removeWidget(self.data_modification)

            self.progress_bar.step2_button.setEnabled(False)
            self.next_button.setEnabled(True)
            self.prev_button.hide()

        elif self.nbr_step == 2:
            self.content_layout.removeWidget(self.data_analysis)
            self.progress_bar.step3_button.setEnabled(False)

        elif self.nbr_step == 3:
            self.content_layout.removeWidget(self.data_training)
            self.progress_bar.step4_button.setEnabled(False)

        self.nbr_step -= 1
        self.content_layout.setCurrentIndex(self.nbr_step)

    def disable_button(self):
        self.next_button.setEnabled(False)

    def enable_button(self):
        self.next_button.setEnabled(True)
        #AJOUTER CODE QUI RECUPÈRE LA DATA SPLITÉE
