import sys
import random
import time
import sqlite3
import pickle
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer
import pyqtgraph as pg

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QLabel()
        self.plot_widget = pg.PlotWidget()
        self.plot_data = []

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.plot_widget)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.data = []
        self.conn = sqlite3.connect('data.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS data
                             (petal_length REAL, petal_width REAL, sepal_length REAL, sepal_width REAL, prediction TEXT)''')

        with open('iris_model.pkl', 'rb') as f:
            self.model = pickle.load(f)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(100)



    def update_data(self):
        petal_length = random.uniform(1, 2)
        petal_width = random.uniform(0.1, 0.5)
        sepal_length = random.uniform(4.3, 8)
        sepal_width = random.uniform(2, 4.3)
        data = {
            'petal_length': petal_length,
            'petal_width': petal_width,
            'sepal_length': sepal_length,
            'sepal_width': sepal_width
        }
        self.data.append(data)
        self.label.setText(str(data))
        self.plot_data.append(petal_length)
        self.plot_widget.clear()
        self.plot_widget.plot(self.plot_data)
        prediction = self.model.predict(np.array([[petal_length, petal_width, sepal_length, sepal_width]]))[0]
        data['prediction'] = prediction
        print(data)

        if prediction == "Versicolor" :
            print ("EXPLOSION IMINNENTE, FLEUR FEUR")


        self.cursor.execute('''INSERT INTO data VALUES (?, ?, ?, ?)''',
                           (petal_length, petal_width, sepal_length, sepal_width))
        self.conn.commit()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
