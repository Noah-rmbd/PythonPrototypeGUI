import sys
import random
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer
import pyqtgraph as pg

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.plot_widget = pg.PlotWidget()
        self.plot_data = []
        self.setCentralWidget(self.plot_widget)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)

    def update_data(self):
        data = random.uniform(0, 100)
        self.plot_data.append(data)
        self.plot_widget.clear()
        self.plot_widget.plot(self.plot_data)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
