# Pyn: A Comprehensive Password Security Toolkit

## 🔐 Overview

Pyn is a Python-based Flask web application designed to enhance password security. It provides tools for analyzing the strength of existing passwords and generating new, secure passwords. This project is inspired by the [Cygnius Password Test](https://apps.cygnius.net/passtest/).

## 🚀 Key Features

### 🔎 Password Analysis
- Comprehensive strength evaluation
- Entropy calculation
- Crack time estimation
- Complexity assessment
- Pwned password detection via [Have I Been Pwned?](https://haveibeenpwned.com/) API

### 🔧 Password Generation
- Customizable password creation
- Secure random generation
- Multiple character set options
- Configurable length and complexity

## 💡 How it Works

### Password Analysis

Pyn's password analysis goes beyond simple checks, providing a deep dive into a password's resilience:

-   **Entropy Calculation**: Measures the randomness and unpredictability of a password in bits. Higher entropy means a more secure password.
-   **Crack Time Estimation**: Estimates how long it would take for various attack methods to crack a password. This includes:
    -   **Offline Fast Hashing**: Simulates attacks where an attacker has access to hashed passwords and can attempt billions of guesses per second.
    -   **Offline Slow Hashing**: Accounts for slower hashing algorithms designed to resist brute-force attacks.
    -   **Online No Throttling**: Represents attacks against online services without rate limits.
    -   **Online With Throttling**: Simulates attacks against services with rate limiting, significantly slowing down attempts.
    -   **Offline Parallel Attack**: Considers large-scale attacks using multiple machines.
-   **Complexity Assessment**: Checks if a password meets common complexity requirements, such as minimum length, inclusion of uppercase, lowercase, numbers, and special characters, and avoidance of excessive character repeats.
-   **Pwned Password Detection**: Integrates with the "Have I Been Pwned?" API to check if a password has appeared in known data breaches, alerting users to compromised credentials.

### Password Generation

The password generator creates strong, unique passwords based on user-defined criteria:

1.  **Character Set Selection**: Users can specify which character types to include (uppercase, lowercase, digits, special characters).
2.  **Exclusion Rules**: Specific characters can be excluded to avoid ambiguity (e.g., 'l', '1', 'O', '0').
3.  **Random Generation**: Passwords are built using cryptographically secure random number generation.
4.  **Post-Generation Analysis and Validation**: After a password is generated, it undergoes an immediate analysis using the same robust methods as the password analysis feature. The system then validates if the generated password meets predefined security criteria (e.g., not pwned, sufficient zxcvbn score, adequate entropy). If the generated password does not meet these criteria, the system attempts to regenerate it up to a maximum number of times to ensure a secure password is delivered.

### Passphrase Generation

Pyn also supports generating secure passphrases, which are often easier to remember than complex passwords:

1.  **Wordlist Usage**: Passphrases are generated using the EFF (Electronic Frontier Foundation) large wordlist, which consists of carefully selected words to ensure randomness and memorability.
2.  **Dice Roll Method**: Words are selected based on a simulated dice roll method, ensuring true randomness and making the passphrase highly unpredictable.
3.  **Customization**: Users can specify the number of words, the separator character (e.g., hyphens, spaces), and whether to capitalize each word.

### Local Deployment and Security

Pyn is designed primarily for local deployment to ensure maximum security and privacy. Running the application locally means that sensitive password data never leaves your machine, reducing the risk of exposure to external threats.

The only online interaction is with the optional "Have I Been Pwned?" API, which checks if passwords have appeared in known data breaches. This API usage is optional and can be disabled to maintain a fully offline and secure environment.

This local-first approach makes Pyn suitable for users who require strong password security without relying on cloud services or external servers.


## 💻 Getting Started

### Prerequisites
- Python 3.8+
- pip
- Virtual environment support

### 🚀 Running the application

For a quick and easy setup, use the provided initialization scripts:

-   **Windows:**
    ```cmd
    scripts\init_app.bat
    ```
-   **macOS/Linux:**
    ```bash
    bash scripts/init_app.sh
    ```
These scripts will handle the virtual environment setup, dependency installation, database initialization, and application launch.

### 🛠️ Manual Setup and Commands

If you prefer to run the setup commands manually instead of using the scripts, follow these steps:

#### On Windows (Command Prompt):

1. Create a virtual environment (if not already created):
    ```
    python -m venv venv
    ```
2. Activate the virtual environment:
    ```
    venv\Scripts\activate.bat
    ```
3. Upgrade pip and install dependencies:
    ```
    pip install --upgrade pip
    pip install -r requirements.txt
    ```
4. Set the FLASK_APP environment variable:
    ```
    set FLASK_APP=run.py
    ```
5. Initialize the database:
    ```
    flask init-db
    ```
6. Run the application:
    ```
    python run.py
    ```

#### On macOS/Linux (Bash/Zsh/Fish):

1. Create a virtual environment (if not already created):
    ```
    python3 -m venv venv
    ```
2. Activate the virtual environment:
    ```
    source venv/bin/activate
    ```
3. Upgrade pip and install dependencies:
    ```
    pip install --upgrade pip
    pip install -r requirements.txt
    ```
4. Set the FLASK_APP environment variable:
    ```
    export FLASK_APP=run.py
    ```
5. Initialize the database:
    ```
    flask init-db
    ```
6. Run the application:
    ```
    python3 run.py
    ```

## 🔗 API Endpoints (Overview)

Pyn exposes API endpoints for programmatic access to its features:

-   **`/passwords/analyze` (POST):** Analyze one or more passwords for strength, entropy, crack time, and pwned status.
-   **`/passwords/generate` (POST):** Generate secure, customizable passwords based on specified criteria.
-   **`/passphrase/analyze` (POST):** Analyze passphrases.
-   **`/passphrase/generate` (POST):** Generate passphrases.

Refer to the application's source code (e.g., `app/blueprints/passwords/routes.py` and `app/blueprints/passphrase/routes.py`) for detailed API payload and response structures.

## 🛠️ Technologies Used

### Backend
-   Python
-   Flask (Web Framework)

### Security Libraries
-   zxcvbn (Password strength estimation)
-   hashlib (Hashing library)
-   Flask-SQLAlchemy (ORM for database interaction)
-   SQLAlchemy (Python SQL Toolkit and ORM)

### API Integration
-   Requests (HTTP library)
-   Have I Been Pwned? API (For breach checking)

### Web Technologies
-   HTML
-   JavaScript
-   CSS

## 🤝 Contributing

Contributions are welcome! Please refer to the `CONTRIBUTING.md` file for detailed guidelines on how to contribute to this project.

## 📜 License

This project is distributed under the MIT License. See the `LICENSE` file for more information.

## 🐛 Known Issues

-   Limited support for international characters in some analysis features.
-   Potential rate limiting when using external APIs (e.g., Have I Been Pwned?).
-   Continuous improvement is required for analysis algorithms and front-end design.

## 🔗 Related Resources

-   [zxcvbn Documentation](https://github.com/dropbox/zxcvbn)
-   [Have I Been Pwned?](https://haveibeenpwned.com)
-   [NIST Password Guidelines](https://www.nist.gov)

## 📞 Contact

Project Link: [Pyn on GitHub](https://github.com/emanuellcs/pyn)

For any inquiries, you can reach me at: emanuellzr01@outlook.com

## ⚠️ Disclaimer

Always use generated passwords responsibly and avoid sharing them.

---

Made with ❤️ by [Emanuel Lázaro](https://github.com/emanuellcs).
