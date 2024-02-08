from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np

dataframe = pd.read_csv(r'C:\Louis\Cours\Projet Peip2\PythonPrototypeGUI-main(2)\PythonPrototypeGUI-main\iris.csv')
label = []
nrow = len(dataframe.index)

for i in range(nrow):
    label.append(dataframe.iat[i, -1])

label_array = np.array(label)

matrice = dataframe.to_numpy()
matrice_sans_label = matrice[:, :-1]

def plot_algorithm_result(classifier, matrice_sans_label, label_array, algorithm_name):
    X_train, X_test, y_train, y_test = train_test_split(matrice_sans_label, label_array, test_size=0.2,
                                                        random_state=42)
    classifier = classifier()  # instantiate the classifier
    classifier.fit(X_train, y_train)
    predictions = classifier.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"{algorithm_name} Accuracy: {accuracy}")

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
    plt.show()

print(matrice_sans_label)
print(label_array)

#plot_algorithm_result(KNeighborsClassifier, matrice_sans_label, label_array, "KNeighborg")
