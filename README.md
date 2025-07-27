# Youth Club Community Service Tracker 🕒📚

Welcome to the **Youth Club Community Service Tracker** — a sleek, web-based app designed to modernize how student clubs track their community service hours. No more messy pen-and-paper logs or lost signatures! This app makes logging, viewing, and managing service hours easy, efficient, and secure. 💻✨

While it’s built specifically for our club’s needs, it’s open source and fully customizable — so clubs anywhere can fork, rebrand, and adapt it for their own students worldwide. 🌍

---

## 🚀 Why This App Exists

Many student clubs still track service hours with archaic paper forms that are easy to lose, hard to manage, and a pain to total up. This app solves that problem by offering an easy-to-use online system where students can:

- Register and log in securely 🔐
- Add detailed service tasks with descriptions, dates, and proof images 🖼️
- View their accumulated hours at a glance 📊
- Admins can manage users and tasks via protected pages 👮‍♂️

---

## ✨ Features

- **User authentication:** Register, login, logout — with secure password hashing 🔑  
- **Role-based access:** First 7 registered users are granted admin privileges automatically (manage users, nuke database, view all tasks). Everyone else is a normal user.  
- **Service logging:** Students log tasks with description, hours, date, and upload photo proof 📸  
- **Task management:** Users can add and delete their own tasks; admins can view and manage all tasks and users  
- **Email contact form:** Students and visitors can send messages to club officers via a contact form with multi-recipient emails ✉️  
- **Bootstrap 5 styling:** Clean, responsive UI built with Flask-Bootstrap 🎨  

---

## 🛠️ Setup Instructions (Local Development)

### 🔧 Prerequisites

- Python 3.8+ installed
- `pip` (Python package manager)
- A Gmail account (for contact form email sending)
- Git (to clone the repository)

---

### 📦 Installation Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
2. **Install Dependencies**
   Make sure you have a virtual env (optional but recommended)
   `
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   `
3. **Create an .env file**
   - NOTE: **First 7 users** have ADMIN priveledges.
   `
   FLASK_KEY=your_flask_secret_key
   MY_EMAIL_FOR_USER=your_email@gmail.com
   MY_PASS_FOR_USER=your_email_password
   OFFICER_1_EMAIL=officer1@example.com
   OFFICER_2_EMAIL=officer2@example.com
   OFFICER_3_EMAIL=officer3@example.com
   OFFICER_4_EMAIL=officer4@example.com
   OFFICER_5_EMAIL=officer5@example.com
   OFFICER_6_EMAIL=officer6@example.com
   OFFICER_7_EMAIL=officer7@example.com
   MY_PERSONAL_EMAIL=your_personal_email@example.com
   DATABASE_URL=sqlite:///site.db
   `
5. **Create the database (one-time thing)**
  - Run the below from root directory:
  - `python create_tables.py`
6. **Run the Main.py**
  - `python main.py`
7. **Enjoy!**
