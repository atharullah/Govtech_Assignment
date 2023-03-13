import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Load the car evaluation dataset
data_file = "car.data"
columns = ["buying", "maint", "doors", "persons", "lug_boot", "safety", "class"]
df = pd.read_csv(data_file, names=columns, header=None)

# Preprocess the dataset
le = LabelEncoder()
df["buying"] = le.fit_transform(df["buying"])
df["maint"] = le.fit_transform(df["maint"])
df["doors"] = le.fit_transform(df["doors"])
df["persons"] = le.fit_transform(df["persons"])
df["lug_boot"] = le.fit_transform(df["lug_boot"])
df["safety"] = le.fit_transform(df["safety"])
df["class"] = le.fit_transform(df["class"])

ohe = OneHotEncoder()
X = ohe.fit_transform(df[["maint", "doors", "lug_boot", "safety", "class"]]).toarray()
y = df["buying"].values

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train a decision tree model
model = DecisionTreeRegressor(random_state=42)
model.fit(X_train, y_train)

# Evaluate the model on the testing set
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Predict the buying price for a car with the given parameters
new_car = ohe.transform([[3, 3, 1, 2, 0]]).toarray()  # High maintenance, 4 doors, big lug boot, high safety, good class
price = model.predict(new_car)
print("Predicted buying price:", price)
