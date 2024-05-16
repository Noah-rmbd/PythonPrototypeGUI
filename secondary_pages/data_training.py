import time as tm

import numpy as np
from PyQt6.QtGui import QFont, QIntValidator
from PyQt6.QtCore import Qt

import seaborn as sns
from PyQt6.QtWidgets import QWidget, QVBoxLayout,QHBoxLayout,QPushButton,QLabel,QLayout,QComboBox,QDialog,QLineEdit


from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from sklearn import metrics
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, cross_val_score

from components.classe_bouton import *


class DataTraining(QWidget):
    def __init__(self, dataframe_splited, next_step_bar):

        self.predictions_train = None
        self.predictions_test = None
        try:
            super().__init__()
            self.X_train = dataframe_splited[0]
            self.X_test = dataframe_splited[1]
            self.y_train = dataframe_splited[2]
            self.y_test = dataframe_splited[3]

            print("X_train shape:", self.X_train.shape)
            print("X_test shape:", self.X_test.shape)
            print("y_train shape:", self.y_train.shape)
            print("y_test shape:", self.y_test.shape)

            self.algo_type_combo = QComboBox(self)
            self.algo_type_combo.addItem("Choisissez un algorithme")
            self.algo_type_combo.addItem("CART")
            self.algo_type_combo.addItem("KNN")
            self.algo_type_combo.addItem("Random Forest")
            self.algo_type_combo.addItem("MLP")

            self.algo_type_combo.currentIndexChanged.connect(self.hyperpara_based_on_selection)
            self.algo_type_combo.currentIndexChanged.connect(self.enable_train_button)

            self.update_hyperparameter_button = QPushButton("Changer les hyperparamètres")
            self.update_hyperparameter_button.clicked.connect(self.reset_hyperpara)
            self.update_hyperparameter_button.clicked.connect(self.hyperpara_based_on_selection)

            self.train_button = QPushButton("Train algorithm")
            self.train_button.setEnabled(False)
            self.train_button.clicked.connect(self.train_based_on_selection)
            self.train_button.clicked.connect(self.enable_plot_button)

            self.plot_button = QPushButton("Plot training confusion matrix")
            self.plot_button.setEnabled(False)

            label=QLabel("Algorithme actuellement entrainé:")
            self.current_algo_label = QLabel("Aucun")
            self.label_train_scores = QLabel("")

            font = QFont()
            font.setPointSize(16)  # Set the desired font size
            label.setFont(font)
            self.current_algo_label.setFont(font)
            self.label_train_scores.setFont(font)

            self.next_step_bar = next_step_bar
            self.next_step_bar.next_button.setEnabled(False)

            ############ Variables pour hyperparamètres #####################
            self.criterian_combo = QComboBox()
            self.criterian_combo.addItem("Gini (default)")
            self.criterian_combo.addItem("Entropie")
            self.criterian_combo.addItem("Log loss")

            self.criterian_combo.currentIndexChanged.connect(self.criterion_update)

            ############### POUR MLP: ##########################

            self.activation_combo = QComboBox()
            self.activation_combo.setPlaceholderText("Choose activation function")
            self.activation_combo.addItem("Rectified linear unit (default)")
            self.activation_combo.addItem("Identify")
            self.activation_combo.addItem("Logistic")
            self.activation_combo.addItem("Hyperbolic tan")
            self.activation_combo.currentIndexChanged.connect(self.MLP_criterion_update)

            self.solver_type_combo = QComboBox()
            self.solver_type_combo.setPlaceholderText("Choose solver type")
            self.solver_type_combo.addItem("adam (default)")
            self.solver_type_combo.addItem("sgd")
            self.solver_type_combo.currentIndexChanged.connect(self.MLP_criterion_update)

            self.learning_rate_combo = QComboBox()
            self.learning_rate_combo.setPlaceholderText("Choose learning rate")
            self.learning_rate_combo.addItem("constant (default)")
            self.learning_rate_combo.addItem("invscaling")
            self.learning_rate_combo.addItem("adaptive")
            self.learning_rate_combo.currentIndexChanged.connect(self.MLP_criterion_update)
            #initialisation des hyperparamètres

            self.algorithm_name = None
            self.hyperparameters = None

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


            #initialisation des champs d'insertion de texte
            self.insert_neighbors_nb = QLineEdit()
            self.insert_tree_number = QLineEdit()

            self.count_connection = 0

            # Create an integer validator for the QLineEdit
            validator = QIntValidator()
            self.insert_neighbors_nb.setValidator(validator)
            self.insert_neighbors_nb.editingFinished.connect(self.process_neighbors_input)
            self.ok_button_KNN = QPushButton("OK")
            self.ok_button_KNN.clicked.connect(self.fen_hyperpara_KNN.accept)


            self.insert_tree_number.setValidator(validator)
            self.insert_tree_number.editingFinished.connect(self.process_tree_input)
            self.ok_button_RF = QPushButton("OK")
            self.ok_button_RF.clicked.connect(self.fen_hyperpara_RF.accept)  # accept ferme la fenêtre

            #self.fig2, self.ax = plt.subplots(figsize=(16, 6))
            #####################################
            self.fit_time_label = QLabel()
            self.predict_train_time_label = QLabel()

            self.main_layout = QVBoxLayout()
            label_layout = QVBoxLayout()
            #label_layout.setAlignment(Qt.Alignment.AlignLeft)
            label_layout.addWidget(label)
            label_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            label_layout.addWidget(self.current_algo_label)
            label_layout.addWidget(self.fit_time_label)
            label_layout.addWidget(self.predict_train_time_label)

            self.main_layout.addLayout(label_layout)
            self.main_layout.addWidget(self.label_train_scores)
            self.canvas_layout = QHBoxLayout()
            self.main_layout.addLayout(self.canvas_layout)
            ############## tableau métriques #########################
            # table_widget = QTableWidget()
            # self.setup_table(actual_labels, predicted_labels)
            # main_layout.addWidget(table_widget)
            #####################################################

            self.main_layout.addWidget(self.algo_type_combo)
            self.main_layout.addWidget(self.train_button)
            self.main_layout.addWidget(self.plot_button)
            self.main_layout.addWidget(self.update_hyperparameter_button)
            #test_size_layout = QHBoxLayout()
            #test_size_layout.addWidget(text_test_size)
            #test_size_layout.addWidget(self.test_size_box)
            #self.main_layout.addLayout(test_size_layout)
            # main_layout.addLayout(bouton_layout)

            self.setLayout(self.main_layout)
        except Exception as e:
            print(f"Exception IA tab : {e}")
    def process_tree_input(self):
        print("Entered process_tree_input method")
        try:
            if self.insert_tree_number:
                tree_value = self.insert_tree_number.text()
                if tree_value:
                    # Assuming you want to convert the input to an integer
                    self.tree_value_as_int = int(tree_value)
                    # Use the value_as_int in your function or logic
                    print(f"Entered tree nb value: {self.tree_value_as_int}")
        except Exception as e:
            print(f"Exception in process_tree_input: {e}")

    '''
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
            self.table_widget.setItem(row, 1, QTableWidgetItem(f"{value:.4f}"))'''

    def train_cart(self):
        try:
            self.predictions_train, self.cross_validation = self.train_algo("DecisionTreeClassifier", self.X_train,
                                                                            self.X_test, self.y_train, self.y_test,
                                                                            "Cart Algorithm",
                                                                            criterion_in=self.actual_criterion)
            self.update_current_algorithm_label("Decision Tree", criterion=self.actual_criterion)
            #print("shape prediction:", self.predictions_train.shape)
        except Exception as e:
            print(f'Exception during training CART: {e}')
        return self.predictions_train, self.cross_validation

    def train_KNN(self):
        try:
            self.predictions_train, self.cross_validation = self.train_algo("KNeighborsClassifier", self.X_train,
                                                                            self.X_test, self.y_train, self.y_test,
                                                                            "KNN Algorithm",
                                                                            neighbors_nb=self.k_value_as_int)
            self.update_current_algorithm_label("K-Nearest Neighbors", neighbors=self.k_value_as_int)
        except Exception as e:
            print(f'Exception during training KNN: {e}')
        return self.predictions_train,self.cross_validation

    def train_random_forest(self):
        try:
            self.predictions_train, self.cross_validation = self.train_algo("RandomForestClassifier", self.X_train,
                                                                            self.X_test, self.y_train, self.y_test,
                                                                            "Random Forest Algorithm",
                                                                            tree_nb=self.tree_value_as_int,
                                                                            criterion_in=self.actual_criterion)
            self.update_current_algorithm_label("Random Forest", trees=self.tree_value_as_int,
                                                criterion=self.actual_criterion)
        except Exception as e:
            print(f'Exception during training Random Forest: {e}')
        return self.predictions_train, self.cross_validation

    def train_MLP(self):
        try:
            self.predictions_train, self.cross_validation = self.train_algo("MLPClassifier", self.X_train, self.X_test,
                                                                            self.y_train, self.y_test, "MLP Algorithm",
                                                                            mlp_solver=self.solver_type,
                                                                            mlp_learning_rate=self.learning_rate,
                                                                            mlp_activation=self.mlp_activation)

            self.update_current_algorithm_label("MLP", solver=self.solver_type, learning_rate=self.learning_rate,
                                                activation=self.mlp_activation)
        except Exception as e:
            print(f'Exception during training MLP: {e}')
        return self.predictions_train, self.cross_validation

    def train_based_on_selection(self):
        #try:
            if self.algo_type_combo.currentText() == "CART":
                self.train_cart()
                text = "Training accuracy : " + str(self.accuracy_train) + " - Cross validation accuracy : " + str(self.cross_validation)
                self.label_train_scores.setText(text)

            elif self.algo_type_combo.currentText() == "KNN":
                self.train_KNN()
                text = "Training accuracy : " + str(self.accuracy_train) + " - Cross validation accuracy : " + str(
                    self.cross_validation)
                self.label_train_scores.setText(text)

            elif self.algo_type_combo.currentText() == "Random Forest":
                self.train_random_forest()
                text = "Training accuracy : " + str(self.accuracy_train) + " - Cross validation accuracy : " + str(
                    self.cross_validation)
                self.label_train_scores.setText(text)

            elif self.algo_type_combo.currentText() == "MLP":
                self.train_MLP()
                text = "Training accuracy : " + str(self.accuracy_train) + " - Cross validation accuracy : " + str(
                    self.cross_validation)
                self.label_train_scores.setText(text)

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

        print("entererd hyperpara_KNN")
        self.fen_hyperpara_KNN.setWindowTitle("KNN Hyperparameter")
        #layout.removeWidget(self.insert_neighbors_nb)


        self.insert_neighbors_nb.clear()
        self.insert_neighbors_nb.setPlaceholderText("Enter the number of neighbors you want")


        layout_KNN = QVBoxLayout()
        layout_KNN.addWidget(self.insert_neighbors_nb)
        layout_KNN.addWidget(self.ok_button_KNN)
        self.fen_hyperpara_KNN.setLayout(layout_KNN)
        self.fen_hyperpara_KNN.setGeometry(500, 200, 300, 300)
        self.fen_hyperpara_KNN.exec()

    def hyperpara_RF(self):
        # self.fen_hyperpara_RF = QDialog()
        print("entererd hyperpara_RF")
        self.fen_hyperpara_RF.setWindowTitle("RandomForest Hyperparameter")

        self.insert_tree_number.clear()
        self.insert_tree_number.setPlaceholderText("Enter the number of trees you want")

        layout_RF = QVBoxLayout()
        layout_RF.addWidget(self.insert_tree_number)
        layout_RF.addWidget(self.ok_button_RF)

        self.fen_hyperpara_RF.setLayout(layout_RF)
        self.fen_hyperpara_RF.setGeometry(500, 200, 300, 300)
        self.criterian_combo.currentIndexChanged.connect(self.criterion_update)
        self.fen_hyperpara_RF.exec()

        print(self.actual_criterion)

    def hyperpara_MLP(self):

        #les combo box sont initialisées au début du fichier
        self.fen_hyperpara_MLP.setWindowTitle("MLP Hyperparameter")

        activation_label =QLabel("Activation function :")

        solver_label =QLabel("Choose solver type:")

        learning_rate_label = QLabel ("Choose learning rate")

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
        print("Entered process_neighbors_input method")
        self.k_value = self.insert_neighbors_nb.text()
        print("text k_value =", self.k_value)
        if self.k_value:
            # Assuming you want to convert the input to an integer
            self.k_value_as_int = int(self.k_value)
            # Use the value_as_int in your function or logic
            print(f"Entered value: {self.k_value_as_int}")

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
            print("choosed sgd")

        if self.learning_rate_combo.currentText() == "constant (default)":
            self.learning_rate = "constant"
        elif self.learning_rate_combo.currentText() == "invscaling":
            self.learning_rate = "invscaling"
        elif self.learning_rate_combo.currentText() == "adaptative":
            self.learning_rate = "adaptative"

    def reset_hyperpara(self):
        #self.insert_neighbors_nb = None
        self.k_value_as_int = 5

        self.tree_value_as_int = 100

        self.actual_criterion = "gini"

        self.mlp_activation = "relu"
        self.solver_type = "adam"
        self.learning_rate = "constant"

        print("les hyperparamètres ont étés réinitialisés")

    def train_algo (self, classifier,  X_train, X_test, y_train, y_test, algorithm_name,
                              criterion_in='gini',
                              neighbors_nb=5,
                              tree_nb=100,
                              mlp_solver='adam', mlp_learning_rate='constant', mlp_activation='relu'):
        try:
            print(f"algo used: {classifier}")
            print("classifier:", classifier)

            if classifier == "DecisionTreeClassifier":
                classifier_obj = DecisionTreeClassifier(criterion=criterion_in)  # instantiate the classifier
                print(f"\n criterion used: {criterion_in}")

            elif classifier == "KNeighborsClassifier":
                classifier_obj = KNeighborsClassifier(n_neighbors=neighbors_nb)  # instantiate the classifier
                print(f"neighbors number = {neighbors_nb}")

            elif classifier == "RandomForestClassifier":
                classifier_obj = RandomForestClassifier(n_estimators=tree_nb)  # instantiate the classifier
                print(f"number of trees = {tree_nb}")

            elif classifier == "MLPClassifier":
                classifier_obj = MLPClassifier(solver=mlp_solver, activation=mlp_activation,
                                               learning_rate=mlp_learning_rate)  # instantiate the classifier
                print(f"solver = {mlp_solver}\n")
                print(f"activation = {mlp_activation}\n")
                print(f"learning rate = {mlp_learning_rate}\n")
            else:
                raise ValueError(f"Unknown classifier type: {classifier}")

            start_fit_time = tm.time()
            classifier_obj.fit(X_train, y_train)
            end_fit_time = tm.time()
            execution_fit_time = end_fit_time - start_fit_time
            print("Temps d'entrainement de l'algorithme:", execution_fit_time, "secondes")
            self.fit_time_label.setText(f"Temps d'entrainement de l'algorithme: {str(execution_fit_time)} secondes")

            self.classifier = classifier_obj

            start_predict_train_time = tm.time()
            predictions_train = classifier_obj.predict(X_train)
            end_predict_train_time = tm.time()
            execution_predict_train_time = end_predict_train_time - start_predict_train_time
            print("Temps de prédiction des données d'entrainement:", execution_predict_train_time, "secondes")
            self.predict_train_time_label.setText(f"Temps de prédiction des données d'entrainement: {str(execution_predict_train_time)} secondes")

            self.accuracy_train = accuracy_score(y_train, predictions_train)
            #accuracy_test = accuracy_score(y_test, predictions_test)

            cross_val_accu = cross_val_score(classifier_obj,X_train,y_train)
            print(f"{algorithm_name} Accuracy train: {self.accuracy_train}")
            print(f"{algorithm_name} Cross validation accuracy: {cross_val_accu}")
        except Exception as e:
            print(f"exception dans train algo:{e}")
        return predictions_train, cross_val_accu

    def heat_confusion_matrix(self):
        print("entered conf matrix method")
        try:
            # canvas = self.heat_confusion_matrix(list(self.dataframe[2]), list(predictions))  # self.dataframe[2] est y_train, predictions sont les labels prédits par l'algorithme
            #canvas = self.heat_confusion_matrix(list(self.y_train), list(predictions))

            for i in reversed(range(self.canvas_layout.count())):
                self.canvas_layout.itemAt(i).widget().setParent(None)

            self.fig2, self.ax = plt.subplots(figsize=(16, 6))
            self.ax.clear()

            cm = confusion_matrix(self.y_train, self.predictions_train)
            sns.heatmap(cm,
                        annot=True,
                        fmt='g',
                        xticklabels=np.unique(self.y_train),
                        yticklabels=np.unique(self.y_train),
                        ax=self.ax,
                        cbar=True
                        )

            plt.ylabel('Prediction', fontsize=13)
            plt.xlabel('Actual', fontsize=13)

            plt.title('Training Confusion Matrix', fontsize=17)
            # Ajouter la figure à la mise en page canvas_layout
            canvas = FigureCanvasQTAgg(self.fig2)
            self.canvas_layout.addWidget(canvas)
            self.fig2.canvas.draw()
        except Exception as e:
            print(f"Exception during heatmap creation: {e}")
            #canvas = None

        return canvas


    def enable_plot_button(self):
        print("entered enable_plot_button")
        try:
            if self.predictions_test is None:
                print("no predictions_test")
            if self.predictions_train is not None:
                    self.plot_button.setEnabled(True)
                    self.next_step_bar.next_button.setEnabled(True)
                    print("plot_button enabled")
                    if self.count_connection ==0:
                        self.plot_button.clicked.connect(self.heat_confusion_matrix)
            self.count_connection+=1

        except Exception as e:
            print(f"exception dans enable_plot_button: {e}")

    def enable_train_button(self):
        if self.algo_type_combo.currentText !="Choisissez un algorithme":
            self.train_button.setEnabled(True)
        else:
            self.train_button.setEnabled(False)

    def update_current_algorithm_label(self, algorithm_name, **kwargs):
        hyperparameters = ", ".join([f"{key}={value}" for key, value in kwargs.items()])
        self.current_algo_label.setText(f"{algorithm_name} - Hyperparameters: {hyperparameters}")
        self.algorithm_name = algorithm_name
        self.hyperparameters = hyperparameters
