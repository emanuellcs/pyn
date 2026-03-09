import math
import re
import random
import string
from typing import Tuple, List, Dict, Any


class PasswordDomain:
    @staticmethod
    def get_charset_size(password: str) -> Tuple[int, List[str]]:
        charsets_used = []
        charset_size = 0

        if bool(re.search(r"[A-Z]", password)):
            charset_size += 26
            charsets_used.append("uppercase")
        if bool(re.search(r"[a-z]", password)):
            charset_size += 26
            charsets_used.append("lowercase")
        if bool(re.search(r"\d", password)):
            charset_size += 10
            charsets_used.append("numbers")
        if bool(re.search(r"[^a-zA-Z0-9]", password)):
            charset_size += 32
            charsets_used.append("special")

        return charset_size, charsets_used

    @staticmethod
    def calculate_entropy(password: str) -> Dict[str, float]:
        charset_size, _ = PasswordDomain.get_charset_size(password)
        password_length = len(password)

        if charset_size == 0:
            return {"entropy": 0.0, "expected_guesses": 0.0}

        entropy = math.log2(charset_size) * password_length
        expected_guesses = charset_size**password_length

        return {"entropy": entropy, "expected_guesses": expected_guesses}

    @staticmethod
    def check_complexity_requirements(password: str) -> Dict[str, bool]:
        return {
            "min_length": len(password) >= 15,
            "has_uppercase": bool(re.search(r"[A-Z]", password)),
            "has_lowercase": bool(re.search(r"[a-z]", password)),
            "has_numbers": bool(re.search(r"\d", password)),
            "has_special": bool(re.search(r"[^a-zA-Z0-9]", password)),
            "no_start_with_special_or_number": not bool(
                re.match(r"^[0-9\W]", password)
            ),
            "no_excessive_repeats": all(
                password.count(char) <= 3 for char in set(password)
            ),
        }

    @staticmethod
    def calculate_crack_time(password: str) -> Dict[str, Dict[str, float]]:
        charset_size, _ = PasswordDomain.get_charset_size(password)
        password_length = len(password)

        if charset_size == 0:
            return {}

        possible_combinations = charset_size**password_length
        rates = {
            "offline_fast_hashing": 100_000_000_000,
            "offline_slow_hashing": 10_000,
            "online_no_throttling": 1000,
            "online_with_throttling": 10,
            "offline_parallel_attack": 1_000_000_000_000,
        }

        crack_times = {}
        for scenario, attempts_per_second in rates.items():
            seconds = (
                possible_combinations / attempts_per_second
                if attempts_per_second > 0
                else float("inf")
            )
            crack_times[scenario] = {
                "seconds": seconds,
                "display": PasswordDomain.format_time(seconds),
            }
        return crack_times

    @staticmethod
    def format_time(seconds: float) -> str:
        if seconds < 60:
            return f"{seconds:.1f} seconds"
        elif seconds < 3600:
            return f"{seconds / 60:.1f} minutes"
        elif seconds < 86400:
            return f"{seconds / 3600:.1f} hours"
        elif seconds < 31536000:
            return f"{seconds / 86400:.1f} days"
        else:
            years = seconds / 31536000
            if years < 1_000_000:
                return f"{years:,.1f} years"
            elif years < 1_000_000_000:
                return f"{years/1_000_000:.1f} million years"
            else:
                return f"{years/1_000_000_000:.1f} billion years"


class PasswordGenerator:
    """
    Generates random passwords based on specified criteria.
    """

    def __init__(self):
        self.uppercase = string.ascii_uppercase
        self.lowercase = string.ascii_lowercase
        self.digits = string.digits
        self.special = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    def generate(
        self,
        length: int = 16,
        use_upper: bool = True,
        use_lower: bool = True,
        use_digits: bool = True,
        use_special: bool = True,
        exclude_chars: str = "",
    ) -> Dict[str, Any]:
        selected_chars = ""

        if use_upper:
            selected_chars += self.uppercase
        if use_lower:
            selected_chars += self.lowercase
        if use_digits:
            selected_chars += self.digits
        if use_special:
            selected_chars += self.special

        # Fallback if everything is False
        if not selected_chars:
            selected_chars = self.lowercase + self.digits

        all_chars = list(selected_chars)

        if exclude_chars:
            all_chars = [c for c in all_chars if c not in exclude_chars]
            if not all_chars:
                all_chars = list(selected_chars)

        sr = random.SystemRandom()
        password_list = [sr.choice(all_chars) for _ in range(length)]
        sr.shuffle(password_list)
        password = "".join(password_list)

        return {"password": password}
