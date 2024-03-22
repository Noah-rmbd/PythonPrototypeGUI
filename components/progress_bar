from PyQt6.QtWidgets import QGridLayout, QPushButton, QSizePolicy


class ProgressBar(QGridLayout):
    def __init__(self):
        super().__init__()

        self.step1_button = QPushButton("1  Visualization")
        self.step2_button = QPushButton("2  Modification")
        self.step2_button.setEnabled(False)
        self.step3_button = QPushButton("3  Analysis")
        self.step3_button.setEnabled(False)
        self.step4_button = QPushButton("4  Training")
        self.step4_button.setEnabled(False)
        self.step5_button = QPushButton("5  Testing")
        self.step5_button.setEnabled(False)

        self.btn_undone = (
            'QPushButton::disabled{background-color : #e1e1e1; border:3px #e1e1e1}QPushButton{background-color:#f0f0f0; border:1px solid #000000; color:black;}')
        self.btn_done = (
            'QPushButton::disabled{background-color : #e1e1e1; border:3px #e1e1e1}QPushButton{background-color:#ffffff; border:1px solid #000000; color:black;}')

        self.step1_button.setStyleSheet(self.btn_done)
        self.step2_button.setStyleSheet(self.btn_done)
        self.step3_button.setStyleSheet(self.btn_done)
        self.step4_button.setStyleSheet(self.btn_done)
        self.step5_button.setStyleSheet(self.btn_done)

        self.addWidget(self.step1_button, 0, 0)
        self.addWidget(self.step2_button, 0, 1)
        self.addWidget(self.step3_button, 0, 2)
        self.addWidget(self.step4_button, 0, 3)
        self.addWidget(self.step5_button, 0, 4)

        self.step1_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.step2_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.step3_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.step4_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.step5_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.step1_button.setMinimumHeight(40)
        self.step2_button.setMinimumHeight(40)
        self.step3_button.setMinimumHeight(40)
        self.step4_button.setMinimumHeight(40)
        self.step5_button.setMinimumHeight(40)

        self.step1_button.setMaximumHeight(60)
        self.step2_button.setMaximumHeight(60)
        self.step3_button.setMaximumHeight(60)
        self.step4_button.setMaximumHeight(60)
        self.step5_button.setMaximumHeight(60)

        self.setSpacing(0)

        # Définir les colonnes du layout pour qu'elles s'étirent
        self.setColumnStretch(0, 1)
        self.setColumnStretch(1, 1)
        self.setColumnStretch(2, 1)
        self.setColumnStretch(3, 1)
        self.setColumnStretch(4, 1)
