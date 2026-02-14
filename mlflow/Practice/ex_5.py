import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

import mlflow 
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

# load data
df = pd.read_csv('winequality-red.csv')
X = df.drop('quality', axis=1)
y = (df['quality'] >= 7.0).astype(int) # binary value : 0 or 1

# split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# set tracking uri
mlflow.set_tracking_uri('http://127.0.0.1:5001')

## create experiment
# mlflow.create_experiment('exercise5')

# set experiment
mlflow.set_experiment('exercise5')

# start run
with mlflow.start_run(run_name="exercise5") as run: 
    # parameters
    params = {
        'max_iter' : 100,
        'C' : 1.0
    }
    
    # model
    lr_model = LogisticRegression(**params, random_state=42)
    
    # train
    lr_model.fit(X_train, y_train)
    
    # predict
    pred = lr_model.predict(X_test)
    
    # accuracy
    accuracy = accuracy_score(y_test, pred)
    
    # confusion matrix
    cm = confusion_matrix(y_test, pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d")
    plt.title("Confusion Matrix")
    plt.savefig("Confusion Matrix.png")
    
    # enable autologging
    mlflow.sklearn.autolog()
    # manual logging custom metrics
    mlflow.log_metric('accuracy', accuracy)
    mlflow.log_artifact("Confusion Matrix.png")
