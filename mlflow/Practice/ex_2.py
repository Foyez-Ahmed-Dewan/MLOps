import mlflow 

mlflow.set_tracking_uri('http://127.0.0.1:5000')

# mlflow.create_experiment('exercise2')

mlflow.set_experiment('exercise2')

# start 1st run
run = mlflow.start_run(run_name='first-run')

mlflow.log_param('learning_rate', 2e-5)
mlflow.log_metric('accuracy', 92.5)

# end 1st run
mlflow.end_run()

# start 2nd run
mlflow.start_run(run_name='second-run')

mlflow.log_param('max_depth', 5)
mlflow.log_param('learning_rate', 1e-6)
mlflow.log_metric('accuracy', 92.7)

# end 2nd run
mlflow.end_run()