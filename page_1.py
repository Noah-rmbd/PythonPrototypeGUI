from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class CPage1(QWidget):
    def __init__(self, window):
        super().__init__()
        #Creating all the layouts
        self.widget_page1 = QWidget()
        page_layout = QVBoxLayout()
        title_layout = QVBoxLayout()
        edit_layout = QVBoxLayout()
        solution_layout = QVBoxLayout()
        form_layout = QHBoxLayout()

        #title widget
        title = QLabel("Page 1")
        title.setFont(QFont("Helvetica Neue", 20))
        title.setMaximumSize(100, 50)
        title.setGeometry(0, 0, 100, 50)

        #description widget
        description = QLabel("Chiffrez et déchiffrez une suite de caractère en utilisant le codage de fibonacci")
        description.setMaximumHeight(100)

        #description 2 widget
        description_2 = QLabel("Entrez votre chaîne de caractères ci-dessous : ")
        description_2.setMaximumHeight(80)
        self.text_edit = QLineEdit()

        #action buttons widgets
        self.convert_btn = QPushButton("Convert", window)
        encrypt_btn = QRadioButton("Encrypt", window)
        decrypt_btn = QRadioButton("Decrypt", window)

        #description and result widgets
        description_3 = QLabel("Solution : ")
        description_3.setMaximumHeight(100)
        self.text_solution = QLabel("", window)
        self.text_solution.setMaximumHeight(50)
        self.convert_btn.clicked.connect(self.convert_text)

        #adding all the widgets to the different layouts
        title_layout.addWidget(title)
        title_layout.addWidget(description)
        edit_layout.addWidget(description_2)
        edit_layout.addWidget(self.text_edit)
        form_layout.addWidget(encrypt_btn)
        form_layout.addWidget(decrypt_btn)
        form_layout.addWidget(self.convert_btn)
        edit_layout.addLayout(form_layout)
        solution_layout.addWidget(description_3)
        solution_layout.addWidget(self.text_solution)

        #adding all the layouts to the page widget
        page_layout.addLayout(title_layout)
        page_layout.addLayout(edit_layout)
        page_layout.addLayout(solution_layout)
        self.widget_page1.setLayout(page_layout)

    def convert_text(self):
        text_input = self.text_edit.text()
        self.text_solution.setText(text_input)