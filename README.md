# 📧 J3Mail Backend

This is the backend for **J3Mail**, a secure, end-to-end encrypted mailing system that ensures confidentiality, integrity, and authenticity of messages.

The backend is built with **Django**, **Django Rest Framework**, and **MongoDB**, and implements multiple layers of cryptography (RSA, AES, and digital signatures) to protect user data.

## 🔗 Application

[J3Mail]()

## Frontend Repository

👉 [https://github.com/nizamsalim/j3mail_frontend](https://github.com/nizamsalim/j3mail_frontend)

---

## 🚀 Features

- 🔐 RSA-based authentication flow
- 📬 Encrypted email handling using AES (per-mail session keys)
- 🔑 RSA key management per user (keys stored securely)
- ✍️ Digital signatures for authenticity
- 🌐 RESTful APIs powered by Django Rest Framework
- 🗄 MongoDB database support

---

## 🛠 Installation (Local)

### 1. Clone the Backend Repo

```bash
git clone https://github.com/nizamsalim/j3mail_backend.git
cd j3mail_backend
```

### 2. Set up virtual environment

```bash
python -m venv env
env\Scripts\activate
```

### 3. Dependency installation

```bash
pip install -r requirements.txt
```

### 4. Running Development Server

```bash
python manage.py runserver
```

Ensure to set the following env variables in `.env` file

```env
PUBLIC_KEY="-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"
PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----"
DJANGO_SECRET_KEY="..."
DEBUG=False
MONGODB_URI="..."
```
