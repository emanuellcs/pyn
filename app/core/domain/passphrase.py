import random
import os


class PassphraseDomain:
    VOWELS = "aeiou"
    CONSONANTS = "bcdfghjklmnpqrstvwxyz"

    @classmethod
    def generate_pronounceable(cls, num_words: int = 3, separator: str = "-") -> str:
        """
        Generates a pronounceable, gibberish passphrase (e.g. trin-fack-bort).
        Each word follows a CVC, CVCC, or CCVC pattern.
        """
        words = []
        patterns = ["CVC", "CVCC", "CCVC"]

        for _ in range(num_words):
            pattern = random.choice(patterns)
            word = ""
            for char_type in pattern:
                if char_type == "C":
                    word += random.choice(cls.CONSONANTS)
                elif char_type == "V":
                    word += random.choice(cls.VOWELS)
            words.append(word.capitalize())

        return separator.join(words)

    @classmethod
    def generate_diceware(
        cls, num_words: int = 4, separator: str = "-", wordlist_path: str = None
    ) -> str:
        """
        Generates a passphrase using a wordlist.
        """
        if not wordlist_path or not os.path.exists(wordlist_path):
            # Fallback
            words = [
                "correct",
                "horse",
                "battery",
                "staple",
                "apple",
                "banana",
                "orange",
                "grape",
            ]
        else:
            with open(wordlist_path, "r", encoding="utf-8") as f:
                words = [
                    line.strip().split("\t")[-1]
                    for line in f.readlines()
                    if line.strip()
                ]

        selected = [random.choice(words).capitalize() for _ in range(num_words)]
        return separator.join(selected)
