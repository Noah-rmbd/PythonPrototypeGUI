from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class CPage1(QWidget):
    def __init__(self, window):
        super().__init__()
        #Creating all the layouts
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
        self.encrypt_btn = QRadioButton("Encrypt", window)
        self.encrypt_btn.setChecked(True)
        self.decrypt_btn = QRadioButton("Decrypt", window)

        #description and result widgets
        description_3 = QLabel("Solution : ")
        description_3.setMaximumHeight(100)
        self.text_solution = QLineEdit("", window)
        self.text_solution.setMaximumHeight(50)
        copy = QPushButton("Add to clipboard")
        copy.setMaximumHeight(50)

        self.convert_btn.clicked.connect(self.convert_text)
        self.text_edit.returnPressed.connect(self.convert_text)
        copy.clicked.connect(self.add_clipboard)

        #adding all the widgets to the different layouts
        title_layout.addWidget(title)
        title_layout.addWidget(description)
        edit_layout.addWidget(description_2)
        edit_layout.addWidget(self.text_edit)
        form_layout.addWidget(self.encrypt_btn)
        form_layout.addWidget(self.decrypt_btn)
        form_layout.addWidget(self.convert_btn)
        edit_layout.addLayout(form_layout)
        solution_layout.addWidget(description_3)
        solution_layout.addWidget(self.text_solution)
        solution_layout.addWidget(copy)

        #adding all the layouts to the page widget
        page_layout.addLayout(title_layout)
        page_layout.addLayout(edit_layout)
        page_layout.addLayout(solution_layout)
        self.setLayout(page_layout)

    def convert_text(self):
        text_input = self.text_edit.text()
        if self.encrypt_btn.isChecked():
            solution = self.encrypt_text(text_input)
        elif self.decrypt_btn.isChecked():
            solution = self.decrypt_text(text_input)

        self.text_solution.setText(solution)
        print(self.text_solution.text())

    def add_clipboard(self):
        self.text_edit.copy()

    def fibonacci_rec_term(self, n, val1, val2):
        if n <= 1:
            return val2
        else:
            return self.fibonacci_rec_term(n - 1, val2, val1 + val2)

    def encrypt_character(self, n):
        ligne1 = []
        ligne2 = "1"
        i = 2

        # on crée la première ligne
        while (self.fibonacci_rec_term(i, 0, 1) <= n):
            ligne1.append(self.fibonacci_rec_term(i, 0, 1))
            i += 1

        # on crée la deuxième ligne
        for i in range(1, len(ligne1) + 1):  # on parcourt la première ligne à l'envers
            if ((n - ligne1[-i]) >= 0):  # on vérifie si la valeur analysée sur la ligne 1 peut être retirée à n
                n -= ligne1[-i]  # n=n-ligne[-i]
                ligne2 += "1"

            else:
                ligne2 += "0"

        return ligne2

    def encrypt_text(self, text):
        solution = ""
        for i in text:
            solution += str(self.encrypt_character(ord(i)))
        return solution

    def decrypt_text(self, text):
        decodage = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        solution = ""
        i = 1
        pos = 1
        tableau = []
        while (i < len(text)):
            # Permet d'ajouter le dernier caractère au tableau
            if (i == len(text) - 1):
                tableau.append(text[pos:i + 1])

            # On detecte la limite entre deux caractères
            if (text[i - 1] == "1" and text[i] == "1" and i != pos):
                # 1er cas : c'est la fin d'un caractere
                if (text[i + 1] == "1"):
                    tableau.append(text[pos:i])
                    i += 1
                    pos = i

                # 2eme cas : c'est le début d'un autre
                else:
                    tableau.append(text[pos:i - 1])
                    pos = i
                    i += 1
            else:
                i += 1

        # il faut obligatoirement inverser le texte de i
        for i in tableau:
            sum = 0
            newi = ""
            newi = i[::-1]
            for t in range(0, len(newi)):
                sum += int(newi[t]) * decodage[t]
            solution += chr(sum)
        return solution
