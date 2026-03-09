# Pyn: Modern Security & Developer Toolkit

Pyn is a high-performance, local-first security suite built with **Python**, **Flask**, **HTMX**, and **Tailwind CSS**. It provides professional-grade utilities for password generation, security analysis, and developer workflows—all while maintaining absolute privacy through a zero-knowledge architecture.

## 🚀 Key Features

### 🔐 Password & Passphrase Intelligence
*   **Secure Generator:** Customizable password generation (Length, Charsets) using `secrets` (SystemRandom).
*   **Diceware & Gibberish:** Generate high-entropy passphrases using EFF large wordlists or pronounceable phonetic algorithms.
*   **k-Anonymity HIBP Check:** Query Have I Been Pwned? safely. Passwords are hashed locally; only the first 5 SHA-1 characters are sent to the API.
*   **Real-time Analytics:** Instant entropy calculation, zxcvbn strength scoring, and offline crack-time estimation.

### 🛠️ Developer Utilities (Zero-Knowledge)
*   **Secure Hasher:** Generate Argon2id and Bcrypt hashes with safe salt handling.
*   **Text Utilities:** Real-time MD5, SHA-256, and SHA-512 hashing.
*   **Encoder/Decoder:** Base64, Hex, and URL encoding/decoding.
*   **JWT & JSON:** Decode JWT tokens and format/validate JSON strings locally.
*   **UUID/PIN:** Batch generate UUIDs (v1/v4) and secure numeric PINs.

### 📊 Security Dashboard
*   **Local Analytics:** Track your security habits with an offline dashboard.
*   **Data at Rest Encryption:** All saved metrics are encrypted using **AES-256-GCM** before being stored in the local SQLite database.
*   **Privacy-First UI:** Sensitive data in the activity log is blurred by default and only revealed on hover.

## 🏗️ Architecture

Pyn follows **Domain-Driven Design (DDD)** principles to ensure high maintainability and testability:

*   **`app/core/domain`**: Pure business logic and algorithms (Zero dependencies).
*   **`app/core/application`**: Use-case services and orchestrators.
*   **`app/infrastructure`**: External boundaries (Database, HIBP API, Encryption).
*   **`app/web`**: Reactive delivery mechanism using Flask and HTMX.

## 🛠️ Tech Stack

*   **Backend:** Python 3.11, Flask, SQLAlchemy.
*   **Frontend:** HTMX (AJAX without JS), Tailwind CSS (Premium SaaS UI), Alpine.js (Micro-interactions).
*   **Security:** Cryptography (AES-GCM), Argon2, Bcrypt, zxcvbn.
*   **DevOps:** Docker, Docker Compose, GitHub Actions (CI/CD).

## 🚦 Getting Started

### Prerequisites
*   Docker and Docker Compose

### Fast Deploy (Recommended)
1. Clone the repository.
2. Run the toolkit:
   ```bash
   docker-compose up --build
   ```
3. Open your browser at `http://localhost:5000`.

### Local Development
1. Install dependencies: `pip install -r requirements.txt`
2. Set your encryption key: `export AES_GCM_KEY=your-32-byte-key`
3. Run the app: `flask run`

## 🧪 Testing & Quality
Pyn includes a comprehensive `pytest` suite covering domain algorithms, security logic, and web endpoints.

```bash
# Run tests
pytest tests/

# Format code
black .
ruff check . --fix
```

## 🛡️ Security Policy
Everything in Pyn is **local-only**. No passwords, passphrases, or tokens are ever transmitted to a remote server (except for the k-Anonymized HIBP prefix check). Your data belongs to you.

---
Built with ❤️ for the security community.
