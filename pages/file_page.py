from PyQt6.QtWidgets import *
from secondary_pages.data_visualization import DataVisualization
from secondary_pages.data_modification import DataModification
from secondary_pages.data_analysis_tab import FenData
from secondary_pages.feature_PCA import FenPCA
from secondary_pages.data_training import DataTraining
from secondary_pages.data_testing import DataTesting
from secondary_pages.data_evaluation import DataEvaluation

from components.progress_bar import ProgressBar
from components.next_step_bar import NextStepBar

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

class FileWindow(QWidget):
    def __init__(self, data_frame, loading_bar):
        QWidget.__init__(self)

        #Generates the page elements
        window_style = 'background-color:white; border-radius: 10px 0px 0px 0px;'

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.progress_bar = ProgressBar()
        self.next_step_bar = NextStepBar()
        self.content_layout = QStackedLayout()

        self.next_step_bar_container = QWidget()
        self.next_step_bar_container.setStyleSheet(window_style)
        self.next_step_bar_container.setLayout(self.next_step_bar)

        self.progress_bar_container = QWidget()
        self.progress_bar_container.setStyleSheet(window_style)
        self.progress_bar_container.setLayout(self.progress_bar)

        #self.next_step_bar.prev_button.setText("<- Homepage")
        #self.next_step_bar.prev_button.show()
        self.next_step_bar.next_button.clicked.connect(self.switch_step)
        self.next_step_bar.prev_button.clicked.connect(self.previous_step)

        #Generates the data structure
        self.data_frame = data_frame
        self.percentage_splited = None
        self.data_frame_splited = []
        self.data_frame_features_selection = []
        self.features_selection_percentage = None
        self.data_frame_pca = []
        self.pca_percentage = None
        self.trained_model = None

        self.nbr_step = 0

        self.data_visualization = DataVisualization(self.data_frame, loading_bar)

        self.content_layout.addWidget(self.data_visualization)

        layout.addWidget(self.progress_bar_container)
        layout.addLayout(self.content_layout)
        layout.addWidget(self.next_step_bar_container)

        layout.setSpacing(0)
        self.setLayout(layout)

    def switch_step(self):
        self.next_step_bar.next_button.clicked.disconnect(self.switch_step)
        self.next_step_bar.prev_button.clicked.disconnect(self.previous_step)
        if self.nbr_step == 0:
            self.data_modification = DataModification(self.data_frame, self.next_step_bar)
            self.data_modification.split_button.clicked.connect(self.enable_button)
            self.data_modification.back_button.clicked.connect(self.disable_button)

            self.content_layout.addWidget(self.data_modification)

            self.nbr_step += 1
            self.progress_bar.step2_button.setEnabled(True)
            self.next_step_bar.next_button.setEnabled(False)
            self.content_layout.setCurrentIndex(self.nbr_step)

            self.next_step_bar.prev_button.show()
            #self.next_step_bar.prev_button.setText("<- Prev step")
            print(self.nbr_step)

        elif self.nbr_step == 1:
            data_frame_columns = self.data_modification.data_frame.columns
            self.data_frame_splited = [self.data_modification.X_train, self.data_modification.X_test,
                                       self.data_modification.y_train, self.data_modification.y_test]
            self.data_frame_features_selection = self.data_frame_splited.copy()
            self.data_frame_pca = self.data_frame_splited.copy()
            self.percentage_splited = int(self.data_modification.split_combo.currentText()[:2]) / 100

            #modifier self.data_frame pour que la colonne label soit automatiquement à la fin

            self.data_analysis = FenData(data_frame_columns, self.data_frame_splited, self.next_step_bar)
            self.content_layout.addWidget(self.data_analysis)

            self.nbr_step += 1
            self.progress_bar.step3_button.setEnabled(True)
            self.content_layout.setCurrentIndex(self.nbr_step)

            print(self.percentage_splited)

        elif self.nbr_step == 2:
            #Saves new data
            if self.data_analysis.index_features_to_del is not None:
                self.index_features_to_del = self.data_analysis.index_features_to_del
                self.data_frame_features_selection[0] = np.delete(self.data_frame_splited[0], self.index_features_to_del, axis=1)
                self.data_frame_features_selection[1] = np.delete(self.data_frame_splited[1], self.index_features_to_del, axis=1)
            self.data_frame_pca = self.data_frame_features_selection.copy()
            self.features_selection_percentage = self.data_analysis.seuil

            #Generates the page
            self.pca_selection = FenPCA(self.data_frame_features_selection)
            self.content_layout.addWidget(self.pca_selection)

            self.nbr_step += 1
            self.progress_bar.step4_button.setEnabled(True)
            self.content_layout.setCurrentIndex(self.nbr_step)

        elif self.nbr_step == 3:
            #Saves new data
            pca = PCA(n_components=self.pca_selection.pct_variance_to_keep)
            pca.fit(self.data_frame_features_selection[0])
            self.data_frame_pca[0] = pca.fit_transform(self.data_frame_features_selection[0])
            self.data_frame_pca[1] = pca.fit_transform(self.data_frame_features_selection[1])
            self.pca_percentage = self.pca_selection.pct_variance_to_keep

            #Generates the page
            self.data_training = DataTraining(self.data_frame_pca, self.next_step_bar)
            self.content_layout.addWidget(self.data_training)

            self.nbr_step += 1
            self.progress_bar.step5_button.setEnabled(True)
            self.content_layout.setCurrentIndex(self.nbr_step)

        elif self.nbr_step == 4:
            self.classifier = self.data_training.classifier
            self.name_model = self.data_training.algorithm_name
            self.hyperparameters = self.data_training.hyperparameters

            self.data_testing = DataTesting(self.data_frame_pca, self.classifier, self.name_model, self.hyperparameters)
            self.content_layout.addWidget(self.data_testing)

            self.nbr_step += 1
            self.progress_bar.step6_button.setEnabled(True)
            self.content_layout.setCurrentIndex(self.nbr_step)

        elif self.nbr_step == 5:
            self.data_evaluation = DataEvaluation(self.data_frame_pca, self.classifier, self.name_model, self.hyperparameters, self.percentage_splited, self.features_selection_percentage, self.pca_percentage, self.next_step_bar)
            self.content_layout.addWidget(self.data_evaluation)

            self.nbr_step += 1
            self.progress_bar.step7_button.setEnabled(True)
            self.content_layout.setCurrentIndex(self.nbr_step)
        self.next_step_bar.next_button.clicked.connect(self.switch_step)
        self.next_step_bar.prev_button.clicked.connect(self.previous_step)


    def previous_step(self):
        self.next_step_bar.next_button.clicked.disconnect(self.switch_step)
        self.next_step_bar.prev_button.clicked.disconnect(self.previous_step)
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

            self.nbr_step -= 1
            self.content_layout.setCurrentIndex(self.nbr_step)

        elif self.nbr_step == 3:
            self.content_layout.removeWidget(self.pca_selection)
            self.progress_bar.step4_button.setEnabled(False)

            self.nbr_step -= 1
            self.content_layout.setCurrentIndex(self.nbr_step)

        elif self.nbr_step == 4:
            self.content_layout.removeWidget(self.data_training)
            self.progress_bar.step5_button.setEnabled(False)
            self.next_step_bar.next_button.setEnabled(True)

            self.nbr_step -= 1
            self.content_layout.setCurrentIndex(self.nbr_step)

        elif self.nbr_step == 5:
            self.content_layout.removeWidget(self.data_testing)
            self.next_step_bar.next_button.setText("Next Step ->")
            self.progress_bar.step6_button.setEnabled(False)

            self.nbr_step -= 1
            self.content_layout.setCurrentIndex(self.nbr_step)

        elif self.nbr_step == 6:
            self.content_layout.removeWidget(self.data_evaluation)
            self.progress_bar.step7_button.setEnabled(False)

            self.nbr_step -= 1
            self.content_layout.setCurrentIndex(self.nbr_step)
        self.next_step_bar.next_button.clicked.connect(self.switch_step)
        self.next_step_bar.prev_button.clicked.connect(self.previous_step)

    def disable_button(self):
        self.next_step_bar.next_button.setEnabled(False)

    def enable_button(self):
        self.next_step_bar.next_button.setEnabled(True)
