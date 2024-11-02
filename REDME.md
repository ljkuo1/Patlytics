# Patent Infringement Checker

A web application designed to analyze company products for potential patent infringements using advanced natural language processing techniques.

## Overview

This application utilizes Sentence Transformers for semantic similarity analysis to detect potential overlaps between company products and patent claims. The backend is powered by a RESTful API built with Flask, and the frontend provides an intuitive interface for users with with React and Vite for a fast and responsive user interface.

## Features

- **Patent Analysis**: Identify potential patent infringements based on the semantic similarity between product descriptions and patent claims.
- **Natural Language Processing**: Uses Sentence Transformers for accurate and efficient similarity matching.
- **RESTful API**: Flask-based backend to handle requests and responses.

## Prerequisites

Make sure the following dependencies are installed:

1. **Python**: Required for the backend (preferably Python 3.7+).
2. **Node.js and npm**: Required for running the frontend.

## Installation

1. Backend Setup:

```
cd backend
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

2. Frontend Setup:

```
cd frontend
npm install
```

## Running the Application locally

- Backend (Flask API)
  Start the backend server by running:

  ```
  python app.py
  ```

  The API will be running on `http://127.0.0.1:8080`.

- Frontend (React App)
  In a new terminal, navigate to the frontend directory if not already there:
  ```
  cd frontend
  ```
  Start the frontend by running:
  ```
  npm run dev
  ```
  The app will be running on `http://localhost:5173`.

## Running the Application with Docker

- Build and Run the Docker Container
  Ensure Docker is installed and running on your machine. Then, build and run the Docker container:

  ```
  docker build -t patent-infringement-checker .
  docker run -p 8080:8080 patent-infringement-checker
  ```

  The application will be accessible at `http://localhost:8080`.
