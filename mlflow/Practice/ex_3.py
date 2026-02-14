import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

# # Load dataset
data = pd.read_csv("winequality-red.csv")
X = data.drop("quality", axis=1)
y = (data["quality"] >= 7).astype(int)  # Binary classification: quality >= 7 is "good"

# split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

## set mlflow tracking uri
mlflow.set_tracking_uri('http://127.0.0.1:5000')

## create an experiment
# mlflow.create_experiment('exercise3')

# set experiment
mlflow.set_experiment('exercise3')

## create run
with mlflow.start_run(run_name='first_run') as run:
    lr_params = {"C": 1.0, "max_iter": 200}
    lr_model = LogisticRegression(**lr_params, random_state=42)
    lr_model.fit(X_train, y_train)
    lr_pred = lr_model.predict(X_test)
    lr_accuracy = accuracy_score(y_test, lr_pred)

    ## Log parameters and metrics
    mlflow.log_params(lr_params)
    mlflow.log_metric("accuracy", lr_accuracy)
    
    ## save prediciton array as artifact
    np.save('predictions.npy', lr_pred)
    mlflow.log_artifact('predictions.npy')
    

    # Log confusion matrix as artifact
    cm = confusion_matrix(y_test, lr_pred)
    plt.figure(figsize=(5, 5))
    sns.heatmap(cm, annot=True, fmt="d")
    plt.title("Logistic Regression Confusion Matrix")
    plt.savefig("lr_confusion_matrix.png")
    ## log artifact
    mlflow.log_artifact("lr_confusion_matrix.png")

    # Log model
    mlflow.sklearn.log_model(lr_model, "logistic_regression_model")
    print(f"Logistic Regression Accuracy: {lr_accuracy}")