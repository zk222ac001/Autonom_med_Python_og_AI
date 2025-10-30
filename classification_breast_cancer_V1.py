# predicting whether a tumor is malignant or benign.

# Step 1: Import libraries
# Loads the built-in Breast Cancer Wisconsin dataset from scikit-learn.
from sklearn.datasets import load_breast_cancer
# → Splits the dataset into training and testing sets.
from sklearn.model_selection import train_test_split
# → A machine learning model that uses multiple decision trees for classification.
from sklearn.ensemble import RandomForestClassifier
# accuracy_score →  Measures the percentage of correct predictions.
# classification_report → Shows precision, recall, F1-score, and support for each class.
# confusion_matrix → Table showing true positives, false positives, true negatives, false negatives.
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Step 2: Load the dataset
'''
Loads the breast cancer dataset into the variable data.
data contains:
data.data → Feature matrix (measurements of tumors, 30 features total)
data.target → Labels (0 = malignant, 1 = benign)
data.feature_names → Names of the features
data.target_names → Names of the classes (malignant, benign)
'''
data = load_breast_cancer()
# X → Input features for the model (shape: [569 samples, 30 features]).
X = data.data       # Features (e.g., mean radius, texture, perimeter, etc.)
# y → Output labels (0 or 1 for tumor type).
y = data.target     # Labels: 0 = malignant, 1 = benign

# Step 3: Split into training and test sets
'''
Splits the dataset into:
X_train, y_train → 80% of the data for training.
X_test, y_test → 20% of the data for testing.
test_size=0.2 → 20% of the dataset will be for testing.
random_state=42 → Makes the split reproducible (same random selection every run).
'''
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

'''
Creates a Random Forest Classifier with:
n_estimators=100 → Uses 100 decision trees in the forest.
random_state=42 → Ensures reproducibility of the model.
.fit(X_train, y_train) → Trains the model on the training data.
'''
# Step 4: Initialize and train the model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Step 5: Make predictions
# Uses the trained model to predict the tumor type for the test set (X_test).

# Stores predictions in y_pred.
# Uses the trained model to predict the tumor type for the test set (X_test).
y_pred = clf.predict(X_test)

# Step 6: Evaluate the model
# Calculates the accuracy by comparing predicted labels (y_pred) with actual labels (y_test).
accuracy = accuracy_score(y_test, y_pred)
# Prints the accuracy score.
print("Accuracy:", accuracy)

'''
Prints a detailed performance report:
Precision → How many predicted positives are actually correct.
Recall → How many actual positives were correctly identified.
F1-score → Balance between precision and recall.
Support → Number of samples for each class.'''

print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=data.target_names))

'''
Prints the confusion matrix, a table showing:
True Negatives (TN) → Correctly predicted malignant.
False Positives (FP) → Benign predicted as malignant.
False Negatives (FN) → Malignant predicted as benign.
True Positives (TP) → Correctly predicted benign.
'''
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
