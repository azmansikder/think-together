# Think Together 🎓🔬

Think Together is a Django-based collaboration platform designed to bridge the gap between students and researchers. It allows users to register based on their roles, create and browse research projects, and communicate seamlessly via a built-in messaging system.

## ✨ Features
* **Role-Based Authentication:** Separate registration and login flows for Students and Researchers.
* **Custom Dashboards:** Tailored dashboard experiences showing relevant stats (Total Posts, Active Projects, Pending Collaborations).
* **Project Management:** Students can create projects, and researchers can post research topics.
* **Real-time Collaboration:** Built-in messaging system for seamless communication between users.

## 📸 Screenshots

### User Registration
Users can join the community by selecting their specific role (Student or Researcher).
<p align="center">
  <img src="C:\Users\I dont know\OneDrive\Pictures\Screenshots\student_register.png" width="45%" alt="Student Registration">
  <img src="C:\Users\I dont know\OneDrive\Pictures\Screenshots\researcher_register.png" width="45%" alt="Researcher Registration">
</p>

### Custom Dashboards
#### Student Panel
Students can manage their projects, browse latest research, and track their saved items.
![Student Dashboard](screenshots/student_dashboard.png)

#### Researcher Panel
Researchers can monitor their published posts, total views, and pending collaboration requests.
![Researcher Dashboard](screenshots/researcher_dashboard.png)

### Messaging System
Direct communication interface between students and researchers.
![Messaging Interface](screenshots/messaging.png)

## 🛠️ Tech Stack
* **Backend:** Django (Python)
* **Frontend:** HTML, CSS, Bootstrap
* **Database:** SQLite (Development) / PostgreSQL (Production)

## 🚀 Local Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/think-together.git](https://github.com/yourusername/think-together.git)
   cd think-together
2. **Create and activate a virtual environment:**

Bash
python -m venv env
# On Windows:
env\Scripts\activate
# On Mac/Linux:
source env/bin/activate
3. **Install dependencies:**

Bash
pip install -r requirements.txt
4. **Apply database migrations:**

Bash
python manage.py migrate
5. **Run the development server:**

Bash
python manage.py runserver
Open http://127.0.0.1:8000/ in your browser.
