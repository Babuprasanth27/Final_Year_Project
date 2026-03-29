# 🚀 Full Stack Dockerized Application (Frontend + Backend)

## 📌 Project Description

This project is a containerized full-stack web application consisting of:

* 🎯 **Frontend** – User interface built using modern web technologies(Streamlit)
* ⚙️ **Backend** – API service (FastAPI) handling business logic
* 🧠 **Machine Learning and Deep learning Model** – Integrated into backend for predictions
* 🐳 **Dockerized Setup** – Entire application runs using Docker & Docker Compose

The application demonstrates how to build, containerize, and deploy scalable applications using modern DevOps practices.
<img width="1024" height="1536" alt="ChatGPT Image Mar 14, 2026, 04_39_44 PM" src="https://github.com/user-attachments/assets/18c792d9-dc04-444a-9cda-838152e401fb" />

---

## 🏗️ Architecture Diagram
<img width="1024" height="1536" alt="Hybrid intrusion detection system flowchart" src="https://github.com/user-attachments/assets/1731325b-35b4-4f70-8f0e-7924dfc371bb" />

```
            ┌───────────────┐
            │   Frontend    │
            │  (Streamlit)  │
            └──────┬────────┘
                   │ HTTP Request
                   ▼
            ┌───────────────┐
            │   Backend     │
            │  (FastAPI)    │
            └──────┬────────┘
                   │
        ┌──────────▼──────────┐
        │ ML Model/ DL Model  │
        └─────────────────────┘

        (All services are containerized using Docker)
```

---

## 🧰 Tech Stack

* Frontend: Streamlit
* Backend: FastAPI (Python)
* Machine Learning: Random Forest, Support Vector Machine(SVM), XGBoost, KMeans
* Deep Learning: Artificial Neural Network (ANN)
* Containerization: Docker, Docker Compose

---
<img width="940" height="970" alt="image" src="https://github.com/user-attachments/assets/9f563793-0ca8-4b1f-a236-19fbf53f8e6f" />

## ⚙️ Setup Instructions

### 🔹 Prerequisites

Make sure you have installed:

* Docker
* Docker Compose

---

### 🔹 Step 1: Clone Repository

```bash
git clone https://github.com/Babuprasanth27/Final_Year_Project/
cd Final_Year_Project  --(Main Directory)
**To run Backend in local machine**
1) cd backend
2).\venv\Scripts\Activate.ps1
3) uvicorn app.api:app --reload
**To run Frontend in Local Machine**
1) cd frontend
2) streamlit run streamlit_app.py

Other folders like **Simple,react_ui and ui** are used for testing purpose
```

---

### 🔹 Step 2: Run Application using Docker Compose

```bash
docker compose up --build
```

---

### 🔹 Step 3: Access Application

* Frontend → http://localhost:3000
* Backend API → http://localhost:8000

---

## 🐳 Docker Commands

### 🔹 Build Images

```bash
docker compose build
```

### 🔹 Start Containers

```bash
docker compose up
```

### 🔹 Run in Detached Mode

```bash
docker compose up -d
```

### 🔹 Stop Containers

```bash
docker compose down
```

### 🔹 View Running Containers

```bash
docker ps
```

---
## Pages/UI
<img width="940" height="364" alt="image" src="https://github.com/user-attachments/assets/6f4ec9b6-0d80-4496-88a8-92469179675f" />
<img width="944" height="414" alt="image" src="https://github.com/user-attachments/assets/882625d7-dcff-4658-8c2e-9e2e265d08c9" />
<img width="940" height="389" alt="image" src="https://github.com/user-attachments/assets/a5cdcde6-da8a-4349-880d-3f9eb3fbc81e" />
<img width="940" height="450" alt="image" src="https://github.com/user-attachments/assets/451a333f-4736-44b5-92b9-cc975636d378" />
<img width="940" height="397" alt="image" src="https://github.com/user-attachments/assets/fd7f9ad0-afd1-414b-bd79-0dcd57f72454" />
<img width="940" height="386" alt="image" src="https://github.com/user-attachments/assets/fcdae6a0-1d10-47e6-be23-cbd445ba6b96" />
<img width="940" height="397" alt="image" src="https://github.com/user-attachments/assets/87e75978-8cb2-4cd3-a69b-fcb5b675b229" />



## 🧠 Key Features

* Full containerized architecture
* ML and DL model integration
* Easy deployment using Docker Hub

---

## 📌 Conclusion

This project demonstrates real-world DevOps practices including containerization, service orchestration, and deployment using Docker.

---

## 👨‍💻 Author

**Your Name**
Babuprasanth R
