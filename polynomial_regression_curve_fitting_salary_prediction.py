# Step no : 1 Polynomial Regression Example
import pandas as pd # handling data 
import numpy as np # creating and manipulating numerical arrays.
import matplotlib.pyplot as plt #  for plotting data & results.
from sklearn.linear_model import LinearRegression # the model we’ll use for fitting data.
from sklearn.preprocessing import PolynomialFeatures # transforms our data into polynomial form (adds powers of features).
from sklearn.metrics import mean_squared_error # metric for measuring prediction error.
from sklearn.metrics import r2_score #  metric for measuring how well the model fits the data.

# Step no :2  ................................Fake non-linear dataset.......................................
# X → represents Years of Experience (reshaped into a column vector using .reshape(-1, 1) so sklearn accepts it).
X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape(-1, 1)
# y → represents Salary values (The data grows non-linearly — salary increases faster after a few years)
y = np.array([35000, 37000, 42000, 49000, 57000, 66000, 77000, 89000, 102000, 116000])

# Step no: 3 Transform to polynomial features (degree=2 means quadratic)
"""
degree=2 means we want quadratic terms:
For example, if X = [2], polynomial features become:
[1, 2, 4] → (1 for bias term, 2 for original value, 4 for squared value).
fit_transform(X) → creates a new dataset with the squared term added.
Result: X_poly now has 3 columns:1 (constant term), Years, Years². 
"""
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)

# Step no: 4 Train model
"""
Creates a linear regression model.
fit() trains it using polynomial features X_poly and target values y.
Even though we use LinearRegression, because X_poly has Years², the model fits a curve.
"""
model = LinearRegression()
model.fit(X_poly, y)

# Step no :5 Predictions
"""
Uses the trained model to predict salaries for all years in the dataset.
Output is a set of smooth curve values matching the polynomial fit. 
"""
y_pred = model.predict(X_poly)

# Step no :6 (Evaluation)
# MSE (Mean Squared Error) → average squared difference 
# between actual and predicted salaries. Smaller = better.
print("MSE:", mean_squared_error(y, y_pred))
# R² (Coefficient of Determination) → proportion of variance explained by 
# the model (1 = perfect fit).
print("R²:", r2_score(y, y_pred))
# model.coef_ → list of coefficients for [constant, Years, Years²].
# model.intercept_ → the constant bias term
# Formats the output into a readable equation: Salary = a*Years² + b*Years + c
print("Equation: Salary = {:.2f} * Years² + {:.2f}*Years + {:.2f}".format(
    model.coef_[2], model.coef_[1], model.intercept_
))

# Step no :7 (Plot)
plt.scatter(X, y, color="blue", label="Actual Data") # scatter() → blue dots for actual data points.
plt.plot(X, y_pred, color="red", label="Polynomial Fit") # red curve for model predictions.
plt.xlabel("Years of Experience")
plt.ylabel("Salary") 
plt.legend() # shows which line is which.
plt.show() # displays the plot.
