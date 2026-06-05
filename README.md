# 🥔 Potato Disease Classification

End-to-end deep learning project for potato leaf disease detection using **TensorFlow/Keras**, **FastAPI**, and **React**.

This application allows users to upload a potato leaf image and predicts whether the leaf is:

* Early Blight
* Late Blight
* Healthy

along with a confidence score.

---

# 🚀 Live Demo

## Frontend
https://potato-disease-classification-60s5q9dck.vercel.app/

## Backend API
https://vaibhavnayak-potato-disease-api.hf.space/prediction

---

# 📌 Features

* Upload potato leaf images
* Deep learning image classification
* FastAPI REST API backend
* React frontend with drag-and-drop upload
* Confidence percentage display
* Dockerized backend deployment
* Free cloud deployment

---

# 🧠 Problem Statement

The goal of this project is to identify potato leaf diseases from images using deep learning.

The model classifies images into:

* Early Blight
* Late Blight
* Healthy

This project demonstrates an end-to-end machine learning workflow including:

* Data preprocessing
* Model training
* API development
* Frontend integration
* Cloud deployment

---

# 🏗️ Project Architecture

```text
React Frontend
       ↓
FastAPI Backend
       ↓
TensorFlow/Keras Model
```

---

# 📂 Project Structure

```text
Potato-disease/
│
├── api/                     # Local FastAPI backend
├── deploy-api/              # Deployment-ready backend
├── frontend/                # React frontend
├── saved_models/            # Trained Keras models
├── training/                # Model training notebooks/scripts
├── docs/                    # Documentation
├── tools/                   # Helper scripts
│
├── potatoes.keras           # Saved Keras model
├── potatoes.h5              # Saved H5 model
├── Dockerfile               # Docker configuration
├── requirements.txt         # Python dependencies
└── README.md
```

---

# 🧪 Model Information

The CNN model was trained using potato leaf images categorized into:

* Early Blight
* Late Blight
* Healthy

## Model Input

* Image size: `256 x 256`
* RGB images

## Model Output

* Predicted disease class
* Confidence score

---

# ⚙️ Backend - FastAPI

The backend was built using FastAPI and TensorFlow.

## API Endpoints

### Health Check

```http
GET /
```

Response:

```json
{
  "message": "Potato Disease API Running"
}
```

---

### Prediction Endpoint

```http
POST /prediction
```

Accepts:

* Image file upload

Returns:

```json
{
  "prediction": "Early Blight",
  "confidence": 0.98
}
```

---

# 🎨 Frontend - React

The frontend was developed using React and Material UI.

## Features

* Image upload
* Drag-and-drop support
* Prediction result display
* Confidence percentage
* Responsive UI

---

# 🛠️ Tech Stack

| Layer      | Technologies                        |
| ---------- | ----------------------------------- |
| Model      | Python, TensorFlow, Keras           |
| Backend    | FastAPI, Uvicorn, Pillow, NumPy     |
| Frontend   | React, Axios, Material UI           |
| Deployment | Hugging Face Spaces, Docker, Vercel |

---

# 🐳 Docker Deployment

The backend API is deployed using Docker on Hugging Face Spaces.

## Run Locally Using Docker

```bash
docker build -t potato-api .
```

```bash
docker run -p 8000:8000 potato-api
```

---

# 💻 Local Setup

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/potato-disease-classification.git
```

```bash
cd potato-disease-classification
```

---

# 🔧 Backend Setup

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Start FastAPI Server

```bash
cd api
```

```bash
uvicorn main:app --reload
```

Backend runs on:

```text
http://localhost:8000
```

Swagger docs:

```text
http://localhost:8000/docs
```

---

# 🎨 Frontend Setup

## Install Dependencies

```bash
cd frontend
```

```bash
npm install
```

---

## Create Environment File

Create:

```text
frontend/.env
```

Add:

```env
REACT_APP_API_URL=http://localhost:8000/prediction
```

---

## Start Frontend

```bash
npm start
```

Frontend runs on:

```text
http://localhost:3000
```

---

# ☁️ Deployment

## Backend Deployment

Platform:

* Hugging Face Spaces

Tech:

* Docker
* FastAPI
* TensorFlow

---

## Frontend Deployment

Platform:

* Vercel

### Important

Set Vercel Root Directory to:

```text
frontend
```

---

# 📸 How To Test

1. Open the React frontend
2. Upload a potato leaf image
3. Wait for prediction
4. View disease label and confidence score

---

# 📖 Learning Outcomes

This project helped demonstrate:

* CNN image classification
* TensorFlow/Keras model serving
* FastAPI REST API development
* React frontend integration
* Environment variables
* Docker deployment
* Full-stack ML deployment

---

# 🙌 Credits

Special thanks to:

* Codebasics
* Dhaval Patel

for the learning resources and inspiration behind this project.

---

# ⚠️ Disclaimer

This project is built for learning and demonstration purposes.

Real agricultural diagnosis should always involve expert verification and field-level analysis.

---

# 👨‍💻 Author

## Vaibhav Nayak

* LinkedIn: https://www.linkedin.com/in/vaibhav-nayak03/
