from fastapi import FastAPI, Request
from pydantic import BaseModel
import pickle 
import numpy as np
import pandas as pd

app = FastAPI(
    title="IRIS Classifier"
)

# load model at startup
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# routes
@app.get('/health')
def health():
    return {'status': 'healthy', 'model' : 'loaded'}

# # 
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    
# class name for iris dataset
class_names = ['setosa', 'versicolor', 'virginica']

@app.post('/predict')
def make_prediction(data: IrisInput):
    input_df = pd.DataFrame([data.model_dump()])
    pred = model.predict(input_df)[0]
    pred_prob = model.predict_proba(input_df)[0].tolist()
    
    return {
        'prediction': int(pred),
        'class_name': class_names[int(pred)],
        'probabilities': pred_prob
    }
    
    