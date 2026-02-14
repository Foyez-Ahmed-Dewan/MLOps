# MLflow Practice Repository

This repository contains structured exercises to practice MLflow experiment tracking, model registry, and model serving workflows step by step.

---

### **Exercise 1: Basic Experiment Tracking**

**Goal:** Understand runs, params, metrics

**Task**

- Train a simple model (LogisticRegression / RandomForest)
- Create an MLflow experiment named `mlflow_practice`
- Log:
    - learning_rate / max_depth
    - accuracy
- Run the script **twice with different parameters**

**You should verify**

- Two separate runs exist
- Metrics differ
- Params are visible in UI

---

### **Exercise 2: Manual Run Control**

**Goal:** Learn why `start_run()` matters

**Task**

- Explicitly start and end runs
- Inside one script:
    - create **two runs** sequentially
- Log different params in each

**Break it**

- Remove `start_run()`
- Observe where logs go

---

### **Exercise 3: Logging Artifacts**

**Goal:** Understand artifacts vs metrics

**Task**

- Generate:
    - confusion matrix plot
    - classification report (txt)
- Log them as artifacts
- Open them from MLflow UI

---

### **Exercise 4: Autologging Comparison**

**Goal:** Understand what autologging does

**Task**

- Enable `mlflow.sklearn.autolog()`
- Train a model
- Inspect:
    - params
    - metrics
    - model
    - artifacts

What was logged automatically?

- dataset train, eval
- model
- metrics: accuracy, precision, recall, f1, roc-auc, training_score
- parameters, even though there are only 3 used in the experiment, it lists all estimator parameters with null value (if not provided)
- artifacts (model related files)

What was NOT logged?

- confusion matrix figure

NOTE:  
MLflow autologging logs what the framework exposes, not what *you visualise*. Custom evaluation metrics, artifacts such as confusion matrices or plots are not logged automatically.

---

### **Exercise 5: Hybrid Logging**

**Goal:** Learn real-world usage

**Task**

- Enable autologging
- Manually log:
    - custom metric (e.g., F1)
    - custom artifact (plot)

👉 Observe:

- Both appear in same run
- No conflicts if named properly

---

### **Exercise 6: Register a Model**

**Goal:** Learn model lifecycle

**Task**

- Log and register a model
- Register under name: `spam_classifier`
- Verify version `v1` exists

---

## Exercise 7:

- For a registered model, see alias
- Set alias to specific version and verify
- Load a model using alias

MLflow guarantees:

- same model
- same weights
- same artifacts

It does **not** guarantee:

- correct input
- correct feature engineering
- correct business logic

---

## Exercise 8:

Using the Iris dataset, do the following in a single MLflow workflow:

1. Load the Iris dataset and prepare features and labels.
2. Train three models:
    - Logistic Regression
    - Decision Tree
    - Random Forest
- Track each training as a separate MLflow run under the same experiment.
- Evaluate all models using the same metric and identify the best-performing run.
1. Register the best model in the MLflow Model Registry.
2. Assign an alias to the registered model (e.g., `production` or `champion`).
3. Load the model using the alias (not run ID or version).
4. Make predictions on sample Iris inputs and verify the outputs are reasonable.

---

## Exercise 9: Serving via FastAPI

- load a registered model
- write api endpoints to make prediciton
- verify using fastapi and postman

---

## Exercise 10

**Breast Cancer Classification Service**

**Dataset:** `breast_cancer` from `sklearn.datasets`

**Goal:** Practice MLflow logging, experiment tracking, and model serving

**Models to Try:**

1. Logistic Regression
2. RandomForestClassifier
3. GradientBoostingClassifier

**MLflow Tasks:**

1. **Experiment Setup:**
    - Create an experiment named `'breast_cancer_classification_experiments'`.
    - Each model should be a separate run.
2. **Logging:**
    - Log training hyperparameters.
    - Log evaluation metrics: Accuracy, Precision, Recall, F1-score.
    - Log Confusion Matrix plot and full Classification Report.
    - Use **both autologging** (for models) **and manual logging** (for F1-score, confusion matrix plot).
3. **Best Model Selection:**
    - Compare all models based on **F1-score**.
    - Log a **tag** `best_model=True` for the selected run.
4. **Model Registration:**
    - Register **only the best model** as `'breast_cancer_classifier'`.
    - Promote the best version to **Production**.
    - Add a **description** explaining why this model was chosen.
5. **Model Serving:**
    - Serve the Production model using **FastAPI**.
    - Create endpoints to accept new patient data and return predictions.
6. **Verification:**
    - Test the API endpoints using **Swagger UI** and **Postman** to ensure proper serving.
