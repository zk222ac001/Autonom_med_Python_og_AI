import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Step 1: Load the dataset
data = load_breast_cancer()
X = data.data
y = data.target
feature_names = data.feature_names
target_names = data.target_names

# Step 2: Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Train the model (Random Forest)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Step 4: Make predictions
y_pred = clf.predict(X_test)

# Step 5: Evaluation
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=target_names))

# Step 6: Confusion Matrix
conf_mat = confusion_matrix(y_test, y_pred)

# Step 7: Feature Importance
importances = clf.feature_importances_
indices = np.argsort(importances)[::-1]

# Step 8: Plot Confusion Matrix & Feature Importance
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Confusion Matrix plot
sns.heatmap(conf_mat, annot=True, fmt='d', cmap='Blues',
            xticklabels=target_names, yticklabels=target_names, ax=axes[0])
axes[0].set_title(f"Confusion Matrix (Accuracy: {accuracy:.2%})")
axes[0].set_xlabel("Predicted")
axes[0].set_ylabel("Actual")

# Feature Importance plot
axes[1].bar(range(X.shape[1]), importances[indices], align="center")
axes[1].set_xticks(range(X.shape[1]))
axes[1].set_xticklabels(feature_names[indices], rotation=90)
axes[1].set_title("Feature Importances")
axes[1].set_ylabel("Importance Score")

plt.tight_layout()
plt.show()

'''
1. Concept
Breast Cancer Classification is a supervised machine learning problem where the goal is to 
predict whether a breast tumor is:
Malignant (cancerous) → needs urgent treatment
Benign (non-cancerous) → not harmful
We use medical measurements (like cell size, shape, and texture) from a tumor 
sample to train a model that can predict the correct category.

2. Definition
Breast Cancer Classification is the process of using labeled medical data (features describing tumors) 
to train a machine learning model that can classify a tumor into malignant or benign classes.
It is a binary classification problem because there are only two possible outcomes.

3. How It Works
Data Collection → We use datasets like the Breast Cancer Wisconsin Dataset (built into scikit-learn).
Features → Tumor measurements such as:
Mean radius
Mean texture
Mean perimeter
Mean smoothness
(30 features in total)
Labels →
0 = Malignant
1 = Benign
Training → We use part of the data to train a model (e.g., Random Forest).
Testing → We use the rest of the data to check the model’s accuracy.
Evaluation → Metrics like accuracy, precision, recall, and confusion matrix show performance.

5. Output
Accuracy Score → Percentage of correct predictions.
Classification Report → Precision, recall, F1-score for each class.
Confusion Matrix → Shows how many malignant/benign cases were classified correctly or incorrectly.
Feature Importance Chart → Highlights which tumor features influence the prediction most.

'''
