import mlflow
from sklearn.linear_model import LogisticRegression

# # set tracking uri
mlflow.set_tracking_uri('http://127.0.0.1:5000')

# create experiment (during initial run only)
# mlflow.create_experiment('mlflow_prac')

# set experiment
mlflow.set_experiment('mlflow_prac')

lr = LogisticRegression()

#first run
with mlflow.start_run(run_name="first_run") as run:
    mlflow.log_param('learning_rate', 1e-5)
    mlflow.log_param('max_depth', 10)
    
    mlflow.log_metric('accuracy', 92)
    
    mlflow.sklearn.log_model(lr, "logistic regression-1")

# # second run
# with mlflow.start_run(run_name="second_run") as run:
#     # log parameter
#     params = {
#         'learning_rate' : 1e-6,
#         'regularization' : 2e-3,
#         'max_depth': 5
#     }
    
#     mlflow.log_params(params)
    
#     # log metrics
#     metrics = {
#         'accuracy' : 96,
#         'roc-auc' : 0.72
#     }

#     mlflow.log_metrics(metrics)
    
#     # log model
#     mlflow.sklearn.log_model(lr, "logistic_regression-2")
    
    