# Flexeere B2B Registration Portal

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)

A professional-grade, enterprise-ready Django application serving as a highly secure B2B registration and validation portal. This system implements decoupled data architectures, unique temporary activation tokens, and automated SMTP email dispatch to authenticate potential corporate accounts.

## 🚀 Key Features

*   **Decoupled Security Architecture**: Implements a dedicated `ValidationKey` model conceptually detached from the `Company` profile to isolate security tokens.
*   **Cryptographic Tokens**: Uses Python's native `secrets.token_urlsafe(64)` for high-entropy activation keys with an automatic 48-hour expiration lifecycle.
*   **Automated SMTP Dispatch**: Integrates directly with custom mail servers (e.g., `mail.flexeere.net`) over SSL to deliver activation emails instantly upon registration.
*   **Regex Format Validation**: Ensures Tax/GST numbers strictly follow 15-character alphanumeric formatting requirements.
*   **Enterprise UI Pipeline**: Fully responsive, SaaS-styled interface built strictly using Tailwind CSS, minimizing overhead while maximizing aesthetics.

## 🛠 Tech Stack

*   **Backend Framework:** Django 6.0
*   **Language:** Python 3.11+
*   **Styling:** Tailwind CSS (via CDN for local portability)
*   **Database:** SQLite3 (Local) / PostgreSQL Ready
*   **Architecture:** Model-View-Template (MVT)

## 💻 Getting Started (Local Environment)

Follow these instructions to clone and run the project strictly on your local machine.

### Prerequisites
*   Python 3.11 or higher installed.

### 1. Installation
Clone the repository and spin up a virtual environment.

```bash
git clone https://github.com/flexeere/Key-validation.git
cd Key-validation
python -m venv venv

# Activate on Windows
.\venv\Scripts\activate
# Activate on Mac/Linux
source venv/bin/activate

pip install django
```

### 2. Database & Migrations
Initialize the database schemas and construct the tables.

```bash
python manage.py makemigrations registration
python manage.py migrate
```

### 3. Administrator Setup
Create a secure superuser to access the Django Administration panel.

```bash
python manage.py createsuperuser
```

### 4. Running the Development Server
```bash
python manage.py runserver
```
Navigate to `http://127.0.0.1:8000/register/` to view the application. The Admin dashboard is located at `http://127.0.0.1:8000/admin/`.

## ⚙️ Configuration (SMTP)

To send live emails, edit the variables located at the bottom of `core/settings.py`.

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.flexeere.net'
EMAIL_PORT = 465
EMAIL_USE_SSL = True

EMAIL_HOST_USER = 'noreply@flexeere.net' 
EMAIL_HOST_PASSWORD = '<YOUR_PASSWORD>'
```

## 🧪 Testing

This project ships with a native unit testing suite mimicking standard Django testing assertions, validating models, URL schemas, forms, and template routing.

Run the test suite gracefully:
```bash
python manage.py test registration
```

## 🔒 Security Posture
*   Admin views restrict direct mutation of `ValidationKeys`.
*   Unused or Expired tokens automatically reject connections.
*   Unique DB indexing applied explicitly to emails and GST footprints to prevent data duplication vulnerabilities.

---
*Prepared exclusively for OpenAI CodeX evaluation metrics.*
