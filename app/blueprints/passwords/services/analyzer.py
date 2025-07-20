import time
import math
import re
from typing import List, Dict, Any, Tuple
from zxcvbn import zxcvbn
import requests
import hashlib

class PasswordAnalysis:
    """
    Performs a comprehensive security analysis of a given password.

    Utilizes zxcvbn for strength estimation, checks against complexity requirements,
    calculates entropy, estimates crack times, and queries the Have I Been Pwned? API.
    """
    # Defines constants for time conversions.
    # Facilitates converting seconds into human-readable time formats.
    SECONDS_PER_MINUTE = 60
    SECONDS_PER_HOUR = 3600
    SECONDS_PER_DAY = 86400
    SECONDS_PER_YEAR = 31536000

    # Defines various attack attempt rates.
    # Used to estimate password cracking time under different scenarios.
    ATTEMPT_RATES = {
        "offline_fast_hashing": 100_000_000_000,
        "offline_slow_hashing": 10_000,
        "online_no_throttling": 1000,
        "online_with_throttling": 10,
        "offline_parallel_attack": 1_000_000_000_000
    }

    def __init__(self, password: str, check_pwned_password: bool = True):
        # Initializes the PasswordAnalysis instance.
        # Sets the password to be analyzed and configures pwned password checking.
        self.password = password
        self.analysis = None
        self.complexity_report = {}
        self.calculation_time_ms = 0
        self.check_pwned_password = check_pwned_password

    def get_charset_size(self) -> Tuple[int, List[str]]:
        """
        Calculates the effective character set size based on the password's composition.
        Identifies which character types (uppercase, lowercase, numbers, special) are present.

        Returns:
            Tuple[int, List[str]]: A tuple containing the total character set size
                                   and a list of character sets used.
        """
        charsets_used = []
        charset_size = 0

        # Checks for and adds character set sizes based on regex matches.
        if bool(re.search(r'[A-Z]', self.password)):
            charset_size += 26
            charsets_used.append("uppercase")
        if bool(re.search(r'[a-z]', self.password)):
            charset_size += 26
            charsets_used.append("lowercase")
        if bool(re.search(r'\d', self.password)):
            charset_size += 10
            charsets_used.append("numbers")
        if bool(re.search(r'[^a-zA-Z0-9]', self.password)):
            charset_size += 32
            charsets_used.append("special")

        return charset_size, charsets_used

    def calculate_crack_time(self) -> Dict[str, Dict[str, Any]]:
        """
        Calculates estimated cracking times for the password under various attack scenarios.
        Uses the password's character set size and length to determine combinations.
        """
        charset_size, _ = self.get_charset_size()
        password_length = len(self.password)
        
        if charset_size == 0:
            return {}

        # Calculates the total number of possible combinations.
        possible_combinations = charset_size ** password_length

        crack_times = {}
        # Estimates crack time for each defined attack scenario.
        for scenario, attempts_per_second in self.ATTEMPT_RATES.items():
            seconds = possible_combinations / attempts_per_second if attempts_per_second > 0 else float('inf')
            crack_times[scenario] = {
                "seconds": seconds,
                "display": self.format_time(seconds)
            }
        return crack_times

    def format_time(self, seconds: float) -> str:
        """
        Formats a given duration in seconds into a human-readable string.
        Converts seconds into minutes, hours, days, or years as appropriate.
        """
        if seconds < self.SECONDS_PER_MINUTE:
            return f"{seconds:.1f} seconds"
        elif seconds < self.SECONDS_PER_HOUR:
            minutes = seconds / self.SECONDS_PER_MINUTE
            return f"{minutes:.1f} minutes"
        elif seconds < self.SECONDS_PER_DAY:
            hours = seconds / self.SECONDS_PER_HOUR
            return f"{hours:.1f} hours"
        elif seconds < self.SECONDS_PER_YEAR:
            days = seconds / self.SECONDS_PER_DAY
            return f"{days:.1f} days"
        else:
            years = seconds / self.SECONDS_PER_YEAR
            if years < 1_000_000:
                return f"{years:,.1f} years"
            elif years < 1_000_000_000:
                return f"{years/1_000_000:.1f} million years"
            else:
                return f"{years/1_000_000_000:.1f} billion years"

    def check_complexity_requirements(self) -> Dict[str, bool]:
        """
        Checks the password against a predefined set of complexity requirements.
        Evaluates criteria such as minimum length, presence of character types, and repetition.
        """
        self.complexity_report = {
            "min_length": len(self.password) >= 15,
            "has_uppercase": bool(re.search(r'[A-Z]', self.password)),
            "has_lowercase": bool(re.search(r'[a-z]', self.password)),
            "has_numbers": bool(re.search(r'\d', self.password)),
            "has_special": bool(re.search(r'[^a-zA-Z0-9]', self.password)),
            "no_start_with_special_or_number": not bool(re.match(r'^[0-9\W]', self.password)),
            "no_excessive_repeats": all(self.password.count(char) <= 3 for char in set(self.password))
        }
        return self.complexity_report

    def calculate_entropy(self) -> Dict[str, float]:
        """
        Calculates the entropy of the password in bits.
        Entropy quantifies the randomness and unpredictability of the password.
        """
        charset_size, _ = self.get_charset_size()
        password_length = len(self.password)

        if charset_size == 0:
            return {"entropy": 0.0, "expected_guesses": 0.0}

        # Computes entropy using the formula: log2(charset_size) * password_length.
        entropy = math.log2(charset_size) * password_length
        # Calculates the total number of expected guesses.
        expected_guesses = charset_size ** password_length

        return {"entropy": entropy, "expected_guesses": expected_guesses}

    def analyze(self):
        """
        Performs the core password analysis using the zxcvbn library and custom complexity checks.
        Measures the time taken for the analysis.
        """
        start_time = time.time()
        
        # Runs the zxcvbn analysis on the password.
        self.analysis = zxcvbn(self.password)
        # Checks the password against defined complexity requirements.
        self.check_complexity_requirements()

        end_time = time.time()
        # Records the total time taken for the analysis.
        self.calculation_time_ms = (end_time - start_time) * 1000

    def check_pwned(self) -> int:
        """
        Checks if the password has appeared in known data breaches using the Have I Been Pwned? API.
        Returns the number of times the password was found, 0 if not found, or -1 on error.
        """
        if not self.password:
            return 0
        # Hashes the password and retrieves the first 5 characters (prefix).
        hashed_password = hashlib.sha1(self.password.encode('utf-8')).hexdigest().upper()
        prefix = hashed_password[:5]
        suffix = hashed_password[5:]
        # Constructs the API URL for the k-anonymity search.
        url = f'https://api.pwnedpasswords.com/range/{prefix}'
        try:
            # Sends a GET request to the HIBP API.
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                # Parses the response to find matching suffixes and their counts.
                for line in response.text.splitlines():
                    s, count = line.split(':')
                    if s == suffix:
                        return int(count)
        except requests.RequestException:
            # Handles network or API request errors.
            return -1  # Indicate an error occurred
        return 0

    def report(self) -> Dict[str, Any]:
        """
        Generates a comprehensive report summarizing all password analysis results.
        Includes zxcvbn output, crack time estimates, complexity checks, and pwned status.
        """
        if self.analysis is None:
            self.analyze()

        # Performs pwned password check if enabled.
        pwned_count = self.check_pwned() if self.check_pwned_password else -2  # -2 indicates not checked
        # Gathers entropy, character set, and crack time data.
        entropy_data = self.calculate_entropy()
        charset_size, char_sets_used = self.get_charset_size()
        crack_time_estimates = self.calculate_crack_time()

        zxcvbn_results = self.analysis or {}

        # Compiles all analysis data into a structured dictionary.
        return {
            "password_strength_metrics": {
                "entropy": entropy_data.get("entropy"),
                "expected_guesses": entropy_data.get("expected_guesses"),
            },
            "crack_time_estimates": {
                "offline_fast_hashing": crack_time_estimates.get("offline_fast_hashing"),
                "offline_slow_hashing": crack_time_estimates.get("offline_slow_hashing"),
                "online_no_throttling": crack_time_estimates.get("online_no_throttling"),
                "online_with_throttling": crack_time_estimates.get("online_with_throttling"),
                "offline_parallel_attack": crack_time_estimates.get("offline_parallel_attack"),
            },
            "complexity_requirements": self.complexity_report,
            "zxcvbn_analysis": {
                "score": zxcvbn_results.get("score"),
                "crack_times_seconds": zxcvbn_results.get("crack_times_seconds"),
                "crack_times_display": zxcvbn_results.get("crack_times_display"),
                "feedback": zxcvbn_results.get("feedback", {}),
                "match_sequence": zxcvbn_results.get("sequence", []),
            },
            "character_set_analysis": {
                "char_sets_used": char_sets_used,
                "char_set_size": charset_size,
            },
            "pwned_password_check": {
                "pwned": pwned_count > 0,
                "pwned_count": "Not checked" if pwned_count == -2 else (pwned_count if pwned_count != -1 else "Error checking"),
            },
            "performance": {
                "calculation_time_ms": round(self.calculation_time_ms, 2),
            }
        }


