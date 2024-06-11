import sqlite3
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM data')
rows = cursor.fetchall()

for row in rows:
    print(row)

# Charger le jeu de données Iris
iris = load_iris()
X = iris.data
y = iris.target

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Créer un objet arbre de décision
clf = DecisionTreeClassifier()

# Entraîner le modèle sur les données d'entraînement
clf.fit(X_train, y_train)

# Faire des prédictions sur les données de test
y_pred = clf.predict(X_test)

# Calculer la précision du modèle
accuracy = accuracy_score(y_test, y_pred)
print("Précision du modèle :", accuracy)

