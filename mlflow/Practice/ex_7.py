import mlflow

# set tracking uri
mlflow.set_tracking_uri('http://127.0.0.1:5001')

# see version wise alias of a registered model
from mlflow.tracking import MlflowClient
client = MlflowClient()

rm = client.get_registered_model("spam_classifier")

# first way
print(rm.aliases)
# second way
for alias, version in rm.aliases.items():
    print(f"Version: {version}, Alias: {alias}")


# Assign 'production' alias to v4
# Assign 'champion' alias to v3
client.set_registered_model_alias(
    name="spam_classifier",
    alias="champion",
    version="3"
)

print("\bAfter Assigning Alias\n")

# see version wise alias
rm = client.get_registered_model("spam_classifier")

for alias, version in rm.aliases.items():
    print(f"Version: {version}, Alias: {alias}")
    

# Load model using Alias
model_name = "spam_classifier"
alias = "production"

## before loading checkout if the pointer is pointing to correct model
from mlflow.tracking import MlflowClient
client = MlflowClient()

mv = client.get_model_version_by_alias(
    name = model_name,
    alias = alias
)

print(f"Alias 'production' points to version: {mv.version}")

## load model
import mlflow.pyfunc

model = mlflow.pyfunc.load_model(
    model_uri = f"models:/{model_name}@{alias}"
)

## model is loaded, this model can be used for inference now