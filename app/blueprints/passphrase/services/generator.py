import random
import os

base_dir = os.path.dirname(__file__)
wordlist_path = os.path.join(base_dir, "wordlists", "eff_large_wordlist.txt")

class PassphraseGenerator:
    def __init__(self, wordlist_path: str):
        self.wordlist = self._load_wordlist(wordlist_path)
    
    def _load_wordlist(self, path: str) -> dict:
        wordlist = {}
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    key, word = line.strip().split()
                    wordlist[key] = word
        return wordlist

    def _roll_dice(self) -> str:
        return ''.join(str(random.randint(1, 6)) for _ in range(5))

    def generate(self, num_words: int, separator: str = '-', capitalize: bool = False) -> str:
        """
        Generate a passphrase with customizable options.

        Args:
            num_words (int): The number of words in the passphrase.
            separator (str): The character to separate words.
            capitalize (bool): Whether to capitalize each word.

        Returns:
            str: The generated passphrase.
        """
        if not isinstance(num_words, int) or num_words <= 0:
            raise ValueError("Number of words must be a positive integer.")
        
        words = []
        while len(words) < num_words:
            roll = self._roll_dice()
            word = self.wordlist.get(roll)
            if word:
                words.append(word.capitalize() if capitalize else word)
            
        return separator.join(words)