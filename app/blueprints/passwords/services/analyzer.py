import time
import math
import re
from typing import List, Dict, Any, Tuple
from zxcvbn import zxcvbn
import requests
import hashlib

class PasswordAnalysis:
    SECONDS_PER_MINUTE = 60
    SECONDS_PER_HOUR = 3600
    SECONDS_PER_DAY = 86400
    SECONDS_PER_YEAR = 31536000

    ATTEMPT_RATES = {
        "offline_fast_hashing": 100_000_000_000,
        "offline_slow_hashing": 10_000,
        "online_no_throttling": 1000,
        "online_with_throttling": 10,
        "offline_parallel_attack": 1_000_000_000_000
    }

    def __init__(self, password: str, check_pwned_password: bool = True):
        self.password = password
        self.analysis = None
        self.complexity_report = {}
        self.calculation_time_ms = 0
        self.check_pwned_password = check_pwned_password

    def get_charset_size(self) -> Tuple[int, List[str]]:
        """
        Calculate the actual character set size based on password composition.
        Returns tuple of (charset_size, used_charsets).
        """
        charsets_used = []
        charset_size = 0

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
        Calculate comprehensive cracking time estimates for different scenarios.
        """
        charset_size, _ = self.get_charset_size()
        password_length = len(self.password)
        
        if charset_size == 0:
            return {}

        possible_combinations = charset_size ** password_length

        crack_times = {}
        for scenario, attempts_per_second in self.ATTEMPT_RATES.items():
            seconds = possible_combinations / attempts_per_second if attempts_per_second > 0 else float('inf')
            crack_times[scenario] = {
                "seconds": seconds,
                "display": self.format_time(seconds)
            }
        return crack_times

    def format_time(self, seconds: float) -> str:
        """
        Format time in seconds to a human-readable string.
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
        Check password against a set of complexity requirements.
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
        Calculate the entropy of the password.
        """
        charset_size, _ = self.get_charset_size()
        password_length = len(self.password)

        if charset_size == 0:
            return {"entropy": 0.0, "expected_guesses": 0.0}

        entropy = math.log2(charset_size) * password_length
        expected_guesses = charset_size ** password_length

        return {"entropy": entropy, "expected_guesses": expected_guesses}

    def analyze(self):
        """
        Performs the main password analysis using zxcvbn and additional checks.
        """
        start_time = time.time()
        
        self.analysis = zxcvbn(self.password)
        self.check_complexity_requirements()

        end_time = time.time()
        self.calculation_time_ms = (end_time - start_time) * 1000

    def check_pwned(self) -> int:
        """
        Checks if the password has been pwned using the Have I Been Pwned? API.
        """
        if not self.password:
            return 0
        hashed_password = hashlib.sha1(self.password.encode('utf-8')).hexdigest().upper()
        prefix = hashed_password[:5]
        suffix = hashed_password[5:]
        url = f'https://api.pwnedpasswords.com/range/{prefix}'
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                for line in response.text.splitlines():
                    s, count = line.split(':')
                    if s == suffix:
                        return int(count)
        except requests.RequestException:
            return -1  # Indicate an error occurred
        return 0

    def report(self) -> Dict[str, Any]:
        """
        Generates a comprehensive report of all password analysis results.
        """
        if self.analysis is None:
            self.analyze()

        pwned_count = self.check_pwned() if self.check_pwned_password else -2  # -2 indicates not checked
        entropy_data = self.calculate_entropy()
        charset_size, char_sets_used = self.get_charset_size()
        crack_time_estimates = self.calculate_crack_time()

        zxcvbn_results = self.analysis or {}

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
    """Maps zxcvbn score to a strength string."""
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

    Args:
        password: The password to analyze.
        check_pwned: Whether to check against the Pwned Passwords database.

    Returns:
        A dictionary containing the analysis details.
    """
    if not password:
        return {
            'strength': 'Unknown',
            'details': [{'title': 'Error', 'explanation': 'Password cannot be empty.'}]
        }

    analysis = PasswordAnalysis(password, check_pwned_password=check_pwned)
    report = analysis.report()

    return report
