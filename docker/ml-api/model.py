from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
import pickle

# load dataset
X, y = load_iris(return_X_y=True)

# model
params = {
    "l1_ratio" : 0,
    "C" : 1.3,
    "max_iter" : 150,
    "solver" : "lbfgs"
}
model = LogisticRegression(**params, random_state=42)

# fit the model
model.fit(X, y)

# save the model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)