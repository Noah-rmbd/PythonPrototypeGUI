
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout,QApplication
import sys
class FenData(QWidget):
    def __init__(self,data_frame):
        super().__init__()
        #self.setWindowTitle("Graphique")
        #self.setGeometry(400, 150, 800, 600)

        # Load data from Excel file
        self.donnee = data_frame

##############      LAYOUT      ################################################
        layout = QVBoxLayout(self)
        label = QLabel("Analyse de données")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.adjustSize()
        font = QFont()
        font.setPointSize(30)
        label.setFont(font)
        layout.addWidget(label)

# app = QApplication([])
# window = FenData()
# window.show()
# sys.exit(app.exec())