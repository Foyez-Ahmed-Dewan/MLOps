import mlflow 
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from mlflow.models import infer_signature
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#### STEP - 0: Dataset Preparation #####
# load dataset
X, y = load_breast_cancer(return_X_y=True)

# split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#### STEP - 1: Tracking server and experiment creation #####
# set tracking uri
mlflow.set_tracking_uri('http://127.0.0.1:5000')

# create experiment
# mlflow.create_experiment('breast_cancer_classification_experiments')

# set experiment
mlflow.set_experiment('breast_cancer_classification_experiments')

#### STEP - 2: Model training and logging #####

## helper function for metrics
def get_metrics(y_test, y_pred):
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    
    cr = classification_report(y_test, y_pred, output_dict=True)
    df_cr = pd.DataFrame(cr).T  # now classe -> rows, metrrics -> columns
    
    return acc, prec, recall, f1, cm, df_cr
    
# Logistic Regression
with mlflow.start_run(run_name='logistic regression') as run:
    # model
    params = {
        'solver' : 'liblinear',
        'C' : 1.0,
        'max_iter' : 100
    }
    
    lr_model = LogisticRegression(**params, random_state=42)
    lr_model.fit(X_train, y_train)
    y_pred = lr_model.predict(X_test)
    # metric
    acc, prec, recall, f1, cm, df_cr = get_metrics(y_test, y_pred)
    df_cr.to_csv('cr-lr.csv')
    
    signature = infer_signature(X_test, y_pred)
    # cm plot
    plt.figure(figsize=(5, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('confusion-matrix-logistic-regression')
    plt.savefig('cm-lr.png')
    
    # logging
    mlflow.log_params(params)
    mlflow.log_metric('accuracy', acc)
    mlflow.log_metric('precision', prec)
    mlflow.log_metric('recall', recall)
    mlflow.log_metric('f1', f1)
    mlflow.log_artifact('cr-lr.csv')
    mlflow.log_artifact('cm-lr.png')
    
    mlflow.sklearn.log_model(lr_model, 'logistic_regression', signature=signature)
    

# # Random Forest 
with mlflow.start_run(run_name='random forest') as run:
    # autolog
    mlflow.sklearn.autolog()
    # models
    params = {
        'n_estimators' : 100,
        'max_depth' : None,
        'min_samples_split' : 2,
        'random_state': 42
    }
    
    rfc = RandomForestClassifier(**params)
    rfc.fit(X_train, y_train)
    y_pred = rfc.predict(X_test)
    
    # metric
    acc, prec, recall, f1, cm, df_cr = get_metrics(y_test, y_pred)
    df_cr.to_csv('cr-rfc.csv')
    # input/output schema
    signature = infer_signature(X_test, y_pred)
    
    # cm plot
    plt.figure(figsize=(5, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('confusion-matrix-random-forest')
    plt.savefig('cm-rfc.png')
    
    # disable autolog
    mlflow.sklearn.autolog(disable=True)
    
    # logging
    mlflow.log_artifact('cr-rfc.csv')
    mlflow.log_artifact('cm-rfc.png')
    

## Gradient Boosting
with mlflow.start_run(run_name='gradient_boosting') as run:
    params = {
        'n_estimators' : 100,
        'learning_rate' : 0.1,
        'max_depth' : 3,
        'random_state' : 42
    }
    
    gbc = GradientBoostingClassifier(**params)
    gbc.fit(X_train, y_train)
    y_pred = gbc.predict(X_test)
    
    # get metric
    acc, prec, recall, f1, cm, df_cr = get_metrics(y_test, y_pred)
    df_cr.to_csv('cr-gbc.csv')
    # input output scehma
    signature = infer_signature(X_test, y_pred)
    # plot
    plt.figure(figsize=(5, 5))
    sns.heatmap(cm, annot=True, fmt='d')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('confusion-matrix-gradient-boosting')
    plt.savefig('cm-gbc.png')
    
    # log
    mlflow.log_params(params)
    mlflow.log_metric('accuracy', acc)
    mlflow.log_metric('precision', prec)
    mlflow.log_metric('recall', recall)
    mlflow.log_metric('f1', f1)
    mlflow.log_artifact('cm-gbc.png')
    mlflow.log_artifact('cr-gbc.csv')
    
    mlflow.sklearn.log_model(sk_model=gbc, artifact_path = "gradient-boosting", signature=signature)


##### STEP - 3 #####
# # best run: random forest classifier
run_id = "0c449d279e074752bd63bc6546c2b460"

from mlflow.tracking import MlflowClient
client = MlflowClient()

client.set_tag(run_id, "best_model", "True")


###### STEP - 4 ######
# register best model, add description and alias
run_id = "0c449d279e074752bd63bc6546c2b460"
model_name = "model"

model_uri = f"runs:/{run_id}/{model_name}"
reg_model_name = "breast-cancer-classifier"

mlflow.register_model(
    model_uri=model_uri,
    name=reg_model_name
)

from mlflow.tracking import MlflowClient
client = MlflowClient()

client.update_registered_model(name=reg_model_name, description="The f1 score of this model is 1, means a perfect classifier.")
client.set_registered_model_alias(name=reg_model_name, alias='production', version='1')
    