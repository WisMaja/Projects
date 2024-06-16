from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from lazypredict.Supervised import LazyClassifier

# Pobierz zbiór danych mushroom z OpenML
mushroom = fetch_openml(name='mushroom', version=1, as_frame=True)

# Wyodrębnij cechy i etykiety
X = mushroom.data
y = mushroom.target

# Podziel dane na zestawy treningowe i testowe
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Utwórz instancję LazyClassifier
clf = LazyClassifier(verbose=0, ignore_warnings=True, custom_metric=None)

# Dopasuj modele i przewiduj na zestawie testowym
models, predictions = clf.fit(X_train, X_test, y_train, y_test)

# Wyświetl wyniki
print(models)
