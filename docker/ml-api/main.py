from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np
import pandas as pd

app = FastAPI(
    title="IRIS Classfier Test"
)

# load model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
    
# route
@app.get('/welcome')
def welcome_msg():
    return {'message' : 'APP is working'}

# input validation
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width : float 
    petal_length: float
    petal_width : float 
    
# class name for iris dataset
class_names = ['setosa', 'versicolor', 'virginica']

# prediction endpoint
@app.post('/predict')
def make_prediction(input_data: IrisInput):
    input_df = pd.DataFrame([input_data.model_dump()])
    
    pred = int(model.predict(input_df)[0])
    
    prob = model.predict_proba(input_df)[0].tolist()
    
    return {
        'prediction' : pred,
        'class name' : class_names[pred],
        'probabilities' : prob
    }