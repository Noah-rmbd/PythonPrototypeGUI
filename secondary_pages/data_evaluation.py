import numpy as np
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

import seaborn as sns
from tqdm import tqdm

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from sklearn import metrics
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
import time
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, cross_val_score
import timeit
from components.classe_bouton import *

class DataEvaluation(QWidget):
    def __init__(self, dataframe_splited, classifier, model_name, hyperparameters, splited, feature, pca, next_step_bar):
        super().__init__()
        main_layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        scroll_widget.setLayout(self.scroll_layout)
        scroll_area.setWidget(scroll_widget)
        next_step_bar.next_button.setText("Home Page")

        main_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setSpacing(0)

        label = QLabel(f"Proportion of testing data = {splited*100}%, Information gain treshold = {feature}, PCA treshold = {pca}")

        self.X_train = dataframe_splited[0]
        self.X_test = dataframe_splited[1]
        self.y_train = dataframe_splited[2]
        self.y_test = dataframe_splited[3]

        self.nbr_classifier = 0

        self.show_classifier(classifier, model_name, hyperparameters, "NaN")

        add_classifier_button = QPushButton("Add a new classifier")
        add_classifier_button.setMaximumWidth(180)
        add_classifier_button.clicked.connect(self.new_classifier)

        menu_layout = QHBoxLayout()
        menu_layout.setContentsMargins(20, 20, 20, 0)

        menu_layout.addWidget(label)
        menu_layout.addWidget(add_classifier_button)
        main_layout.addLayout(menu_layout)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def new_classifier(self):
        classifier = None

        try:
            self.new_classifier_window = QDialog()
            main_layout = QVBoxLayout()
            self.hyperpara_layout = QStackedLayout()

            model_label = QLabel("Select your classifier model : ")

            self.model_selection = QComboBox()
            self.model_selection.setPlaceholderText("Model")
            items = ["CART", "KNN", "Random Forest", "MLP"]
            self.model_selection.addItems(items)
            self.model_selection.currentIndexChanged.connect(self.switch_hyperparameters)

            placeholder_widget = QWidget()

            cart_widget = QWidget()
            cart_layout = QVBoxLayout()
            cart_layout.setContentsMargins(0, 0, 0, 0)
            self.cart_combo = QComboBox()
            cart_label = QLabel("CART Hyperparameters")

            cart_criterion_items = ['Gini (default)', 'Entropy', 'Log loss']
            self.cart_combo.addItems(cart_criterion_items)

            cart_layout.addWidget(cart_label)
            cart_layout.addWidget(self.cart_combo)
            cart_widget.setLayout(cart_layout)


            knn_widget = QWidget()
            knn_layout = QVBoxLayout()
            knn_layout.setContentsMargins(0, 0, 0, 0)
            knn_label = QLabel("KNN Hyperparameters")
            self.knn_input = QLineEdit()
            self.knn_input.setPlaceholderText("Enter the number of neighbors")
            validator = QIntValidator()
            self.knn_input.setValidator(validator)
            self.knn_input.textEdited.connect(self.enable_close_button)

            knn_widget.setLayout(knn_layout)
            knn_layout.addWidget(knn_label)
            knn_layout.addWidget(self.knn_input)

            random_f_widget = QWidget()
            random_f_layout = QVBoxLayout()
            random_f_layout.setContentsMargins(0, 0, 0, 0)
            random_f_label = QLabel("Random Forest Hyperparameters")
            self.random_f_input = QLineEdit()
            self.random_f_input.setPlaceholderText("Enter the number of trees")
            self.random_f_input.setValidator(validator)
            self.random_f_input.textEdited.connect(self.enable_close_button)

            random_f_layout.addWidget(random_f_label)
            random_f_layout.addWidget(self.random_f_input)
            random_f_widget.setLayout(random_f_layout)

            mlp_widget = QWidget()

            mlp_layout = QVBoxLayout()
            mlp_layout.setContentsMargins(0, 0, 0, 0)
            mlp_label = QLabel("MLP Hyperparameters")

####################### Valeurs initiales des hyperpara MLP #############################
            self.mlp_activation = "relu"
            self.solver_type = "adam"
            self.learning_rate = "constant"
