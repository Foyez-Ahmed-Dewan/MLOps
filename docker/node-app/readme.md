# Node.js + MongoDB Multi-Container Docker Application

This project demonstrates how to build and run a **multi-container application using Docker Compose** with persistent storage.

The application allows users to submit their **username and email through a web form**, which is stored in a **MongoDB database**. The system also includes **Mongo Express**, a web interface for viewing the database.

The goal of this project is to practice key Docker concepts such as:

- Multi-container architecture
- Container networking
- Docker volumes for persistent data
- Docker Compose orchestration

---

# Project Architecture

The application consists of three containers:

1. **Node.js Application**
   - Serves a simple web form
   - Accepts user input
   - Stores data in MongoDB

2. **MongoDB Database**
   - Stores submitted user data
   - Uses a Docker volume for persistent storage

3. **Mongo Express**
   - Web-based interface to view MongoDB data

### Architecture Diagram

```
Browser
   |
   | HTTP Request
   v
Node.js Container (Express App)
   |
   | MongoDB Driver
   v
MongoDB Container
   |
   | Persistent Storage
   v
Docker Volume (mongo-data)

Browser
   |
   | HTTP Request
   v
Mongo Express Container
   |
   v
MongoDB Container
```

---

# Project Structure

```
node-app
│
├── app
│   ├── server.js
│   ├── package.json
│   └── views
│       └── form.html
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
└── README.md
```

---

# Prerequisites

Before running the project, ensure the following tools are installed:

- Docker
- Docker Compose
- Node.js (optional for local testing)

Check installation:

```bash
docker --version
docker compose version
```

---

# Step 1 — Clone or Create the Project

```bash
mkdir node-app
cd node-app
```

Create the project structure as shown above.

---

# Step 2 — Install Node Dependencies

Navigate to the application folder:

```bash
cd app
npm install
```

This installs all required dependencies for the Node.js application.

---

# Step 3 — Build and Start Containers

From the project root directory:

```bash
docker compose up --build
```

Docker Compose will:

1. Build the Node.js image using the Dockerfile
2. Pull the MongoDB image
3. Pull the Mongo Express image
4. Create a Docker network for communication
5. Create a Docker volume for MongoDB data
6. Start all containers

---

# Step 4 — Verify Running Containers

Check running containers:

```bash
docker ps
```

You should see three containers:

- Node application
- MongoDB
- Mongo Express

---

# Step 5 — Access the Application

Open the web application in your browser:

```
http://localhost:3000
```

Submit a username and email through the form.

---

# Step 6 — View Data Using Mongo Express

Open Mongo Express:

```
http://localhost:8081
```

Navigate to:

```
userdb → users
```

You should see the inserted user records.

---

# Step 7 — Verify Docker Volume

List Docker volumes:

```bash
docker volume ls
```

You should see:

```
mongo-data
```

Inspect the volume:

```bash
docker volume inspect mongo-data
```

This volume stores MongoDB data and ensures **data persistence even if containers stop or restart**.

---

# Step 8 — Stop Containers

To stop the application:

```bash
docker compose down
```

Containers will stop but **database data remains stored in the Docker volume**.

---

# Key Docker Concepts Demonstrated

This project demonstrates several important Docker concepts:

### Multi-Container Applications

Using Docker Compose to manage multiple services together.

### Container Networking

Containers communicate using **service names instead of localhost**.

### Persistent Data with Volumes

MongoDB data is stored in a **Docker volume**, ensuring data is not lost when containers restart.

### Docker Image Building

The Node.js application is packaged into a Docker image using a **Dockerfile**.

---

# Access URLs

Application:

```
http://localhost:3000
```

Mongo Express Dashboard:

```
http://localhost:8081
```

---

# Purpose

This project was built as a **Docker practice exercise** to understand how containerized services interact in a real-world architecture.

It focuses on learning **Docker networking, volumes, and service orchestration using Docker Compose**.