def get_strength_from_score(score: int) -> str:
    """
    Maps a zxcvbn score to a human-readable password strength string.
    Provides a qualitative assessment of password strength.
    """
    if score <= 1:
        return "Weak"
    elif score == 2:
        return "Good"
    elif score == 3:
        return "Strong"
    else:
        return "Very Strong"


def analyze_password(password: str, check_pwned: bool = True) -> Dict[str, Any]:
    """
    Analyzes a password to determine its strength and provide detailed feedback.

    Initializes a PasswordAnalysis object and generates a comprehensive report.

    Args:
        password: The password string to be analyzed.
        check_pwned: A boolean indicating whether to check the password against
                     the Have I Been Pwned? database.

    Returns:
        A dictionary containing various analysis details, including strength,
        crack time estimates, complexity report, and pwned status.
    """
    if not password:
        return {
            'strength': 'Unknown',
            'details': [{'title': 'Error', 'explanation': 'Password cannot be empty.'}]
        }

    # Creates a PasswordAnalysis instance and generates the full report.
    analysis = PasswordAnalysis(password, check_pwned_password=check_pwned)
    report = analysis.report()

    details = []
    # Adds password length to the report details.
    details.append({'title': 'Length', 'explanation': f"{len(password)} characters"})
    
    # Adds character set usage to the report details.
    char_sets_used = report['character_set_analysis']['char_sets_used']
    details.append({'title': 'Character Variety', 'explanation': f"Uses: {', '.join(char_sets_used) if char_sets_used else 'None'}"})

    # Adds offline crack time estimate to the report details.
    if report['crack_time_estimates'] and 'offline_fast_hashing' in report['crack_time_estimates']:
        details.append({'title': 'Time to Crack (Offline, Fast Hashing)', 'explanation': report['crack_time_estimates']['offline_fast_hashing']['display']})

    # Adds pwned status to the report details.
    pwned_status = report['pwned_password_check']['pwned_count']
    details.append({'title': 'Pwned Status', 'explanation': f"Found {pwned_status} times in breaches." if isinstance(pwned_status, int) and pwned_status > 0 else "Not found in breaches."})

    # Adds complexity requirements check results to details.
    complexity_items = []
    for req, passed in report['complexity_requirements'].items():
        status = "✅" if passed else "❌"
        complexity_items.append(f"{status} {req.replace('_', ' ').title()}")
    details.append({'title': 'Complexity Requirements', 'explanation': ', '.join(complexity_items)})

    # Adds zxcvbn feedback suggestions to details if available.
    if report['zxcvbn_analysis']['feedback'] and report['zxcvbn_analysis']['feedback']['suggestions']:
        feedback_suggestions = report['zxcvbn_analysis']['feedback']['suggestions']
        details.append({'title': 'Suggestions', 'explanation': ' '.join(feedback_suggestions)})

    # Updates the report with the generated details and overall strength.
    report['details'] = details
    report['strength'] = get_strength_from_score(report['zxcvbn_analysis']['score'])

    return report
