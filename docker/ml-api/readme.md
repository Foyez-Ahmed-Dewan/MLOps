# Dockerized FastAPI ML App (Practice)

This project demonstrates how to **containerize a Machine Learning API using FastAPI and Docker**.  
The workflow includes training a model, exposing prediction endpoints with FastAPI, and packaging the entire application into a Docker container for easy deployment.

---

# Project Workflow

1. Create Python virtual environment
2. Train ML model and save `.pkl`
3. Build FastAPI API
4. Export dependencies (`requirements.txt`)
5. Create `Dockerfile` and `.dockerignore`
6. Build Docker image
7. Run container
8. Publish image to Docker Hub

---

# 1. Create Virtual Environment

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

python3 -m venv .venv
source .venv/bin/activate
```

Install required packages:

```bash
pip install scikit-learn pickle fastapi uvicorn pydantic pandas numpy
```

---

# 2. Train the ML Model

Train your model and save it as a `.pkl` file.

Example:

```bash
python model.py
```

This will generate a trained model file (e.g., `model.pkl`) used for inference.

---

# 3. Create FastAPI Application

Write your API endpoints and load the trained model inside the FastAPI app.

Run the API locally:

```bash
uvicorn main:app --reload
```

Access the API:

```
http://localhost:8000
```

Interactive documentation:

```
http://localhost:8000/docs
```

---

# 4. Generate `requirements.txt`

Export project dependencies:

```bash
pip freeze > requirements.txt
```

---

# 5. Create Docker Configuration

Create:

- `Dockerfile`
- `.dockerignore`

These files define how the application will be packaged and which files should be excluded from the Docker image.

---

# 6. Build Docker Image

Build the Docker image:

```bash
docker build -t img_name:tag .
```

Check created images:

```bash
docker images
```

---

# 7. Run Docker Container

Start a container from the built image:

```bash
docker run --name container_name -p host_port:container_port -d img_name
```

Example:

```bash
docker run --name iris_container -p 8000:5000 -d iris_image
```

---

# 8. Inspect Running Container

To access the container shell:

```bash
docker exec -it container_id bash
```

Check files inside the container:

```bash
ls
```

---

# 9. Publish Image to Docker Hub

Create a repository on Docker Hub and use its name as the image name.

Build image:

```bash
docker build -t username/repository_name .
```

Login to Docker Hub:

```bash
docker login
```

Push image:

```bash
docker push username/repository_name
```

---

# 10. Run the Published Image

Example image:

```
foyez063/iris-test
```

Run container:

```bash
docker run --name cont_name -p 8000:5000 -it -d foyez063/iris-test
```

---

# 11. Access the Deployed API

After the container starts:

1. Go to **Docker Desktop**
2. Navigate to **Containers**
3. Click the **port link**

This will redirect you to the running API service.

---

# Example Project Structure

```
project-root
│
├── main.py
├── model.py
├── model.pkl
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md
```

---

# Technologies Used

- Python
- FastAPI
- Scikit-learn
- Docker
- Uvicorn
- Pydantic
- Pandas / NumPy

---

# Purpose

This project is a **practice exercise for learning MLOps fundamentals**, specifically:

- Packaging ML applications
- API serving with FastAPI
- Containerization using Docker
- Deploying reproducible ML services

---