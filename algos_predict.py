from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

#KNeighborsClassifier est utilisé pour la classification
# on entraine le classificateur avec .fit
# X a deux dimensions (nombre d'échantillons et nombre de variables (features)) et y 1 dimensions (targets)
# on fait les prédictions avec .predict


dataframe = pd.read_csv(r'C:\Louis\Cours\Projet Peip2\PythonPrototypeGUI-main(2)\PythonPrototypeGUI-main\iris.csv')
label=[]
nrow = len(dataframe.index)

for i in range(nrow):
    label.append(dataframe.iat[i,-1]) #-1 permet d'aller dans la denière colonne (où se trouve les labels)

label_array = np.array(label)

matrice = dataframe.to_numpy()
matrice_sans_label = matrice[:,:-1]

def cart(data,target):
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=42)
    cart_classifier = DecisionTreeClassifier()
    cart_classifier.fit(X_train, y_train)
    predictions = cart_classifier.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy: {accuracy}")


    # Use PCA to reduce the dimensionality for visualization (2D plot)
    pca = PCA(n_components=2)
    X_train_pca = pca.fit_transform(X_train)

#######   convertion de y_train en liste d'entier, pour la rendre utilisable dans plt.scatter ################
    noms_de_labels = np.unique(y_train)

    longueur = len(y_train)
    valeur_initiale = 0
    y_train_number = [valeur_initiale] * longueur #on force la liste à avoir la même longueur que y_train

    n=0
    for nom in noms_de_labels:
        for i in range (len(y_train_number)):
            if y_train[i]==nom:
                y_train_number[i]=n
        n+=1
##########################################################################################################
    # Scatter plot of the actual labels
    plt.scatter(X_train_pca[:, 0], X_train_pca[:, 1], c=y_train_number, cmap='viridis', label='Actual Labels')

    predictions_pca = pca.transform(X_test)

    valeur_initiale = 0
    predicion_number = [valeur_initiale] * len(y_test)  # on force la liste à avoir la même longueur que y_test

    n = 0
    for nom in noms_de_labels:
        for i in range(len(predicion_number)):
            if predictions[i] == nom:
                predicion_number[i] = n
        n += 1
    # Scatter plot of predicted labels

    plt.scatter(predictions_pca[:, 0], predictions_pca[:, 1], c=predicion_number, marker='x', cmap='viridis',label='Predicted Labels')

    plt.title('Actual and Predicted Labels with KNN algorithm')
    plt.legend()
    plt.show()

def KNN(data,target):
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=42)
    KNN_classifier = KNeighborsClassifier()
    KNN_classifier.fit(X_train, y_train)
    predictions = KNN_classifier.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy: {accuracy}")

    # Use PCA to reduce the dimensionality for visualization (2D plot)
    pca = PCA(n_components=2)
    X_train_pca = pca.fit_transform(X_train)

#######   convertion de y_train en liste d'entier, pour la rendre utilisable dans plt.scatter ################
    noms_de_labels = np.unique(y_train)

    longueur = len(y_train)
    valeur_initiale = 0
    y_train_number = [valeur_initiale] * longueur #on force la liste à avoir la même longueur que y_train

    n=0
    for nom in noms_de_labels:
        for i in range (len(y_train_number)):
            if y_train[i]==nom:
                y_train_number[i]=n
        n+=1
##########################################################################################################
    # Scatter plot of the actual labels
    plt.scatter(X_train_pca[:, 0], X_train_pca[:, 1], c=y_train_number, cmap='viridis', label='Actual Labels')

    predictions_pca = pca.transform(X_test)

    valeur_initiale = 0
    predicion_number = [valeur_initiale] * len(y_test)  # on force la liste à avoir la même longueur que y_test

    n = 0
    for nom in noms_de_labels:
        for i in range(len(predicion_number)):
            if predictions[i] == nom:
                predicion_number[i] = n
        n += 1
    # Scatter plot of predicted labels

    plt.scatter(predictions_pca[:, 0], predictions_pca[:, 1], c=predicion_number, marker='x', cmap='viridis',label='Predicted Labels')

    plt.title('Actual and Predicted Labels with KNN algorithm')
    plt.legend()
    plt.show()

def random_forest(data,target):
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=42)
    random_forest_classifier = RandomForestClassifier()
    random_forest_classifier.fit(X_train, y_train)
    predictions = random_forest_classifier.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy: {accuracy}")


    # Use PCA to reduce the dimensionality for visualization (2D plot)
    pca = PCA(n_components=2)
    X_train_pca = pca.fit_transform(X_train)

#######   convertion de y_train en liste d'entier, pour la rendre utilisable dans plt.scatter ################
    noms_de_labels = np.unique(y_train)

    longueur = len(y_train)
    valeur_initiale = 0
    y_train_number = [valeur_initiale] * longueur #on force la liste à avoir la même longueur que y_train

    n=0
    for nom in noms_de_labels:
        for i in range (len(y_train_number)):
            if y_train[i]==nom:
                y_train_number[i]=n
        n+=1
##########################################################################################################
    # Scatter plot of the actual labels
    plt.scatter(X_train_pca[:, 0], X_train_pca[:, 1], c=y_train_number, cmap='viridis', label='Actual Labels')

    predictions_pca = pca.transform(X_test)

    valeur_initiale = 0
    predicion_number = [valeur_initiale] * len(y_test)  # on force la liste à avoir la même longueur que y_test

    n = 0
    for nom in noms_de_labels:
        for i in range(len(predicion_number)):
            if predictions[i] == nom:
                predicion_number[i] = n
        n += 1

    # Scatter plot of predicted labels
    plt.scatter(predictions_pca[:, 0], predictions_pca[:, 1], c=predicion_number, marker='x', cmap='viridis',label='Predicted Labels')
    plt.title('Actual and Predicted Labels with random forest algorithm')
    plt.legend()
    plt.show()

