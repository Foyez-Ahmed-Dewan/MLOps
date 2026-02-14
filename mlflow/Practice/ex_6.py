import mlflow 
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# load dataset
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# set tracking uri
mlflow.set_tracking_uri('http://127.0.0.1:5001')

# create experiment
# mlflow.create_experiment('exercise6')

# set experiment
mlflow.set_experiment('exercise6')

# start run
with mlflow.start_run(run_name="exercise6") as run:
    # model
    rfc = RandomForestClassifier()
    # train
    rfc.fit(X_train, y_train)
    # pred
    pred = rfc.predict(X_test)
    # accuracy
    acccuracy = accuracy_score(y_test, pred)
    # log metrics
    mlflow.log_metric("accuracy", acccuracy)
    
    # log + register model
    mlflow.sklearn.log_model(sk_model=rfc, artifact_path="Random Wine", registered_model_name="spam_classifier")

# register already run model
# run_id = "7b9f1bb4fea949418e1da789253e6312"
# model_uri = f"runs:/Random Wine/{run_id}/model"

# mlflow.register_model(model_uri= model_uri, name="wine classifier")