# Car Service Prediction Application

A full-stack web application for predicting car service costs and managing vehicle service history.

## Features
- **User Authentication**: Secure login and registration with JWT.
- **Vehicle Management**: Users can add and manage their vehicles.
- **Service Prediction**: Predict service costs based on vehicle details.
- **Service History**: Track service records for each vehicle.
- **Super Admin Dashboard**: Manage users and the vehicle catalog.
- **Vehicle Catalog**: Admin-managed database of vehicle makes and models.

## Prerequisites
- **Python 3.8+**
- **Node.js 16+**
- **npm** (comes with Node.js)

## Installation

### 1. Backend Setup
1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Create a virtual environment:
    ```bash
    python -m venv venv
    ```
3.  Activate the virtual environment:
    - **Windows**: `venv\Scripts\activate`
    - **macOS/Linux**: `source venv/bin/activate`
4.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5.  Create a `.env` file in the `backend` directory (optional, defaults are set in code):
    ```env
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```
6.  Initialize the database and create a superuser:
    ```bash
    # This script initializes the DB and creates the first admin
    python create_superuser.py admin@test.com admin123456
    ```

### 2. Frontend Setup
1.  Navigate to the frontend directory:
    ```bash
    cd frontend/car-service-prediction_FE
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```

## Running the Application

### 1. Start the Backend
In the `backend` directory (with venv activated):
```bash
fastapi dev main.py
```
The API will be available at `http://localhost:8000`. API docs at `http://localhost:8000/docs`.

### 2. Start the Frontend
In the `frontend/car-service-prediction_FE` directory:
```bash
npm run dev
```
The application will be available at `http://localhost:5173`.

## Usage Guide

### Super Admin
- **Login**: Use the credentials created via `create_superuser.py` (e.g., `admin@test.com` / `admin123456`).
- **Dashboard**: Access `/admin/dashboard` to view stats.
- **Catalog**: Go to `/admin/catalog` to add/remove Vehicle Makes and Models.

### Regular User
- **Register**: Create a new account at `/register`.
- **My Vehicles**: Go to `/vehicles` to add your cars. You can select Make/Model from the catalog.
- **Predict**: Use the home page to predict service costs.
- **Profile**: View your profile at `/profile`.

## Troubleshooting
- **Login Redirect Loop**: Ensure you are running the latest code. Admin pages wait for user profile to load.
- **Database Errors**: Delete `sql_app.db` in the backend folder and re-run `create_superuser.py` to reset the database.
