# scikit-learn library with a simple Linear Regression example
# Step 1 : Install libraries (if needed)
# pip install scikit-learn pandas matplotlib

# Step 2 :  import libraries ...........................................................
# data handling and data manipulation
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt # for plotting
from sklearn.linear_model import LinearRegression # for linear regression (model)
from sklearn.model_selection import train_test_split # split data into train/test sets
from sklearn.metrics import mean_squared_error, r2_score # evaluation metrics

 # Step 3 : Load the dataset................................................................
 # small dataset of Years of Experience vs Salary.
data = {
    'YearsExperience': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Salary': [35000, 40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000]
}
df = pd.DataFrame(data)
print(df)

# Step 4 – Split data
# X (features) must be 2D; that’s why we select with double brackets to keep a DataFrame.
# y (target) is 1D series.
X = df[['YearsExperience']]  # Feature
y = df['Salary']  # Target

# Creates a tiny toy dataset where Salary increases by a constant 5,000 per year. 
# DataFrame makes it tabular; print shows it.
# Split into 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# step 5 - Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# step 6 - Make predictions
y_pred = model.predict(X_test)
print("Predictions:", y_pred)

# Step 7 - Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Mean Squared Error:", mse)
print("R² Score:", r2)

# Step 8 - Plot the results ( Visualize the data and the model)
plt.scatter(X, y, color='blue', label="Actual Data")
plt.plot(X, model.predict(X), color='red', label="Regression Line")
plt.xlabel("Years of Experience")
plt.ylabel("Salary")
plt.legend()
plt.show()
