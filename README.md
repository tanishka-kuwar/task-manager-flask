#  📝 Task Manager Web App

A full-stack task management application built using **Flask**, **MySQL**, and **Bootstrap**.

## 🚀 Features
- User authentication (Register / Login / Logout)
- Add, edit, delete tasks
- Mark tasks as completed or pending
- Task categories (Work, Personal, Study, General)
- Filter tasks by status, priority, and category
- Clean and responsive UI using Bootstrap
- Secure session-based access

## 🛠 Tech Stack
- Backend: Flask (Python)
- Frontend: HTML, CSS, Bootstrap
- Database: MySQL
- Authentication: Werkzeug security

## 📂 Project Structure
task-manager-flask/
│
├── app.py
├── templates/
│ ├── base.html
│ ├── login.html
│ ├── register.html
│ ├── dashboard.html
│ └── edit_task.html
├── static/
│ └── css/
├── requirements.txt
└── README.md


## ⚙️ Setup Instructions
Create virtual environment

python -m venv venv
venv\Scripts\activate
Install dependencies

pip install -r requirements.txt
Configure MySQL database and update credentials

Run the app
python app.py

👤 Author
Tanishka Kuwar


Commit it:
```bash
git add README.md
git commit -m "Add README"
git push
