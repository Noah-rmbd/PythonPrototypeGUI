from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

import numpy as np
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier


def plot_algorithm_result(classifier,  X_train, X_test, y_train, y_test, algorithm_name,
                          criterion_in='gini',
                          neighbors_nb=5,
                          tree_nb=100,
                          mlp_solver='adam', mlp_learning_rate='constant', mlp_activation='relu'):

    print(f"algo used: {classifier}")
    print ("classifier:", classifier)

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
        classifier_obj = MLPClassifier(solver=mlp_solver, activation=mlp_activation, learning_rate=mlp_learning_rate)  # instantiate the classifier
        print(f"solver = {mlp_solver}\n")
        print(f"activation = {mlp_activation}\n")
        print(f"learning rate = {mlp_learning_rate}\n")
    else:
        raise ValueError(f"Unknown classifier type: {classifier}")

    classifier_obj.fit(X_train, y_train)
    predictions = classifier_obj.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    #print(f"{algorithm_name} Accuracy: {accuracy}")

    pca = PCA(n_components=2)
    X_train_pca = pca.fit_transform(X_train)

    noms_de_labels = np.unique(y_train)
    longueur = len(y_train)
    valeur_initiale = 0
    y_train_number = [valeur_initiale] * longueur

    n = 0
    for nom in noms_de_labels:
        for i in range(len(y_train_number)):
            if y_train[i] == nom:
                y_train_number[i] = n
        n += 1


    fig1, ax = plt.subplots(figsize=(16, 6))

    canvas1 = FigureCanvasQTAgg(fig1)
    plt.scatter(X_train_pca[:, 0], X_train_pca[:, 1], c=y_train_number, cmap='viridis', label='Actual Labels')

    predictions_pca = pca.transform(X_test)

    valeur_initiale = 0
    prediction_number = [valeur_initiale] * len(y_test)

    n = 0
    for nom in noms_de_labels:
        for i in range(len(prediction_number)):
            if predictions[i] == nom:
                prediction_number[i] = n
        n += 1

    plt.scatter(predictions_pca[:, 0], predictions_pca[:, 1], c=prediction_number, marker='x', cmap='viridis',
                label='Predicted Labels')

    plt.title(f'Actual and Predicted Labels with {algorithm_name}')
    plt.legend()

    canvas2 = heat_confusion_matrix(list(y_test), list(predictions))

    print(f"algo used: {classifier} \n")
    print("")
    return [canvas1, canvas2]


def heat_confusion_matrix(actual, predicted):
    #creates the confusion matrix and returns it as a canva
    fig2, ax = plt.subplots(figsize=(16, 6))

    canvas2 = FigureCanvasQTAgg(fig2)

    cm = confusion_matrix(actual, predicted)
    sns.heatmap(cm,
                annot=True,
                fmt='g',
                xticklabels=['Setosa', 'Versicolor', 'Virginica'],
                yticklabels=['Setosa', 'Versicolor', 'Virginica']
                )

    plt.ylabel('Prediction', fontsize=13)
    plt.xlabel('Actual', fontsize=13)
    plt.title('Confusion Matrix', fontsize=17)
    return canvas2
