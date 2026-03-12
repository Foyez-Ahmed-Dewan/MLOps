# Training a Machine Learning Model Inside a Docker Container

This project demonstrates how to **train a machine learning model inside a Docker container**.

The example uses the **Iris dataset** and trains a **Random Forest classifier** using Scikit-learn. The trained model and training logs are saved inside the container.

The goal of this exercise is to understand:

- Running ML workloads inside containers
- Creating isolated Python environments in containers
- Installing dependencies in a container
- Training and saving a machine learning model
- Inspecting files generated inside a container

---

# Project Overview

The workflow trains a simple **Random Forest classifier** on the Iris dataset and generates two outputs:

- `iris_model.joblib` → saved trained model
- `training_log.txt` → metadata about training

The training process runs entirely **inside a Docker container**, demonstrating how containers can be used for reproducible ML experiments.

---

# Architecture

```
Host Machine
     |
     | docker run
     v
Python Container (python:3.11-slim)
     |
     | Virtual Environment
     v
Python + ML Libraries
     |
     | Run Training Script
     v
Trained Model + Training Log
```

---

# Prerequisites

Ensure the following tools are installed:

- Docker

Verify installation:

```bash
docker --version
```

---

# Step 1 — Start a Python Container

Run an interactive Python container:

```bash
docker run -it --name ml-percy python:3.11-slim /bin/bash
```

Explanation:

- `-it` → interactive terminal
- `--name ml-percy` → container name
- `python:3.11-slim` → lightweight Python image
- `/bin/bash` → start a bash shell

You are now **inside the container environment**.

---

# Step 2 — Create a Virtual Environment

Create a Python virtual environment inside the container:

```bash
python -m venv .venv
```

Activate the environment:

```bash
source .venv/bin/activate
```

---

# Step 3 — Install Machine Learning Dependencies

Install required libraries:

```bash
pip install scikit-learn numpy joblib
```

These libraries are used for:

- dataset loading
- model training
- saving trained models

---

# Step 4 — Create the Training Script

Create the Python training script inside the container.

Example command:

```bash
cat << 'EOF' > train_model.py
```

Add the script content and close with:

```bash
EOF
```
Example:
```bash
cat << 'EOF' > train_model.py
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load the Iris dataset
print("Loading Iris dataset...")
X, y = load_iris(return_X_y=True)

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")

# Train a Random Forest classifier
print("Training Random Forest model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Model accuracy: {accuracy:.4f}")

# Save the trained model
model_path = 'iris_model.joblib'
joblib.dump(model, model_path)
print(f"Model saved to {model_path}")

# Save training metadata
with open('training_log.txt', 'w') as f:
    f.write(f"Model: Random Forest Classifier\n")
    f.write(f"Estimators: 100\n")
    f.write(f"Accuracy: {accuracy:.4f}\n")
    f.write(f"Training samples: {len(X_train)}\n")
print("Training log saved to training_log.txt")
EOF

```
The script will:

- Load the Iris dataset
- Split data into train/test
- Train a Random Forest classifier
- Evaluate model accuracy
- Save the trained model
- Save a training log

---

# Step 5 — Train the Model

Run the training script:

```bash
python train_model.py
```

Expected output:

- dataset loading message
- training progress
- model accuracy
- model saved confirmation

---

# Step 6 — Verify Generated Files

List files in the container:

```bash
ls -l
```

You should see:

```
iris_model.joblib
training_log.txt
train_model.py
```

---

# Step 7 — Inspect Output Files

View the training log:

```bash
cat training_log.txt
```

Example contents:

```
Model: Random Forest Classifier
Estimators: 100
Accuracy: 0.96
Training samples: 120
```

---

# What This Demonstrates

This exercise demonstrates several important container concepts for machine learning workflows:

### Containerized ML Training

Training models inside containers ensures a **consistent and reproducible environment**.

### Dependency Isolation

Libraries are installed only inside the container environment.

### Experiment Reproducibility

The same container image can reproduce identical training results.

### Lightweight ML Environments

Using `python:3.11-slim` keeps the environment small and efficient.

---

# Limitations of This Approach

In this simple example:

- The trained model exists **only inside the container**
- If the container is deleted, the model will be lost

In real workflows, we typically use:

- **Docker volumes**
- **Artifact storage**
- **ML experiment tracking tools**

to persist models.

---

# Possible Improvements

This example can be extended by:

- Mounting a **Docker volume** to save trained models
- Building a **custom Docker image for training**
- Using **Docker Compose for ML pipelines**
- Integrating **MLflow for experiment tracking**
- Automating training through CI/CD pipelines

---

# Purpose

This project was created as a **hands-on exercise to understand how machine learning workloads can run inside Docker containers**, which is a fundamental concept in **MLOps and reproducible machine learning systems**.