# Nutri Paola

Nutri Paola is a comprehensive web application designed to help nutritionists efficiently manage their clients, streamline intake forms, and track client progress over time. The platform features two distinct portals for Nutritionists and Clients, ensuring a tailored and secure experience for both.

## 🛠 Tech Stack

- **Backend:** FastAPI (Python)
- **Frontend:** React.js
- **Database:** PostgreSQL

---

## ✨ Key Features

### 🔐 User Authentication & Roles
The application supports two distinct user roles:
1. **Client:** Clients can register, log in, submit their intake forms, and view their personalized plans and progress.
2. **Nutritionist:** Nutritionists have a centralized dashboard to manage all their clients, review intake forms, and assign plans.

### 📋 Detailed Intake Forms
Clients submit an extensive intake form directly to their nutritionist upon joining. The form captures critical details, including:
- Personal & Medical Information
- Family History
- Lifestyle & Physical Activity
- Current Diet & Nutrition
- Allergies & Food Preferences

### 👩‍⚕️ Client Management
Nutritionists can oversee their entire client roster with robust tools:
- **Workout Plans:** Create, assign, and manage personalized workout routines for each client.
- **Meal Plans:** Design and distribute tailored nutritional plans.
- **Progress Tracking:** Monitor client goals and health metrics.
- **History Logs:** Maintain a comprehensive historical record of each client's past meal plans, workout plans, and progress logs.

---

## 🚀 Getting Started (Backend API)

### Prerequisites
- Python 3.9+
- PostgreSQL
- Git

### Installation

1. **Clone the repository and enter the directory:**
   ```bash
   git clone <your-repo-url>
   cd nutri_paola
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install backend dependencies:**
   ```bash
   pip install -r api/requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and configure your settings:
   ```ini
   DATABASE_URL=postgresql://user:password@localhost/dbname
   SECRET_KEY=your-super-secret-key-for-jwt
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   AVAILABLE_SCOPES={"me": "Read information about the current user.", "admin": "Admin access."}
   DEFAULT_SCOPES=["me"]
   ```

5. **Run the Development Server:**
   ```bash
   uvicorn api.app:app --reload
   ```

6. **View API Documentation:**
   Once the server is running, navigate to `http://localhost:8000/docs` to view the interactive Swagger API documentation.