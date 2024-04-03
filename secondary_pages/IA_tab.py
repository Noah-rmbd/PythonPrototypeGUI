import numpy as np
from PyQt6.QtWidgets import *
#from secondary_pages.graphs_tab import FenGraph
#from secondary_pages.table_tab import TableTab
import pandas as pd
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from components.classe_bouton import *
from components.algos_predict import plot_algorithm_result

import pandas as pd
import sys


class IATab(QWidget):
    def __init__(self, dataframe_splited_in):
        super().__init__()
        self.dataframe = dataframe_splited_in #le dataframe est désormais décomposé en 4 parties: X_train, X_test, Y_train et Y_test, suite à la data_modification

        # self.dataframe = pd.read_csv(r'C:\Louis\Cours\Projet Peip2\PythonPrototypeGUI-main(3)\PythonPrototypeGUI-main\iris.csv')
        label = []

        #nrow = len(self.dataframe.index)
        # for i in range(nrow):
        #     label.append(
        #         self.dataframe.iat[i, -1])  # -1 permet d'aller dans la denière colonne (où se trouve les labels)

        # self.label_array = np.array(label)
        # matrice = self.dataframe.to_numpy()
        # self.matrice_sans_label = matrice[:, :-1]

        self.algo_type_combo = QComboBox(self)
        self.algo_type_combo.addItem("Choisissez un algorithme")
        self.algo_type_combo.addItem("CART")
        self.algo_type_combo.addItem("KNN")
        self.algo_type_combo.addItem("Random Forest")
        self.algo_type_combo.addItem("MLP")

        self.algo_type_combo.currentIndexChanged.connect(self.hyperpara_based_on_selection)

        self.update_hyperparameter_button = QPushButton("Changer les hyperparamètres")
        self.update_hyperparameter_button.clicked.connect(self.hyperpara_based_on_selection)

        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.plot_based_on_selection)
        #self.plot_button.setEnabled(False)

        label = QLabel()
        label.setText("Utiliser des algorithmes de machine learning")

        # Create a font with a larger size
        font = QFont()
        font.setPointSize(16)  # Set the desired font size

        # Set the font for the QLabel
        label.setFont(font)

        ############ Variables pour hyperparamètres #####################
        self.criterian_combo = QComboBox()
        self.criterian_combo.addItem("Gini (default)")
        self.criterian_combo.addItem("Entropie")
        self.criterian_combo.addItem("Log loss")

        self.criterian_combo.currentIndexChanged.connect(self.criterion_update)

        self.insert_neighbors_nb = None
        self.k_value_as_int = 5
        self.tree_value_as_int = 100
        self.insert_tree_number = None
        self.actual_criterion = "gini"
        self.mlp_activation = "relu"
        self.learning_rate = "constant"

        ##################################################################

        #### Fenêtres additionnelles #####
        self.fen_hyperpara_CART = QDialog()
        self.fen_hyperpara_RF = QDialog()
        self.fen_hyperpara_KNN = QDialog()
        self.fen_hyperpara_MLP = QDialog()
        #####################################

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(label)
        self.canvas_layout = QHBoxLayout()
        self.main_layout.addLayout(self.canvas_layout)
        ############## tableau métriques #########################
        # table_widget = QTableWidget()
        # self.setup_table(actual_labels, predicted_labels)
        # main_layout.addWidget(table_widget)
        #####################################################

        self.main_layout.addWidget(self.algo_type_combo)
        self.main_layout.addWidget(self.plot_button)
        self.main_layout.addWidget(self.update_hyperparameter_button)
        #test_size_layout = QHBoxLayout()
        #test_size_layout.addWidget(text_test_size)
        #test_size_layout.addWidget(self.test_size_box)
        #self.main_layout.addLayout(test_size_layout)
        # main_layout.addLayout(bouton_layout)

        self.setLayout(self.main_layout)

    def process_neighbors_input(self):
        k_value = self.insert_neighbors_nb.text()
        if k_value:
            # Assuming you want to convert the input to an integer
            self.k_value_as_int = int(k_value)
            # Use the value_as_int in your function or logic
            print(f"Entered value: {self.k_value_as_int}")

    def process_tree_input(self):
        print("Entered process_tree_input method")
        try:
            if self.insert_tree_number:
                tree_value = self.insert_tree_number.text()
                if tree_value:
                    # Assuming you want to convert the input to an integer
                    self.tree_value_as_int = int(tree_value)
                    # Use the value_as_int in your function or logic
                    print(f"Entered value: {self.tree_value_as_int}")
        except Exception as e:
            print(f"Exception in process_tree_input: {e}")

    def setup_table(self, actual_labels, predicted_labels):
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(['Metric', 'Value'])

        accuracy = metrics.accuracy_score(actual_labels, predicted_labels)
        precision = metrics.precision_score(actual_labels, predicted_labels)
        recall = metrics.recall_score(actual_labels, predicted_labels)
        f1_score = metrics.f1_score(actual_labels, predicted_labels)

        metrics_dict = {
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'F1 Score': f1_score
        }

        for row, (metric, value) in enumerate(metrics_dict.items()):
            self.table_widget.setItem(row, 0, QTableWidgetItem(metric))
            self.table_widget.setItem(row, 1, QTableWidgetItem(f"{value:.4f}"))

    def plot_cart(self):


        canvas = plot_algorithm_result("DecisionTreeClassifier", self.dataframe[0], self.dataframe[1],self.dataframe[2],self.dataframe[3],"Cart Algorithm",
                                       criterion_in= self.actual_criterion)
        for i in reversed(range(self.canvas_layout.count())):
            self.canvas_layout.itemAt(i).widget().setParent(None)

        self.canvas_layout.addWidget(canvas[0])
        self.canvas_layout.addWidget(canvas[1])


    def plot_KNN(self):
        # # Check if self.k_value_as_int is not None and greater than 0 before creating the classifier
        # if self.k_value_as_int is not None and self.k_value_as_int > 0:
        #     knn_classifier = KNeighborsClassifier(n_neighbors=self.k_value_as_int)
        # else:
        #     # Default to KNeighborsClassifier with default parameters
        #     knn_classifier = KNeighborsClassifier()

        canvas = plot_algorithm_result("KNeighborsClassifier", self.dataframe[0], self.dataframe[1],self.dataframe[2],self.dataframe[3], "KNN Algorithm",
                                       neighbors_nb= self.k_value_as_int)
        for i in reversed(range(self.canvas_layout.count())):
            self.canvas_layout.itemAt(i).widget().setParent(None)

        self.canvas_layout.addWidget(canvas[0])
        self.canvas_layout.addWidget(canvas[1])

    def plot_random_forest(self):
        canvas = plot_algorithm_result("RandomForestClassifier",self.dataframe[0], self.dataframe[1],self.dataframe[2],self.dataframe[3],"Random Forest Algorithm",
                                tree_nb=self.tree_value_as_int, criterion_in=self.actual_criterion)

        for i in reversed(range(self.canvas_layout.count())):
            self.canvas_layout.itemAt(i).widget().setParent(None)

        self.canvas_layout.addWidget(canvas[0])
        self.canvas_layout.addWidget(canvas[1])

    def plot_MLP(self):
        canvas = plot_algorithm_result("MLPClassifier", self.dataframe[0], self.dataframe[1],self.dataframe[2],self.dataframe[3], "MLP algorithm",
                              mlp_solver= self.solver_type, mlp_learning_rate= self.learning_rate, mlp_activation=self.mlp_activation)

        for i in reversed(range(self.canvas_layout.count())):
            self.canvas_layout.itemAt(i).widget().setParent(None)

        self.canvas_layout.addWidget(canvas[0])
        self.canvas_layout.addWidget(canvas[1])

    def plot_based_on_selection(self):

        try:
            if self.algo_type_combo.currentText() == "CART":
                self.plot_cart()

            elif self.algo_type_combo.currentText() == "KNN":
                self.plot_KNN()

            elif self.algo_type_combo.currentText() == "Random Forest":
                self.plot_random_forest()

            elif self.algo_type_combo.currentText() == "MLP":
                self.plot_MLP()

        except Exception as e:
            print(f"Exception: {e}")

    def hyperpara_based_on_selection(self):

        try:
            if self.algo_type_combo.currentText() == "CART":
                self.hyperpara_CART()

            elif self.algo_type_combo.currentText() == "KNN":
                self.hyperpara_KNN()

            elif self.algo_type_combo.currentText() == "Random Forest":
                self.hyperpara_RF()

            elif self.algo_type_combo.currentText() == "MLP":
                self.hyperpara_MLP()

        except Exception as e:
            print(f"Exception: {e}")

    def hyperpara_CART(self):

        self.fen_hyperpara_CART.setWindowTitle("CART Hyperparameter")

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.fen_hyperpara_CART.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.criterian_combo)
        layout.addWidget(ok_button)
        self.fen_hyperpara_CART.setLayout(layout)

        self.fen_hyperpara_CART.setGeometry(500, 200, 300, 300)
        self.fen_hyperpara_CART.exec()

    def hyperpara_KNN(self):

        self.fen_hyperpara_KNN.setWindowTitle("KNN Hyperparameter")

        self.insert_neighbors_nb = QLineEdit()
        self.insert_neighbors_nb.setPlaceholderText("Enter the number of neighbors you want")
        # Create an integer validator for the QLineEdit
        validator = QIntValidator()
        self.insert_neighbors_nb.setValidator(validator)
        # Connect the function to the editingFinished signal
        self.insert_neighbors_nb.editingFinished.connect(self.process_neighbors_input)

        ok_button = QPushButton("OK")
        # Connect the button's clicked signal to a function that closes the dialog
        ok_button.clicked.connect(self.fen_hyperpara_KNN.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.insert_neighbors_nb)
        layout.addWidget(ok_button)
        self.fen_hyperpara_KNN.setLayout(layout)
        self.fen_hyperpara_KNN.setGeometry(500, 200, 300, 300)
        self.fen_hyperpara_KNN.exec()

    def hyperpara_RF(self):
        # self.fen_hyperpara_RF = QDialog()
        self.fen_hyperpara_RF.setWindowTitle("RandomForest Hyperparameter")

        self.insert_tree_number = QLineEdit()
        self.insert_tree_number.setPlaceholderText("Enter the number of trees you want")
        # Create an integer validator for the QLineEdit
        validator = QIntValidator()
        self.insert_tree_number.setValidator(validator)
        # Connect the function to the editingFinished signal
        self.insert_tree_number.editingFinished.connect(self.process_tree_input)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.fen_hyperpara_RF.accept)  # accept ferme la fenêtre

        layout = QVBoxLayout()
        layout.addWidget(self.criterian_combo)
        layout.addWidget(self.insert_tree_number)
        layout.addWidget(ok_button)
        self.fen_hyperpara_RF.setLayout(layout)
        self.fen_hyperpara_RF.setGeometry(500, 200, 300, 300)
        self.criterian_combo.currentIndexChanged.connect(self.criterion_update)
        self.fen_hyperpara_RF.exec()

        print(self.actual_criterion)

    def hyperpara_MLP(self):
        self.fen_hyperpara_MLP.setWindowTitle("MLP Hyperparameter")

        activation_label =QLabel("Activation function :")
        self.activation_combo = QComboBox()
        self.activation_combo.setPlaceholderText("Choose activation function")
        self.activation_combo.addItem("Rectified linear unit (default)")
        self.activation_combo.addItem("Identify")
        self.activation_combo.addItem("Logistic")
        self.activation_combo.addItem("Hyperbolic tan")
        self.activation_combo.currentIndexChanged.connect(self.MLP_criterion_update)

        solver_label =QLabel("Choose solver type:")
        self.solver_type_combo = QComboBox()
        self.solver_type_combo.setPlaceholderText("Choose solver type")
        self.solver_type_combo.addItem("adam (default)")
        self.solver_type_combo.addItem("sgd")
        self.solver_type_combo.currentIndexChanged.connect(self.MLP_criterion_update)

        learning_rate_label = QLabel ("Choose learning rate")
        self.learning_rate_combo = QComboBox()
        self.learning_rate_combo.setPlaceholderText("Choose learning rate")
        self.learning_rate_combo.addItem("constant (default)")
        self.learning_rate_combo.addItem("invscaling")
        self.learning_rate_combo.addItem("adaptive")
        self.learning_rate_combo.currentIndexChanged.connect(self.MLP_criterion_update)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.fen_hyperpara_MLP.accept)

        layout = QVBoxLayout()
        layout.addWidget(activation_label)
        layout.addWidget(self.activation_combo)
        layout.addWidget(solver_label)
        layout.addWidget(self.solver_type_combo)
        layout.addWidget(learning_rate_label)
        layout.addWidget(self.learning_rate_combo)

        layout.addWidget(ok_button)

        self.fen_hyperpara_MLP.setLayout(layout)
        self.fen_hyperpara_MLP.setGeometry(500, 200, 300, 300)
        self.fen_hyperpara_MLP.exec()

    def process_neighbors_input(self):
        k_value = self.insert_neighbors_nb.text()
        if k_value:
            # Assuming you want to convert the input to an integer
            self.k_value_as_int = int(k_value)
            # Use the value_as_int in your function or logic
            print(f"Entered value: {self.k_value_as_int}")

    def process_tree_input(self):
        print("Entered process_tree_input method")
        try:
            if self.insert_tree_number:
                tree_value = self.insert_tree_number.text()
                if tree_value:
                    # Assuming you want to convert the input to an integer
                    self.tree_value_as_int = int(tree_value)
                    # Use the value_as_int in your function or logic
                    print(f"Entered value: {self.tree_value_as_int}")
        except Exception as e:
            print(f"Exception in process_tree_input: {e}")

    def criterion_update(self):
        if self.criterian_combo.currentText() == "Gini (default)":
            self.actual_criterion = "gini"

        elif self.criterian_combo.currentText() == "Entropie":
            self.actual_criterion = "entropy"

        elif self.criterian_combo.currentText() == "Log loss":
            self.actual_criterion = "log_loss"

        print(self.actual_criterion)

    def MLP_criterion_update(self):

        if self.activation_combo.currentText() =="Identity":
            self.mlp_activation = "identity"
        elif self.activation_combo.currentText() == "Logistic":
            self.mlp_activation = "logistic"
        elif self.activation_combo.currentText() == "Hyperbolic tan":
            self.mlp_activation = "tanh"
        elif self.activation_combo.currentText() == "Rectified linear unit (default)":
            self.mlp_activation = "relu"

        if self.solver_type_combo.currentText() == "adam (default)":
            self.solver_type = "adam"
        elif self.solver_type_combo.currentText() == "sgd":
            self.solver_type = "sgd"

        if self.learning_rate_combo.currentText() == "constant (default)":
            self.learning_rate = "constant"
        elif self.learning_rate_combo.currentText() == "invscaling":
            self.learning_rate = "invscaling"
        elif self.learning_rate_combo.currentText() == "adaptative":
            self.learning_rate = "adaptative"
