from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier

#KNeighborsClassifier est utilisé pour la classification
# on entraine le classificateur avec .fit
# X a deux dimensions (nombre d'échantillons et nombre de variables (features)) et y 1 dimensions (targets)
# on fait les prédictions avec .predict

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

    # Scatter plot of the actual labels
    plt.scatter(X_train_pca[:, 0], X_train_pca[:, 1], c=y_train, cmap='viridis', label='Actual Labels')

    # Train the classifier
    cart_classifier.fit(X_train, y_train)

    # Scatter plot of predicted labels
    predictions_pca = pca.transform(X_test)
    plt.scatter(predictions_pca[:, 0], predictions_pca[:, 1], c=predictions, marker='x', cmap='viridis', label='Predicted Labels')
    plt.title('Actual and Predicted Labels with cart algorithm')
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

    # Scatter plot of the actual labels
    plt.scatter(X_train_pca[:, 0], X_train_pca[:, 1], c=y_train, cmap='viridis', label='Actual Labels')

    # Scatter plot of predicted labels
    predictions_pca = pca.transform(X_test)
    plt.scatter(predictions_pca[:, 0], predictions_pca[:, 1], c=predictions, marker='x', cmap='viridis', label='Predicted Labels')
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

    # Scatter plot of the actual labels
    plt.scatter(X_train_pca[:, 0], X_train_pca[:, 1], c=y_train, cmap='viridis', label='Actual Labels')

    # Scatter plot of predicted labels
    predictions_pca = pca.transform(X_test)
    plt.scatter(predictions_pca[:, 0], predictions_pca[:, 1], c=predictions, marker='x', cmap='viridis',
                label='Predicted Labels')
    plt.title('Actual and Predicted Labels with random forest algorithm')
    plt.legend()
    plt.show()


iris = load_iris()
cart(iris.data,iris.target)
KNN(iris.data,iris.target)
random_forest(iris.data,iris.target)