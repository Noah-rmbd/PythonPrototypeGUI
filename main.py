from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
import pandas as pd
import csv
from datetime import datetime
from pages.file_page import FileWindow
from pages.home_page import HomePage

import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application")
        self.setWindowIcon(QIcon("icon.png"))

        self.setMinimumSize(1065, 675)
        self.setGeometry(200, 100, 1080, 720)

        window_style = (
            'background-color:white'
        )
        #self.setStyleSheet(window_style)

        #The window (main_container) is composed of the nav bar and the content (main_content)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_container = QHBoxLayout(central_widget)
        main_container.setContentsMargins(0, 0, 0, 0)

        self.stacked_pages()
        main_container.addLayout(self.stacked_pages)

        file_menu = self.menuBar().addMenu("&File")
        self.home_action = QAction("Home page", self)
        new_action = QAction("Open", self)
        save_action = QAction("Save as", self)
        self.home_action.triggered.connect(self.next_home_page)
        new_action.triggered.connect(self.open_new_file)

        file_menu.addAction(self.home_action)
        file_menu.addAction(new_action)
        file_menu.addAction(save_action)
        save_action.setDisabled(True)
        self.home_action.setDisabled(True)

    def stacked_pages(self):
        self.stacked_pages = QStackedLayout()
        self.stacked_pages.setContentsMargins(0, 0, 0 ,0)
        self.home_page = HomePage(self)
        self.stacked_pages.addWidget(self.home_page)

    def open_home_page(self):
        self.stacked_pages.removeWidget(self.file_page)
        self.home_page.generate_background_image()
        self.data_frame = None
        self.home_action.setDisabled(True)

    def open_file_page(self, file_url):
        self.setStyleSheet("")
        first_opened = True
        num_rows = len(self.home_page.recently_opened_df)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M")
        for i in range(num_rows):
            if file_url in self.home_page.recently_opened_df['file.url'][i]:
                self.home_page.recently_opened_df.loc[i, 'date'] = dt_string
                self.home_page.recently_opened_df.to_csv('resources/data.csv', index=False)
                first_opened = False

        if first_opened:
            new_line = [[str(file_url), dt_string]]
            with open('resources/data.csv', 'a', newline='') as file:
                # création d'un objet writer pour écrire dans le fichier CSV
                writer = csv.writer(file)
                # écriture des noms des colonnes dans le fichier CSV
                writer.writerows(new_line)
            self.home_page.recently_opened_df = pd.read_csv("resources/data.csv")
        print("Voici le data_frame par la suite : ", self.home_page.recently_opened_df)

        if self.stacked_pages.currentIndex() == 1:
            self.stacked_pages.removeWidget(self.file_page)

        if file_url[-4:] == ".csv":
            self.data_frame = pd.read_csv(file_url)
        elif file_url[-8:] == ".parquet":
            self.data_frame = pd.read_parquet(file_url)
        else:
            self.data_frame = pd.read_excel(file_url)


        self.home_page.show_bar() #this function generates a loading bar
        self.file_page = FileWindow(self.data_frame, self.home_page.bar)
        self.is_last_page = False
        self.file_page.next_step_bar.next_button.clicked.connect(self.change_next_button)
        self.file_page.next_step_bar.prev_button.clicked.connect(self.change_prev_button)
        self.home_page.hide_bar()
        self.home_page.update_recently_opened()

        self.stacked_pages.addWidget(self.file_page)
        self.stacked_pages.setCurrentIndex(1)
        self.home_action.setDisabled(False)

    def change_next_button(self):
        if self.file_page.nbr_step == 6 and not self.is_last_page:
            self.file_page.next_step_bar.next_button.clicked.connect(self.next_home_page)
            self.is_last_page = True

    def change_prev_button(self):
        if self.file_page.nbr_step == 5 and self.is_last_page:
            self.file_page.next_step_bar.next_button.clicked.disconnect(self.next_home_page)
            self.is_last_page = False

    def next_home_page(self):
        #print(self.file_page.nbr_step)
        #if self.file_page.nbr_step == 6:
        quit_dialog = QDialog()
        quit_dialog.setMinimumSize(300, 150)
        quit_dialog.setMaximumSize(300, 150)
        quit_dialog.setWindowTitle("Quit the current configuration")
        font = QFont("Helvetica Neue", 17)
        label_dialog = QLabel("Are you sure to quit the page ?", quit_dialog)
        label_dialog.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_dialog.setFont(font)
        label2_dialog = QLabel("(you will lose your unsaved models)")
        label2_dialog.setAlignment(Qt.AlignmentFlag.AlignCenter)
        yes_button = QPushButton("Yes", quit_dialog)
        no_button = QPushButton("No", quit_dialog)
        yes_button.clicked.connect(quit_dialog.accept)
        yes_button.clicked.connect(self.open_home_page)
        no_button.clicked.connect(quit_dialog.reject)
        layout = QVBoxLayout()
        label_layout = QVBoxLayout()
        label_layout.addWidget(label_dialog)
        label_layout.addWidget(label2_dialog)
        label_layout.setContentsMargins(0, 0, 0, 0)
        label_layout.setSpacing(15)
        button_layout = QHBoxLayout()
        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)
        layout.addLayout(label_layout)
        layout.addStretch()
        layout.addLayout(button_layout)
        quit_dialog.setLayout(layout)

        quit_dialog.exec()

    def open_new_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File', '/Users/noah-r/Downloads/',
                                            'CSV, XLSX, Parquet files (*.csv *.xlsx *.parquet)')
        if fname != ('', ''):
            file_url = fname[0]
            self.open_file_page(file_url)


app = QApplication([])
window = Window()
window.show()
sys.exit(app.exec())
