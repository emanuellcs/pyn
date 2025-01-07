import time
import math
import re
from typing import List, Dict, Any, Tuple
from zxcvbn import zxcvbn
import requests
import hashlib
from flask import Flask

class PasswordAnalysis:
    SECONDS_PER_MINUTE = 60
    SECONDS_PER_HOUR = 3600
    SECONDS_PER_DAY = 86400
    SECONDS_PER_YEAR = 31536000

    ATTEMPT_RATES = {
        "offline_fast_hash": 100_000_000_000,
        "offline_slow_hash": 10_000,
        "online_no_throttling": 1000,
        "online_throttling": 10,
        "offline_parallel": 1_000_000_000_000
    }

    def __init__(self, password: str):
        self.password = password
        self.analysis = None
        self.complexity_issues = []
        self.calculation_time_ms = 0

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

    def calculate_crack_time(self) -> Dict[str, str]:
        """
        Calculate comprehensive cracking time estimates for different scenarios and format the output.
        """
        charset_size, _ = self.get_charset_size()
        password_length = len(self.password)
        possible_combinations = charset_size ** password_length

        crack_times_display = {}
        for scenario, attempts_per_second in self.ATTEMPT_RATES.items():
            seconds = possible_combinations / attempts_per_second
            time_display = self.format_time(seconds)
            crack_times_display[scenario] = time_display
        return {"crack_times_display": crack_times_display}

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
                return f"{years:.1f} years"
            elif years < 1_000_000_000:
                return f"{years/1_000_000:.1f} million years"
            else:
                return f"{years/1_000_000_000:.1f} billion years"

    def check_complexity(self) -> None:
        """
        Check password complexity based on defined criteria.
        """
        complexity_warnings = set()
        if len(self.password) < 15:
            complexity_warnings.add("Password is too short, must be at least 15 characters.")
        if not re.search(r'\d', self.password):
            complexity_warnings.add("Password must contain a number.")
        if not re.search(r'[A-Z]', self.password):
            complexity_warnings.add("Password must contain an uppercase letter.")
        if not re.search(r'[a-z]', self.password):
            complexity_warnings.add("Password must contain a lowercase letter.")
        if re.match(r'^[0-9\W]', self.password):
            complexity_warnings.add("Password should not start with a number or special character.")
        for char in set(self.password):
            if self.password.count(char) > 3:
                complexity_warnings.add("Password should not have too many repeated characters.")
        if len(self.password) < 15 and not re.search(r'[^a-zA-Z0-9]', self.password):
            complexity_warnings.add("Password must contain a special character or be at least 15 characters.")
        self.complexity_issues = list(complexity_warnings)

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
        self.check_complexity()

        # Add enhanced crack time calculation
        crack_time_analysis = self.calculate_crack_time()
        self.analysis.update({
            'enhanced_crack_time': crack_time_analysis,
            'complexity_issues': self.complexity_issues
        })

        end_time = time.time()
        self.calculation_time_ms = (end_time - start_time) * 1000

    def check_pwned(self) -> int:
        """
        Checks if the password has been pwned using the Have I Been Pwned? API.
        """
        hashed_password = hashlib.sha1(self.password.encode('utf-8')).hexdigest().upper()
        prefix = hashed_password[:5]
        suffix = hashed_password[5:]
        url = f'https://api.pwnedpasswords.com/range/{prefix}'
        response = requests.get(url)
        if response.status_code == 200:
            for line in response.text.splitlines():
                s, count = line.split(':')
                if s == suffix:
                    return int(count)
        return 0

    def report(self) -> Dict[str, Any]:
        """
        Generates a comprehensive report of all password analysis results.
        """
        if not self.analysis:
            return {"error": "Password not analyzed yet."}

        pwned_status = self.check_pwned()
        entropy_data = self.calculate_entropy()

        match_sequence_output = "match sequence:\n"
        for match in self.analysis.get("sequence", []):
            match_sequence_output += f"'{match.get('token', '')}'\n"
            match_sequence_output += f"pattern:\t{match.get('pattern', '')}\n"
            if match.get('entropy') is not None:
                match_sequence_output += f"entropy:\t{match.get('entropy')}\n"
            if match.get('dictionary_name'):
                match_sequence_output += f"dict-name:\t{match.get('dictionary_name')}\n"
                if match.get('rank') is not None:
                    match_sequence_output += f"rank:\t{match.get('rank')}\n"
                if match.get('base_guesses') is not None:
                    match_sequence_output += f"base-guesses:\t{match.get('base_guesses')}\n"
                if match.get('uppercase_variations') is not None:
                    match_sequence_output += f"uppercase-variations:\t{match.get('uppercase_variations')}\n"
                if match.get('l33t_variations') is not None:
                    match_sequence_output += f"l33t-variations:\t{match.get('l33t_variations')}\n"
            elif match.get('regex_name'):
                match_sequence_output += f"regex_name:\t{match.get('regex_name')}\n"
            if match.get('base_token'):
                match_sequence_output += f"base_token:\t'{match.get('base_token')}'\n"
                if match.get('base_guesses') is not None:
                    match_sequence_output += f"base_guesses:\t{match.get('base_guesses')}\n"
                if match.get('num_repeats') is not None:
                    match_sequence_output += f"num_repeats:\t{match.get('num_repeats')}\n"
            if match.get('cardinality') is not None:
                match_sequence_output += f"cardinality:\t{match.get('cardinality')}\n"
            if match.get('length') is not None:
                match_sequence_output += f"length:\t{match.get('length')}\n"
            match_sequence_output += "\n"

        return {
            "password": self.password,
            "entropy": entropy_data["entropy"],
            "expected_guesses": entropy_data["expected_guesses"],
            "score from 0 to 4": self.analysis.get("score", 0),
            "enhanced_crack_times": self.analysis.get("enhanced_crack_time"),
            "zxcvbn_crack_times": {
                "seconds": self.analysis.get("crack_times_seconds", {}),
                "display": self.analysis.get("crack_times_display", {})
            },
            "suggestions": self.analysis.get("feedback", {}).get("suggestions", []),
            "warning": self.analysis.get("feedback", {}).get("warning", "None"),
            "calculation_time_ms": round(self.calculation_time_ms, 2),
            "pwned": pwned_status,
            "pwned_message": f"Pwned {pwned_status} times. Please generate another password." if pwned_status > 0 else "Not Pwned",
            "match_sequence": match_sequence_output,
            "complexity_issues": self.complexity_issues,
        }
