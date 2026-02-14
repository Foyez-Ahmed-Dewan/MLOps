import mlflow 
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: load data set
X, y = load_iris(return_X_y=True)

# split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# tracking uri
mlflow.set_tracking_uri('http://127.0.0.1:5001')

# create experiment
# mlflow.create_experiment('check')

# set experiment
mlflow.set_experiment('check')

############ STEP - 2 #################
# logistic regression
with mlflow.start_run(run_name="logistic regression") as run:
    # parameters
    params = {
        'penalty' : 'l2',
        'C' : 0.01,
        'max_iter' : 150
    }
    # model
    lr = LogisticRegression(**params, random_state=42)
    # train
    lr.fit(X_train, y_train)
    # prediction
    pred = lr.predict(X_test)
    # accuracy
    accuracy = accuracy_score(y_test, pred)
    
    # confusion matrix
    cm = confusion_matrix(y_test, pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True)
    plt.title('CM - Logistic Regression')
    plt.savefig('CM-LR.png')
    
    # logs
    mlflow.log_params(params)
    mlflow.log_metric('accuracy', accuracy)
    mlflow.log_artifact('CM-LR.png')
    mlflow.sklearn.log_model(lr, 'logistic regression')


## Decision Tree
with mlflow.start_run(run_name='decision tree') as run:
    # parameters
    params = {
        # 'criterion' : 'gini',
        'criterion' : 'entropy',
        'max_depth' : 3,
        'min_samples_split' : 5
    }
    
    # model
    dt = DecisionTreeClassifier(**params, random_state=42)
    # train
    dt.fit(X_train, y_train)
    # predict
    pred = dt.predict(X_test)
    # accuracy
    accuracy = accuracy_score(y_test, pred)
    # cm
    cm = confusion_matrix(y_test, pred)
    plt.figure(figsize=(5, 5))
    sns.heatmap(cm, annot=True, fmt='d')
    plt.title('CM - Decision Tree')
    plt.savefig('CM-DT.png')
    
    # logs
    mlflow.log_params(params)
    mlflow.log_metric('accuracy', accuracy)
    mlflow.log_artifact('CM-DT.png')
    mlflow.sklearn.log_model(dt, 'decision tree')
    
## Random Forest
with mlflow.start_run(run_name='random forest') as run:
    # enable autolog
    mlflow.sklearn.autolog()
    # params
    params = {
        'n_estimators' : 5,
        'max_depth' : 3,
        'random_state' : 42
    }
    # model
    rf = RandomForestClassifier(**params)
    rf.fit(X_train, y_train)
    pred = rf.predict(X_test)
    accuracy = accuracy_score(y_test, pred)
    cm = confusion_matrix(y_test, pred)
    #disable autolog
    mlflow.sklearn.autolog(disable=True)
    
    # log confusion matrix
    plt.figure(figsize=(5, 5))
    sns.heatmap(cm, annot=True, fmt='d')
    plt.title('CM-RF')
    plt.savefig('CM-RF.png')

    mlflow.log_artifact('CM-RF.png')   

###### STEP - 4 ##########

## best run: decision tree, lets register it
run_id = "9d95b608abc04bb8b10108c652e94c81"
model_name = "decision tree"
model_uri = f"runs:/{run_id}/{model_name}"


mlflow.register_model(
    model_uri = model_uri,
    name = "iris-decision"
)

####### STEP - 5 ######
## lets give alias to register model
registered_model_name = "iris-decision"

from mlflow.tracking import MlflowClient
client = MlflowClient()

client.set_registered_model_alias(
    name = registered_model_name,
    alias = "production",
    version = '2'
)

##### STEP - 6 #########
## load model
model_name = "iris-decision"
alias = 'production'
model_uri = f"models:/{model_name}@{alias}"

model = mlflow.sklearn.load_model(
    model_uri = model_uri
)

###### STEP - 7 #######
# make prediciton
prediction = model.predict([[5.1, 3.5, 1.4, 0.2]])
print(prediction) # output: [0]


