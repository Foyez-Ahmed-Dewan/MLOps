import mlflow
from fastapi import FastAPI 
from pydantic import BaseModel
import pandas as pd

# set tracking server
mlflow.set_tracking_uri('http://127.0.0.1:5001')

# load registered model
model_name = "iris-decision"
version = "2"

model_uri = f"models:/{model_name}/{version}"

try:
    model = mlflow.sklearn.load_model(model_uri)
    print("Model Loaded Successfully...!")
    
    if hasattr(model, 'features_names_in_'):
        expected_features = list(model.feature_names_in_)
        print(f"Model expects these feature: {expected_features}")
    else:
        print(f"No features_names_in_ attributes")
    # if you registered the model using infer_signature, you will get the features name, otherwise you wont'
except Exception as e:
    raise Exception(f"Failed to load model: {str(e)}")

## define the input schema
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    
##### FastAPI
app = FastAPI()

@app.get('/')
def start():
    return {'message' : 'IRIS classifier API'}

@app.post('/predict')
def make_prediction(input_data: IrisInput):
    # convert input data to dataframe
    input_df = pd.DataFrame([input_data.dict()])
    # make prediction
    pred = model.predict(input_df)
    
    return {'prediction' : pred.tolist()}
    
# checkout example
# {
#   "sepal_length": 6.9,
#   "sepal_width": 3.1,
#   "petal_length": 5.4,
#   "petal_width": 2.1
# }
# output: 2

# {
#   "sepal_length": 6.0,
#   "sepal_width": 2.7,
#   "petal_length": 4.5,
#   "petal_width": 1.5
# }

# output: 1