<div align="center">

# 🚀 MetroVPS Assignment

### Subscription & Exchange Rate API System

[![Django](https://img.shields.io/badge/Django-5.2.4-092E20?style=for-the-badge\&logo=django\&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-20.10+-2496ED?style=for-the-badge\&logo=docker\&logoColor=white)](https://www.docker.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.4-4479A1?style=for-the-badge\&logo=mysql\&logoColor=white)](https://www.mysql.com/)
[![Redis](https://img.shields.io/badge/Redis-7.2-DC382D?style=for-the-badge\&logo=redis\&logoColor=white)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Celery-5.5.3-37B24D?style=for-the-badge\&logo=celery\&logoColor=white)](https://docs.celeryproject.org/)

A clean and production-grade Django REST API for managing subscriptions and real-time currency exchange rates.

</div>

## 🌟 Features

| Feature                 | Description                                   |
| ----------------------- | --------------------------------------------- |
| **JWT Auth**            | Secure registration, login, and user profiles |
| **Plan Management**     | Full CRUD for subscription plans              |
| **Live Exchange Rates** | Realtime conversion using external API        |
| **Async Tasks**         | Background jobs via Celery & Redis            |
| **Rate Logs**           | Tracks and logs exchange history              |
| **Dockerized**          | Fully containerized microservice setup        |
| **Auto Docs**           | Rich API documentation with examples          |

---

## 🛠️ Tech Stack

| Backend          | Database & Cache | Task Queue | DevOps                 |
| ---------------- | ---------------- | ---------- | ---------------------- |
| Django, DRF, JWT | MySQL, Redis     | Celery     | Docker, Docker Compose |

---

## 🚀 Quick Start

**Requirements:** Docker + Docker Compose

### 🔧 Setup

```bash
# Clone repo
$ git clone https://github.com/adib-the-noob/metro-vps-assignment.git
$ cd metro-vps-assignment

# Stop local services if conflicting
$ sudo systemctl stop redis-server mysql

# Add your .env file to the app/ directory
```

**.env File:** [Download here](https://drive.google.com/file/d/11I6ZTbwzH2SsH1HwHlCWQPIkoJY_2VdN/view?usp=drive_link)

### ⚙️ Run Services

```bash
# Build and run
$ docker-compose build
$ docker-compose up -d

# Check services
$ docker ps
```

### 🛠️ Django Setup

```bash
# Enter Django container
$ docker exec -it metro-vps-assignment-web-1 bash

# Run DB migrations and create superuser
$ python manage.py migrate
$ python manage.py createsuperuser
$ exit
```

### 🔗 URLs

| Service | URL                                                          |
| ------- | ------------------------------------------------------------ |
| API     | [http://localhost:8000](http://localhost:8000)               |
| Admin   | [http://localhost:8000/admin](http://localhost:8000/admin)   |
| Health  | [http://localhost:8000/health](http://localhost:8000/health) |

---

## 🐳 Docker Services

| Container     | Service    | Port | Role            |
| ------------- | ---------- | ---- | --------------- |
| `web`         | Django App | 8000 | REST API Server |
| `db`          | MySQL      | 3306 | Main DB         |
| `redis`       | Redis      | 6379 | Caching & Queue |
| `celery`      | Worker     | -    | Async Tasks     |
| `celery-beat` | Scheduler  | -    | Scheduled Tasks |

---

## 📖 API Documentation

Here’s a clean and professional **API documentation** generated from your Postman collection for the **MetroVPS Assignment**:

---

# 📘 MetroVPS API Documentation

> Base URL: `http://localhost:8000`

## 🔐 Authentication APIs

### ▶️ Register User

**POST** `/api/auth/register/`

#### Request Body:

```json
{
  "first_name": "Hacker",
  "last_name": "ADIB",
  "username": "noob",
  "email": "noob@noob.com",
  "password": "hacker"
}
```

#### Responses:

* ✅ **201 Created**

```json
{
  "status": "success",
  "message": "User registered successfully",
  "data": { ... }
}
```

* ❌ **400 Bad Request**

```json
{
  "status": "error",
  "message": "User registration failed",
  "errors": {
    "username": ["Username already exists."],
    "email": ["Email already exists."]
  }
}
```

---

### ▶️ User Login

**POST** `/api/auth/login/`

#### Request Body:

```json
{
  "username": "noob",
  "password": "hacker"
}
```

#### Responses:

* ✅ **200 OK**

```json
{
  "status": "success",
  "message": "User logged in successfully",
  "data": {
    "type": "Bearer",
    "access_token": "<JWT Token>"
  }
}
```

* ❌ **400 Bad Request**

```json
{
  "status": "error",
  "message": "User login failed",
  "errors": {
    "non_field_errors": ["Invalid username or password"]
  }
}
```

---

### ▶️ Get User Profile

**GET** `/api/auth/profile/`

#### Headers:

```
Authorization: Bearer <auth_token>
```

#### Response:

* ✅ **200 OK**

```json
{
  "status": "success",
  "message": "User profile retrieved successfully",
  "data": { ... }
}
```

---

## 📦 Subscription APIs

### ▶️ Get Subscribed Plans

**GET** `/api/subscriptions/`

#### Headers:

```
Authorization: Bearer <auth_token>
```

#### Response:

* ✅ **200 OK**

```json
{
  "status": "success",
  "message": "Subscriptions retrieved successfully.",
  "data": [ ... ]
}
```

---

### ▶️ Subscribe to a Plan

**POST** `/api/subscribe/`

#### Headers:

```
Authorization: Bearer <auth_token>
```

#### Request Body:

```json
{
  "plan_id": 3
}
```

#### Responses:

* ✅ **200 OK**

```json
{
  "status": "success",
  "message": "Subscription created successfully.",
  "data": { ... }
}
```

* ❌ **400 Bad Request** (already subscribed)

```json
{
  "status": "error",
  "message": "You are already subscribed to this plan and it is still active.",
  "data": { ... }
}
```

* ❌ **400 Bad Request** (invalid plan)

```json
{
  "status": "error",
  "message": "Invalid data provided.",
  "errors": {
    "non_field_errors": ["Plan with this ID does not exist."]
  }
}
```

---

### ▶️ Unsubscribe from a Plan

**POST** `/api/cancel-subscription/`

#### Headers:

```
Authorization: Bearer <auth_token>
```

#### Request Body:

```json
{
  "subscription_id": 3
}
```

#### Responses:

* ✅ **200 OK**

```json
{
  "status": "success",
  "message": "Subscription cancelled successfully.",
  "data": { ... }
}
```

* ❌ **404 Not Found**

```json
{
  "status": "error",
  "message": "Subscription not found!"
}
```

---

## 💱 Exchange Rate API

### ▶️ Compare Exchange Rate

**GET** `/api/exchange-rate/?base_currency=EUR&target_currency=USD`

#### Headers:

```
Authorization: Bearer <auth_token>
```

#### Response:

* ✅ **200 OK**

```json
{
  "status": "success",
  "message": "Exchange rate retrieved successfully.",
  "data": {
    "base_currency": "EUR",
    "target_currency": "USD",
    "rate": 1.1511,
    "timestamp": "2025-08-03T15:33:51.129413+00:00"
  }
}
```

---

## 🩺 Health Check

**GET** `/health`

#### Response:

```json
{
  "status": "ok"
}
```