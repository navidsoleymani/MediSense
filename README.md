# 🚀 MediSense

> A scalable, secure, and machine-learning-driven platform for medical data ingestion and clinical insight delivery. Built with Django, MongoDB, XGBoost, and JWT authentication.

---

## 📚 Table of Contents

* [📝 Introduction](#-introduction)
* [🌟 Features](#-features)
* [🛠️ Technology Stack](#-technology-stack)
* [🏗️ Project Structure](#-project-structure)
* [⚙️ Installation](#-installation)
* [▶️ Running the Application](#-running-the-application)
* [📡 API Endpoints](#-api-endpoints)
* [🧪 Example Usage](#-example-usage)
* [📦 Postman Collection](#-postman-collection)
* [🧪 Testing](#-testing)
* [🔒 Authentication](#-authentication)
* [📄 License](#-license)
* [📞 Contact](#-contact)

---

## 📝 Introduction

MediSense offers an end-to-end pipeline for smart healthcare analysis:

* Imports CSV-based clinical data (longitudinal + cross-sectional)
* Cleans, transforms, and encodes features using Sklearn pipelines
* Trains XGBoost classification models
* Delivers results via secure DRF API endpoints
* Persists trained model metrics into MongoDB for versioning
* Uses JWT (SimpleJWT) to secure all API interactions

---

## 🌟 Features

* 🧾 CSV importer via `import_csv` management command
* 🧠 Sklearn + XGBoost preprocessing & classification pipeline
* 🗂️ MongoDB document schema: `LongData`, `CrossData`, `ModelResult`
* 📊 API endpoints to view training results and predicted probabilities
* ♻️ Re-train model on demand (`POST /api/v1/medicaldataanalysts/train/`)
* 💾 Save and retrieve past model runs (`/results/`, `/results/<id>/`)
* 🔒 JWT-secured access for all API endpoints
* 🌍 Bilingual support (English & Persian)
* 📥 Postman collection available for testing

---

## 🛠️ Technology Stack

| Technology   | Role                    | Version  |
| ------------ | ----------------------- | -------- |
| Python       | Programming Language    | 3.12.x   |
| Django       | Web Framework           | 5.2.x    |
| DRF          | REST API Layer          | latest   |
| MongoDB      | Document-based database | 6.x      |
| mongoengine  | MongoDB ORM             | latest   |
| Scikit-learn | Data preprocessing      | 1.3+     |
| XGBoost      | ML classifier engine    | 2.x      |
| Redis        | Caching / rate-limiting | optional |
| Docker       | Containerization        | 20.x+    |

---

## 🏗️ Project Structure

```bash
MediSense/
├── auth/                      # JWT + user registration
├── config/                    # Core settings, URLs, environments
│   ├── settings/              # dev/prod/test configs
│   └── interfaces/            # API versioning (v1)
├── medicaldataanalysts/      # ML logic, views, data models
│   ├── services.py            # ML pipeline (Sklearn + XGBoost)
│   ├── documents.py           # MongoEngine schemas
│   └── views.py               # DRF APIViews
├── manage.py
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh             # Gunicorn launcher
├── requirements.txt
├── SAMPLE_ENV.txt
├── docs/
│   └── APIs.postman_collection.json
└── tests/                     # Pytest-based unit & integration tests
```

---

## ⚙️ Installation

### Prerequisites

* Python 3.12+
* MongoDB (local or Atlas URI)
* Redis (optional, for cache/throttle)
* Docker (for containerized setup)

### Local Setup

```bash
git clone https://github.com/navidsoleymani/MediSense.git
cd MediSense

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp SAMPLE_ENV.txt .env
# Then update MONGO_URI, SECRET_KEY, REDIS config, etc.
```

### Import Sample Data

```bash
python manage.py import_csv --data-dir=./data
```

---

## ▶️ Running the Application

### Locally

```bash
python manage.py runserver
```

### With Docker Compose

```bash
docker-compose up --build
```

* App: [http://localhost:8000](http://localhost:8000)
* Mongo Express: [http://localhost:8081](http://localhost:8081)

---

## 📡 API Endpoints

| Method | Endpoint                                    | Purpose                              |
| ------ | ------------------------------------------- | ------------------------------------ |
| GET    | `/api/v1/medicaldataanalysts/result/rf/`    | Classification report                |
| GET    | `/api/v1/medicaldataanalysts/result/y/`     | Prediction probabilities             |
| GET    | `/api/v1/medicaldataanalysts/data/`         | Cleaned dataset                      |
| POST   | `/api/v1/medicaldataanalysts/train/`        | Train a new ML model                 |
| POST   | `/api/v1/medicaldataanalysts/result/add/`   | Persist trained model result to DB   |
| GET    | `/api/v1/medicaldataanalysts/results/`      | List stored model results            |
| GET    | `/api/v1/medicaldataanalysts/results/<id>/` | Retrieve specific model result by ID |
| POST   | `/api/v1/auth/register/`                    | Register a new user                  |
| POST   | `/api/v1/auth/login/`                       | Obtain JWT token                     |
| POST   | `/api/v1/auth/login/refresh/`               | Refresh the JWT access token         |
| GET    | `/api/v1/health/`                           | Health check endpoint                |

---

## 🧪 Example Usage (cURL)

```bash
# Register a new user
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "StrongPass123!", ...}'

# Authenticate and get token
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "StrongPass123!"}'

# Use token to fetch results
curl -H "Authorization: Bearer <ACCESS_TOKEN>" \
  http://localhost:8000/api/v1/medicaldataanalysts/result/rf/
```

---

## 📦 Postman Collection

> Located at: `docs/APIs.postman_collection.json`

Import this file into Postman to test endpoints:

* 🔐 Auth & token
* 🧠 Train model
* 📊 Get predictions
* 💾 Save & fetch results

---

## 🧪 Testing

```bash
pytest
```

* Unit + integration tests using `pytest`
* Coverage includes API views, auth, ML service layer

---

## 🔒 Authentication

* All sensitive endpoints require a **JWT token**.
* Auth flow is powered by `rest_framework_simplejwt`.

| Endpoint                      | Purpose       |
| ----------------------------- | ------------- |
| `/api/v1/auth/login/`         | Obtain JWT    |
| `/api/v1/auth/login/refresh/` | Refresh token |

---

## 📄 License

MIT License — see `LICENSE` file.

---

## 📞 Contact

**Navid Soleymani**
📧 [navidsoleymani@ymail.com](mailto:navidsoleymani@ymail.com)
🔗 [github.com/navidsoleymani](https://github.com/navidsoleymani)

<p align="center"><em>Built for intelligent, secure, and scalable medical data pipelines. 🧠</em></p>