######################################################################################"

            activation_label = QLabel("Activation function :")
            self.activation_combo = QComboBox()
            self.activation_combo.setPlaceholderText("Choose activation function")
            self.activation_combo.addItem("Rectified linear unit (default)")
            self.activation_combo.addItem("Identify")
            self.activation_combo.addItem("Logistic")
            self.activation_combo.addItem("Hyperbolic tan")
            self.activation_combo.currentIndexChanged.connect(self.MLP_criterion_update)

            solver_label = QLabel("Choose solver type:")
            self.solver_type_combo = QComboBox()
            self.solver_type_combo.setPlaceholderText("Choose solver type")
            self.solver_type_combo.addItem("adam (default)")
            self.solver_type_combo.addItem("sgd")
            self.solver_type_combo.currentIndexChanged.connect(self.MLP_criterion_update)

            learning_rate_label = QLabel("Choose learning rate")
            self.learning_rate_combo = QComboBox()
            self.learning_rate_combo.setPlaceholderText("Choose learning rate")
            self.learning_rate_combo.addItem("constant (default)")
            self.learning_rate_combo.addItem("invscaling")
            self.learning_rate_combo.addItem("adaptive")
            self.learning_rate_combo.currentIndexChanged.connect(self.MLP_criterion_update)

            mlp_layout.addWidget(mlp_label)
            mlp_layout.addWidget(activation_label)
            mlp_layout.addWidget(self.activation_combo)
            mlp_layout.addWidget(solver_label)
            mlp_layout.addWidget(self.solver_type_combo)
            mlp_layout.addWidget(learning_rate_label)
            mlp_layout.addWidget(self.learning_rate_combo)

            mlp_widget.setLayout(mlp_layout)

            self.close_button = QPushButton("Ok")
            self.close_button.clicked.connect(self.generate_classifier)
            self.close_button.setDisabled(True)
            #self.close_button.clicked.connect(lambda: self.show_classifier(self.classifier, "Text"))

            self.hyperpara_layout.addWidget(placeholder_widget)
            self.hyperpara_layout.addWidget(cart_widget)
            self.hyperpara_layout.addWidget(knn_widget)
            self.hyperpara_layout.addWidget(random_f_widget)
            self.hyperpara_layout.addWidget(mlp_widget)

            main_layout.addWidget(model_label)
            main_layout.addWidget(self.model_selection)
            main_layout.addWidget(QFrame(frameShape=QFrame.Shape.HLine))
            main_layout.addLayout(self.hyperpara_layout)
            main_layout.addWidget(self.close_button)
            self.new_classifier_window.setLayout(main_layout)
            self.new_classifier_window.setWindowTitle("Configure your new model")

            self.new_classifier_window.exec()
        except Exception as e:
            print(f"exception dans new classif: {e} ")

    def generate_classifier(self):
        try:
            if self.model_selection.currentText() == "CART":
                model = "CART"
                if self.cart_combo.currentText() == 'Gini (default)':
                    criterion = "gini"
                    hyperparameters = "criterion : gini"
                elif self.cart_combo.currentText() == 'Entropy':
                    criterion = "entropy"
                    hyperparameters = "criterion : entropy"

                elif self.cart_combo.currentText() == 'Log loss':
                    criterion = "log_loss"
                    hyperparameters = "criterion : log loss"

                self.classifier = DecisionTreeClassifier(criterion=criterion)


            elif self.model_selection.currentText() == "KNN":
                model = "KNN"
                neighbors = int(self.knn_input.text())
                hyperparameters = "number of neighbors = "+str(self.knn_input.text())
                self.classifier = KNeighborsClassifier(n_neighbors=neighbors)

            elif self.model_selection.currentText() == "Random Forest":
                model = "Random Forest"
                nb_trees = int(self.random_f_input.text())
                hyperparameters = "number of trees = " + str(self.random_f_input.text())
                self.classifier = RandomForestClassifier(n_estimators=nb_trees)

            elif self.model_selection.currentText() == "MLP":
                model = "MLP"
                hyperparameters = f"solver type = {self.solver_type}, activation function = {self.mlp_activation}, learning rate = {self.learning_rate}"
                self.classifier = MLPClassifier(solver=self.solver_type, activation=self.mlp_activation, learning_rate=self.learning_rate)


            print(self.model_selection.currentText(), self.cart_combo.currentText())

            time1 = timeit.default_timer()
            self.classifier.fit(self.X_train, self.y_train)
            time2 = timeit.default_timer()
            elapsed_time = time2-time1

            self.new_classifier_window.close()
            self.show_classifier(self.classifier, model, hyperparameters, elapsed_time)
        except Exception as e:
            print(f"exception dans generate_classifier: {e}")

    def switch_hyperparameters(self):
        try:
            if self.model_selection.currentText() == "CART":
                self.hyperpara_layout.setCurrentIndex(1)
                self.close_button.setDisabled(False)
            elif self.model_selection.currentText() == "KNN":
                self.hyperpara_layout.setCurrentIndex(2)
            elif self.model_selection.currentText() == "Random Forest":
                self.hyperpara_layout.setCurrentIndex(3)
            elif self.model_selection.currentText() == "MLP":
                self.hyperpara_layout.setCurrentIndex(4)
                self.close_button.setDisabled(False)
        except Exception as e:
            print(f"exception dans switch_hyperparameters: {e}")

    def enable_close_button(self):
        self.close_button.setDisabled(False)

    def show_classifier(self, classifier, classifier_name, hyperparameters, elapsed_time):
        classifier_widget = QWidget()
        classifier_layout = QVBoxLayout()
        menu_layout = QHBoxLayout()
        action_layout = QHBoxLayout()
        label_layout = QHBoxLayout()
        export_layout = QHBoxLayout()

        self.nbr_classifier += 1

        classifier_layout.setContentsMargins(20, 20, 20, 20)
        action_layout.setContentsMargins(0, 0, 0, 0)
        label_layout.setContentsMargins(0, 0, 0, 0)
        export_layout.setContentsMargins(0, 0, 0, 0)

        classifier_layout.setSpacing(20)
        classifier_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        classifier_widget.setMaximumHeight(300)

        #show_matrix_button = QPushButton("Show confusion matrix")
        show_matrix_button = QPushButton()
        show_matrix_button.setStyleSheet("background-image:url('resources/show.png'); background_color:white; border:1px solid #B6B6B6; border-radius:5px;background-repeat: no-repeat; background-position: center;")
        #show_matrix_button.setIcon(QIcon('resources/show.png'))
        show_matrix_button.setMaximumWidth(50)
        show_matrix_button.setMinimumWidth(40)
        show_matrix_button.setMaximumHeight(50)
        show_matrix_button.setMinimumHeight(40)
        show_matrix_button.clicked.connect(lambda: self.show_matrix(canva, show_matrix_button, classifier_widget))

        #delete_classifier_button = QPushButton("Delete")
        delete_classifier_button = QPushButton()
        delete_classifier_button.setStyleSheet("background-image:url('resources/delete.png'); background_color:white; border:1px solid #B6B6B6; border-radius:5px; background-repeat: no-repeat; background-position: center;")
        #delete_classifier_button.setMaximumWidth(80)
        delete_classifier_button.setMaximumWidth(50)
        delete_classifier_button.setMinimumWidth(40)
        delete_classifier_button.setMaximumHeight(50)
        delete_classifier_button.setMinimumHeight(40)
        #delete_classifier_button.setIcon(QIcon('resources/delete.png'))
        delete_classifier_button.clicked.connect(lambda: self.deleteWidget(classifier_widget))

        export_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        export_button = QPushButton("Export model")
        export_button.setMaximumWidth(180)
        export_button.setMinimumWidth(180)
        export_layout.addWidget(export_button)

        action_layout.addWidget(show_matrix_button)
        action_layout.addWidget(delete_classifier_button)

        model_label = QLabel(f"Classifier : {classifier_name}")
        model_font = QFont("Helvetica Neue", 20)
        model_label.setFont(model_font)
        hyperparameters_label = QLabel(hyperparameters)
        info_label = QLabel()

        predict = classifier.predict(self.X_test)
        F1_score = f1_score(self.y_test, predict, average='macro')

        info_label.setText(f"F1 Score : {F1_score}       Time to train : {elapsed_time} s")
        canva_and_stats = self.heat_confusion_matrix_test(self.y_test, predict)
        canva = canva_and_stats[0]
        stats_widget = canva_and_stats[1]
        canva.setMaximumWidth(1200)
        canva.setMinimumHeight(500)
        canva.hide()

        if self.nbr_classifier%2 == 1:
            canva.setStyleSheet("background-color:grey;")

        if self.nbr_classifier%2 == 0:
            classifier_widget.setStyleSheet("background-color:white;")
            #show_matrix_button.setStyleSheet(
            #"background-image:url('resources/show.png'); background_color:white; border:1px solid #B6B6B6; border-radius:5px;background-repeat: no-repeat; background-position: center;")
            #delete_classifier_button.setStyleSheet(
            #"background-image:url('resources/delete.png'); background_color:white; border:1px solid #B6B6B6; border-radius:5px; background-repeat: no-repeat; background-position: center;")
            export_button.setStyleSheet("border:1px solid #B6B6B6; border-radius: 4px;")

        label_layout.addWidget(model_label)
        label_layout.addWidget(hyperparameters_label)
        menu_layout.addLayout(label_layout)
        menu_layout.addLayout(action_layout)
        classifier_layout.addLayout(menu_layout)
        classifier_layout.addWidget(info_label)
        classifier_layout.addWidget(canva)
        classifier_layout.addWidget(stats_widget)
        classifier_layout.addLayout(export_layout)
        classifier_layout.addStretch(0)
        classifier_widget.setLayout(classifier_layout)
        self.scroll_layout.addWidget(classifier_widget)


    def show_matrix(self, canva, button, layout):
        if canva.isHidden():
            canva.show()
            layout.setMaximumHeight(1000)
            #button.setText("Hide confusion matrix")
            button.setStyleSheet("background-image:url('resources/hide.png');background_color:white; border:1px solid #B6B6B6; border-radius:5px; background-repeat: no-repeat; background-position: center;")
        else:
            canva.hide()
            layout.setMaximumHeight(300)
            #button.setText("Show confusion matrix")
            button.setStyleSheet("background-image:url('resources/show.png');background_color:white; border:1px solid #B6B6B6; border-radius:5px; background-repeat: no-repeat; background-position: center;")

    def deleteWidget(self, widget):
        widget.hide()
        self.scroll_layout.removeWidget(widget)

    def heat_confusion_matrix_test(self, y_actual, y_predicted):
        #Calculates the confusion matrix
        fig2, ax = plt.subplots(figsize=(16, 6))
        cm = confusion_matrix(y_actual, y_predicted)
        sns.heatmap(cm,
                    annot=True,
                    fmt='g',
                    xticklabels=np.unique(y_actual),
                    yticklabels=np.unique(y_actual)
                    )

        plt.ylabel('Actual', fontsize=13)
        plt.xlabel('Predicted', fontsize=13)

        plt.title('Testing Confusion Matrix', fontsize=17)

        # Ajouter la figure à la mise en page canvas_layout
        canvas = FigureCanvasQTAgg(fig2)

        #Calculates : accuracy, recall, and precision
        stats_widget = QTableWidget()
        name_columns = np.unique(y_actual)

        stats_widget.setColumnCount(len(name_columns))
        stats_widget.setRowCount(3)
        stats_widget.setHorizontalHeaderLabels(name_columns)
        stats_widget.setVerticalHeaderLabels(["Accuracy", "Precision", "Recall"])
        stats_widget.setMaximumHeight(113)
        stats_widget.setMinimumHeight(113)
        stats_widget.setContentsMargins(0, 0, 0, 0)

        cm_dimension = np.shape(cm)[0]

        for i in range(cm_dimension):
            tp = cm[i-1][i-1]
            tn = sum(np.diag(cm)) - tp
            fn = sum(cm[i-1]) - tp
            fp = sum(cm[:, i-1]) - tp

            print("Voila : TP=", tp, " ,TN =", tn, " ,FN = ", fn, " ,FP = ", fp)
            accuracy = (tp+tn)/(tp+fp+fn+tn)
            precision = tp/(tp+fp)
            recall = tp/(tp+fn)

            stats_widget.setItem(0, i, QTableWidgetItem(str(round(accuracy, 3))))
            stats_widget.setItem(1, i, QTableWidgetItem(str(round(precision, 3))))
            stats_widget.setItem(2, i, QTableWidgetItem(str(round(recall, 3))))

        result = (canvas, stats_widget)

        return result

    def MLP_criterion_update(self):

        try:
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
        except Exception as e:
            print(f"Fen Eval, exception dans mlp_criterion_update")
