from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
import sys
from PyQt6.QtGui import *
from secondary_pages.data_visualization import DataVisualization
from secondary_pages.data_modification import DataModification
from secondary_pages.data_analysis_tab import FenData
from secondary_pages.feature_PCA import FenPCA
from secondary_pages.IA_tab import IATab

from components.progress_bar import ProgressBar
from components.next_step_bar import NextStepBar

import pandas as pd
import numpy as np

class FileWindow(QWidget):
    def __init__(self, data_frame, loading_bar, normal_visualization):
        QWidget.__init__(self)

        layout = QVBoxLayout()
        self.progress_bar = ProgressBar()
        self.next_step_bar = NextStepBar()
        self.content_layout = QStackedLayout()

        self.next_step_bar.next_button.clicked.connect(self.switch_step)
        self.next_step_bar.prev_button.clicked.connect(self.previous_step)

        self.data_frame = data_frame
        self.normal_visualization = normal_visualization

        #list_steps = []
        self.nbr_step = 0

        self.data_visualization = DataVisualization(self.data_frame, loading_bar, normal_visualization)

        self.data_frame_splited = []
        self.percentage_splited = 20

        self.content_layout.addWidget(self.data_visualization)

        layout.addLayout(self.progress_bar)
        layout.addLayout(self.content_layout)
        layout.addLayout(self.next_step_bar)

        layout.setSpacing(0)
        self.setLayout(layout)

    def switch_step(self):
        if self.nbr_step == 0:
            self.data_modification = DataModification(self.data_frame, self.normal_visualization, self.next_step_bar)
            self.data_modification.split_button.clicked.connect(self.enable_button)
            self.data_modification.back_button.clicked.connect(self.disable_button)

            self.content_layout.addWidget(self.data_modification)

            self.nbr_step += 1
            self.progress_bar.step2_button.setEnabled(True)
            self.next_step_bar.next_button.setEnabled(False)
            self.content_layout.setCurrentIndex(self.nbr_step)

            self.next_step_bar.prev_button.show()

        elif self.nbr_step == 1:
            self.data_frame = self.data_modification.data_frame
            self.data_frame_splited = [self.data_modification.X_train, self.data_modification.X_test,
                                       self.data_modification.y_train, self.data_modification.y_test]
            self.percentage_splited = int(self.data_modification.split_combo.currentText()[:2]) / 100

            #modifier self.data_frame pour que la colonne label soit automatiquement à la fin

            self.data_analysis = FenData(self.data_frame.columns, self.data_frame_splited, self.next_step_bar)
            self.content_layout.addWidget(self.data_analysis)

            self.nbr_step += 1
            self.progress_bar.step3_button.setEnabled(True)
            self.content_layout.setCurrentIndex(self.nbr_step)

            print(self.percentage_splited)

        elif self.nbr_step == 2:
            if self.data_analysis.index_features_to_del is not None:
                self.index_features_to_del = self.data_analysis.index_features_to_del
                self.data_frame_splited[0] = np.delete(self.data_frame_splited[0], self.index_features_to_del, axis=1)
                self.data_frame_splited[1] = np.delete(self.data_frame_splited[1], self.index_features_to_del, axis=1)
            self.data_frame_splited_version_features_selection = self.data_frame_splited.copy()

            self.pca_selection = FenPCA(self.data_frame_splited)
            self.content_layout.addWidget(self.pca_selection)

            self.nbr_step += 1
            self.progress_bar.step4_button.setEnabled(True)
            self.content_layout.setCurrentIndex(self.nbr_step)

        elif self.nbr_step == 3:
            self.data_frame_splited[0] = self.pca_selection.X_train
            self.data_frame_splited[1] = self.pca_selection.X_test

            #self.data_frame_splited[0] = np.array(self.data_frame_splited[0])
            #self.data_frame_splited[2] = np.array(self.data_frame_splited[2])
            self.data_frame_splited[2] = self.data_frame_splited[2].reshape(-1, 1)
            self.data_frame_splited[3] = self.data_frame_splited[3].reshape(-1, 1)
            print("Array numpy x", self.data_frame_splited[0])
            print("Array numpy y", self.data_frame_splited[2])
            print("X", np.shape(self.data_frame_splited[0]))
            print("y", np.shape(self.data_frame_splited[2]))

            self.data_training = IATab(self.data_frame_splited)
            self.content_layout.addWidget(self.data_training)

            self.nbr_step += 1
            self.progress_bar.step5_button.setEnabled(True)
            self.content_layout.setCurrentIndex(self.nbr_step)


    def previous_step(self):
        if self.nbr_step == 1:
            self.content_layout.removeWidget(self.data_modification)

            self.progress_bar.step2_button.setEnabled(False)
            self.next_step_bar.next_button.setEnabled(True)
            self.next_step_bar.prev_button.hide()

            self.nbr_step -= 1
            self.content_layout.setCurrentIndex(self.nbr_step)

        elif self.nbr_step == 2:
            self.content_layout.removeWidget(self.data_analysis)
            self.progress_bar.step3_button.setEnabled(False)

            self.data_frame_splited[0] = self.data_modification.X_train
            self.data_frame_splited[1] = self.data_modification.X_test

            self.nbr_step -= 1
            self.content_layout.setCurrentIndex(self.nbr_step)

        elif self.nbr_step == 3:
            self.content_layout.removeWidget(self.pca_selection)
            self.progress_bar.step4_button.setEnabled(False)

            self.data_frame_splited[0] = self.data_frame_splited_version_features_selection[0].copy()
            self.data_frame_splited[1] = self.data_frame_splited_version_features_selection[1].copy()

            self.nbr_step -= 1
            self.content_layout.setCurrentIndex(self.nbr_step)

        elif self.nbr_step == 4:
            self.content_layout.removeWidget(self.data_training)
            self.progress_bar.step5_button.setEnabled(False)

            self.nbr_step -= 1
            self.content_layout.setCurrentIndex(self.nbr_step)

    def disable_button(self):
        self.next_step_bar.next_button.setEnabled(False)

    def enable_button(self):
        self.next_step_bar.next_button.setEnabled(True)
        #AJOUTER CODE QUI RECUPÈRE LA DATA SPLITÉE
