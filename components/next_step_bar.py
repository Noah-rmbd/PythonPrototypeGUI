from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

class NextStepBar(QHBoxLayout):
    def __init__(self):
        super().__init__()

        next_btn_style = (
            'QPushButton::disabled{background-color : #e1e1e1; border:3px #e1e1e1}QPushButton::hover{background-color : #e1e1e1; border:1px solid #000000}QPushButton{background-color:#ffffff; border:1px solid #000000; color:black;}')
        self.next_button = QPushButton("Next step ->")
        self.prev_button = QPushButton("<- Prev step")

        self.next_button.setMinimumSize(100, 40)
        self.next_button.setStyleSheet(next_btn_style)

        self.prev_button.setMinimumSize(100, 40)
        self.prev_button.setStyleSheet(next_btn_style)
        self.prev_button.hide()

        self.loading_bar = QProgressBar()
        self.loading_bar.setMaximumWidth(500)

        self.loading_label = QLabel()
        self.loading_label.setMaximumWidth(150)

        loading_layout = QHBoxLayout()
        buttons_layout = QHBoxLayout()

        self.loading_label.hide()
        self.loading_bar.hide()

        loading_layout.addWidget(self.loading_label)
        loading_layout.addWidget(self.loading_bar)
        buttons_layout.addWidget(self.prev_button)
        buttons_layout.addWidget(self.next_button)

        self.addLayout(loading_layout)
        self.addLayout(buttons_layout)
        loading_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

    def show_loading(self, label):
        self.loading_bar.show()
        self.loading_label.setText(label)
        self.loading_label.show()

    def hide_loading(self):
        self.loading_bar.hide()
        self.hide_status()

    def show_status(self, label):
        self.loading_label.setText(label)
        self.loading_label.show()
        QApplication.processEvents()

    def hide_status(self):
        self.loading_label.hide()