# Multi-Feature Regression Example
# Let’s add Education Level as a second feature
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Dataset: YearsExperience, EducationYears, Salary
data = {
    'YearsExperience': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'EducationYears': [12, 12, 14, 14, 16, 16, 18, 18, 20, 20],
    'Salary': [35000, 40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000]
}
df = pd.DataFrame(data)

# Features & Target
X = df[['YearsExperience', 'EducationYears']]
y = df['Salary']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Coefficients & Equation
print("Intercept:", model.intercept_)
print("Coefficients:", model.coef_)
print("Equation: Salary = {:.2f}*(YearsExperience) + {:.2f}*(EducationYears) + {:.2f}".format(
    model.coef_[0], model.coef_[1], model.intercept_
))

# Test Predictions
print("\nTest Predictions vs Actual:")
for pred, actual in zip(y_pred, y_test):
    print(f"Predicted: {pred:.2f}, Actual: {actual}")
