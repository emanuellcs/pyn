# Pyn: A Comprehensive Password Security Toolkit

## 🔐 Overview

Pyn is a Python-based web application designed to enhance password security through advanced analysis and generation capabilities. It allows users to create, evaluate, and strengthen their passwords with detailed insights and recommendations. This tool is inspired by the [Cygnius Password Test](https://apps.cygnius.net/passtest/).

## 🚀 Key Features

### 🔎 Password Analysis
- Comprehensive strength evaluation
- Entropy calculation
- Crack time estimation
- Complexity assessment
- Pwned password detection

### 🔧 Password Generation
- Customizable password creation
- Secure random generation
- Multiple character set options
- Configurable length and complexity

## 📋 Table of Contents
1. [Installation](#-installation)
2. [Usage](#-usage)
3. [Technologies Used](#-technologies-used)
4. [Contributing](#-contributing)
5. [License](#-license)
6. [Known Issues](#-known-issues)
7. [Related Resources](#-related-resources)
8. [Contact](#-contact)

## 💻 Installation

### Prerequisites
- Python 3.8+
- pip
- Virtual environment support

### Setup Instructions

#### Linux
1. Clone the repository:
   ```bash
   git clone https://github.com/emanuellcs/pyn.git
   cd pyn
	```

2.  Run the setup script:
    
    ```bash
    bash setups/setup_linux.sh
    ```
    
3.  If the virtual environment activation script encounters an error, execute the following command to manually activate the environment:
    
    ```bash
    source venv/bin/activate && pip install -r requirements.txt
    ```

4. Run `pyn.py`:

   ```bash
   python pyn.py
   ```

#### macOS

1.  Clone the repository:
    
    ```bash
    git clone https://github.com/emanuellcs/pyn.git
    cd pyn
    ```
    
2.  Run the setup script:
    
    ```bash
    bash setups/setup_mac.sh
    ```
    
3.  If the virtual environment activation script encounters an error, execute the following command to manually activate the environment:
    
    ```bash
    source venv/bin/activate && pip install -r requirements.txt
    ```

4. Run `pyn.py`:

   ```bash
   python pyn.py
   ```

#### Windows

1.  Clone the repository:
    
    ```cmd
    git clone https://github.com/emanuellcs/pyn.git
    cd pyn
    ```
    
2.  Run the setup script:
    
    ```cmd
    setups\setup_windows.bat
    ```

3.  If the virtual environment activation script encounters an error, execute the following command to manually activate the environment:
    
    ```cmd
    call venv\Scripts\activate.bat && pip install -r requirements.txt
    ```

4. Run `pyn.py`:

   ```cmd
   python pyn.py
   ```

### Notes

-   The setup scripts automatically create a virtual environment and install all dependencies listed in `requirements.txt`.
-   Ensure Python and pip are correctly installed and accessible in your system's PATH before running the scripts.

## 🔍 Usage

### Running the Application

To start the application, run the following command:

```bash
python pyn.py
```

**Expected Output**:
```
 * Serving Flask app 'pyn'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 121-363-416
```

### API Endpoints

#### Password Analysis

-   **Endpoint**: `/analyze`
-   **Method**: POST
-   **Payload**: Comma-separated passwords

#### Password Generation

-   **Endpoint**: `/generate`
-   **Method**: POST
-   **Configurable Options**:
    -   Length
    -   Character types
    -   Exclusion rules

### Example Requests

#### Generate Password Example

To generate a password, you can send a POST request to the `/generate` endpoint with the following JSON payload:

```json
{
    "length": 16,
    "use_upper": true,
    "use_lower": true,
    "use_digits": true,
    "use_special": true,
    "exclude_chars": "l1O0"  // Example of characters to exclude
}
```

**Example Response**:
```json
{
    "password": "A1b2C3d4E5f6G7h8",
    "analysis": {
        "strength": "strong",
        "crack_time": "years"
    }
}
```

#### Analyze Password Example

To analyze a password, you can send a POST request to the `/analyze` endpoint with the following payload:

```text
passwords = "mypassword123,StrongP@ssw0rd123"
```

**Example Response**:
```json
{
    "results": [
        {
            "password": "mypassword123",
            "entropy": 67.21,
            "expected_guesses": 170581728179578200000,
            "score from 0 to 4": 0,
            "enhanced_crack_times": {
                "offline_fast_hash": "54.1 years",
                "offline_parallel": "5.4 years",
                "offline_slow_hash": "540.9 million years",
                "online_no_throttling": "5.4 billion years",
                "online_throttling": "540.9 billion years"
            },
            "suggestions": ["Add another word or two. Uncommon words are better."],
            "warning": "This is similar to a commonly used password.",
            "pwned": 2315,
            "complexity_issues": [
                "Password must contain an uppercase letter.",
                "Password must contain a special character or be at least 15 characters.",
                "Password is too short, must be at least 15 characters."
            ]
        },
        {
            "password": "StrongP@ssw0rd123",
            "entropy": 111.43,
            "expected_guesses": 3.492798333840549e+33,
            "score from 0 to 4": 4,
            "enhanced_crack_times": {
                "offline_fast_hash": "1107559.1 billion years",
                "offline_parallel": "110755.9 billion years",
                "offline_slow_hash": "11075590860732.3 billion years",
                "online_no_throttling": "110755908607323.3 billion years",
                "online_throttling": "11075590860732332.0 billion years"
            },
            "suggestions": [],
            "warning": null,
            "pwned": 0,
            "complexity_issues": []
        }
    ]
}
```

### Password Analysis Examples

#### Example 1: mypassword123
- **Strength**: Weak
- **Entropy Score**: 67.21 bits
- **Expected Guesses**: 170,581,728,179,578,200,000

**Enhanced Crack Times**:
- Offline Fast Hash: 54.1 years
- Offline Parallel: 5.4 years
- Offline Slow Hash: 540.9 million years
- Online No Throttling: 5.4 billion years
- Online Throttling: 540.9 billion years

**ZXCVBN Crack Times**:
- Offline Fast Hashing (1e10 per second): less than a second
- Offline Slow Hashing (1e4 per second): 7 seconds
- Online No Throttling (10 per second): 2 hours
- Online Throttling (100 per hour): 29 days

**Pwned Status**: Pwned 2315 times

**Suggestions**:
- Add another word or two. Uncommon words are better.

**Complexity Issues**:
- Password must contain an uppercase letter.
- Password must contain a special character or be at least 15 characters.
- Password is too short, must be at least 15 characters.

**Match Sequence**:
- Match Sequence:
  - 'my'
    - Pattern: dictionary
    - Dict-name: us_tv_and_film
    - Rank: 13
    - Base-guesses: 13
    - Uppercase-variations: 1
    - L33t-variations: 1
  - 'password123'
    - Pattern: dictionary
    - Dict-name: passwords
    - Rank: 595
    - Base-guesses: 595
    - Uppercase-variations: 1
    - L33t-variations: 1

**Warning**: This is similar to a commonly used password.

**Calculation Time**: 7.6 ms

#### Example 2: StrongP@ssw0rd123
- **Strength**: Strong
- **Entropy Score**: 111.43 bits
- **Expected Guesses**: 3.49e+33

**Enhanced Crack Times**:
- Offline Fast Hash: 1,107,559.1 billion years
- Offline Parallel: 110,755.9 billion years
- Offline Slow Hash: 11,075,590,860,732.3 billion years
- Online No Throttling: 110,755,908,607,323.3 billion years
- Online Throttling: 11,075,590,860,732,332.0 billion years

**ZXCVBN Crack Times**:
- Offline Fast Hashing (1e10 per second): less than a second
- Offline Slow Hashing (1e4 per second): 3 hours
- Online No Throttling (10 per second): 4 months
- Online Throttling (100 per hour): centuries

**Pwned Status**: Not Pwned

**Suggestions**: None

**Match Sequence**:
- Match Sequence:
  - 'Strong'
    - Pattern: dictionary
    - Dict-name: surnames
    - Rank: 570
    - Base-guesses: 570
    - Uppercase-variations: 2
    - L33t-variations: 1
  - 'P@ssw0rd'
    - Pattern: dictionary
    - Dict-name: passwords
    - Rank: 2
    - Base-guesses: 2
    - Uppercase-variations: 2
    - L33t-variations: 4
  - '123'
    - Pattern: sequence

**Calculation Time**: 6.25 ms

### Password Generation Example

- **Password Length**: 12
- **Exclude Characters**: None
- **Generated Password**: @0B$9ob:D2)F
- **Entropy**: 78.66 bits
- **Pwned Status**: 0

## 🛠 Technologies Used

### Backend

-   Python
-   Flask

### Security Libraries

-   zxcvbn
-   hashlib

### API Integration

-   Requests
-   Have I Been Pwned? API

### Web Technologies

-   HTML
-   JavaScript
-   CSS

## 🤝 Contributing

Contributions are always welcome! Follow these steps to contribute:

1.  Read the `CONTRIBUTING.md` file for detailed guidelines.
2.  Fork the repository:
    
    ```bash
    git fork https://github.com/emanuellcs/pyn.git
    ```
    
3.  Create a branch for your feature:
    
    ```bash
    git checkout -b feature/AmazingFeature
    ```
    
4.  Commit your changes:
    
    ```bash
    git commit -m "Add AmazingFeature"
    ```
    
5.  Push to your branch:
    
    ```bash
    git push origin feature/AmazingFeature
    ```
    
6.  Open a Pull Request with a clear description of your changes.

## 📜 License

This project is distributed under the MIT License. See the `LICENSE` file for more information.

## 🐛 Known Issues

-   Limited support for international characters.
-   Potential rate limiting when using external APIs.
-   Continuous improvement is required for analysis algorithms and front-end design.

## 🔗 Related Resources

-   [zxcvbn Documentation](https://github.com/dropbox/zxcvbn)
-   [Have I Been Pwned?](https://haveibeenpwned.com)
-   [NIST Password Guidelines](https://www.nist.gov)

## 📞 Contact

Project Link: [Pyn on GitHub](https://github.com/emanuellcs/pyn)

For any inquiries, you can reach me at: emanuellzr01@outlook.com

## ❤️ Support

To support this project, please consider donating through [GitHub Sponsors](https://github.com/sponsors/emanuellcs).

## ⚠️ Disclaimer

Always use generated passwords responsibly and avoid sharing them.

---

Made with ❤️ by [Emanuel Lázaro](https://github.com/emanuellcs).
