# protocol: e.g., 6 = TCP, 17 = UDP
# malicious: target label (0 = benign, 1 = malicious)

import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv("network_flows.csv")

# Separate features and labels
X = df.drop("malicious", axis=1)
y = df["malicious"]

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Build a simple neural network
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')  # Binary classification
])

# Compile the model
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
)

# Train the model
history = model.fit(
    X_train, y_train,
    epochs=20,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

# Evaluate on test data
test_loss, test_acc, test_prec, test_rec = model.evaluate(X_test, y_test)
print(f"\n✅ Test Accuracy: {test_acc:.4f}, Precision: {test_prec:.4f}, Recall: {test_rec:.4f}")

# Predict on new flow data
new_flow = [[0.5, 400, 200, 10, 6, 16]]  # Example input
new_flow_scaled = scaler.transform(new_flow)
prediction = model.predict(new_flow_scaled)
print(f"Malicious probability: {prediction[0][0]:.4f}")
print("Prediction:", "Malicious" if prediction[0][0] > 0.5 else "Benign")
