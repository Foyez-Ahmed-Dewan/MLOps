############# STEP 5 ##############
import mlflow 
from fastapi import FastAPI
import pandas as pd
import json

# mlflow tracking uri
mlflow.set_tracking_uri('http://127.0.0.1:5000') 

# load registered model
model_name = "breast-cancer-classifier"
verison = 1

model_uri = f"models:/{model_name}/{verison}"

try:
    model = mlflow.sklearn.load_model(model_uri)
    print(f"Model: {model_name} loaded successfully")
except Exception as e:
    print(f"Failed to load the model: {e}")
    
### fastapi
app = FastAPI()

## api endpoints
@app.get('/')
def initial():
    return {'message': 'breast-cancer-classifier api'}

@app.post('/predict')
def make_prediction(input_data):
    # input json string -> dict -> dataframe
    input_data = pd.DataFrame([json.loads(input_data)])
    # convert all to float
    input_df = input_data.astype(float)
    # make predicitons
    pred = model.predict(input_df)
    proba = model.predict_proba(input_df)

    return {
        "prediction": int(pred[0]),
        "label": "benign" if pred[0] == 1 else "malignant",
        "probability": float(max(proba[0]))
    }


### Example INPUT ####
# {
#   "mean_radius": 14.5,
#   "mean_texture": 19.8,
#   "mean_perimeter": 94.0,
#   "mean_area": 660.0,
#   "mean_smoothness": 0.10,
#   "mean_compactness": 0.11,
#   "mean_concavity": 0.09,
#   "mean_concave_points": 0.05,
#   "mean_symmetry": 0.18,
#   "mean_fractal_dimension": 0.06,

#   "radius_error": 0.40,
#   "texture_error": 1.20,
#   "perimeter_error": 2.80,
#   "area_error": 40.0,
#   "smoothness_error": 0.007,
#   "compactness_error": 0.025,
#   "concavity_error": 0.030,
#   "concave_points_error": 0.010,
#   "symmetry_error": 0.020,
#   "fractal_dimension_error": 0.003,

#   "worst_radius": 16.8,
#   "worst_texture": 25.0,
#   "worst_perimeter": 110.0,
#   "worst_area": 900.0,
#   "worst_smoothness": 0.14,
#   "worst_compactness": 0.25,
#   "worst_concavity": 0.30,
#   "worst_concave_points": 0.12,
#   "worst_symmetry": 0.30,
#   "worst_fractal_dimension": 0.08
# }


## output: 
# {
#   "prediction": 1,
#   "label": "benign",
#   "probability": 0.55
# }
