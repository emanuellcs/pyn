import hashlib
import requests
from functools import lru_cache


class HIBPService:
    @staticmethod
    @lru_cache(maxsize=1024)
    def _fetch_hibp_range(prefix: str) -> str:
        """Fetch the range from HIBP API. Cached in memory to prevent rate limits."""
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.text
        except requests.RequestException:
            pass
        return ""

    @classmethod
    def check_pwned(cls, password: str) -> int:
        if not password:
            return 0

        hashed_password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
        prefix = hashed_password[:5]
        suffix = hashed_password[5:]

        response_text = cls._fetch_hibp_range(prefix)
        if not response_text:
            return -1  # Indicates error or no response

        for line in response_text.splitlines():
            s, count = line.split(":")
            if s == suffix:
                return int(count)

        return 0
