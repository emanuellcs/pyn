import random
import os

base_dir = os.path.dirname(__file__)
wordlist_path = os.path.join(base_dir, "wordlists", "eff_large_wordlist.txt")

# Manages passphrase generation using a wordlist.
# Provides methods to load words and construct passphrases based on dice rolls.
class PassphraseGenerator:
    def __init__(self, wordlist_path: str):
        # Initializes the generator by loading the wordlist.
        # Ensures the wordlist is available for passphrase generation.
        self.wordlist = self._load_wordlist(wordlist_path)
    
    def _load_wordlist(self, path: str) -> dict:
        # Loads words from a specified wordlist file.
        # Each line in the file contains a dice roll sequence and a corresponding word.
        wordlist = {}
        with open(path, 'r') as f:
            for line in f:
                if line.strip():
                    key, word = line.strip().split()
                    wordlist[key] = word
        return wordlist

    def _roll_dice(self) -> str:
        # Simulates rolling five six-sided dice.
        # Generates a 5-digit string representing the dice roll, used to look up words.
        return ''.join(str(random.randint(1, 6)) for _ in range(5))

    def generate(self, num_words: int, separator: str = '-', capitalize: bool = False) -> str:
        """
        Generates a passphrase with customizable options.

        Constructs a passphrase by rolling dice to select words from the loaded wordlist.

        Args:
            num_words (int): The number of words to include in the passphrase.
            separator (str): The character used to join words in the passphrase.
            capitalize (bool): If true, capitalizes the first letter of each word.

        Returns:
            str: The generated passphrase.
        """
        # Validates that the number of words is a positive integer.
        # Ensures proper input for passphrase generation.
        if not isinstance(num_words, int) or num_words <= 0:
            raise ValueError("Number of words must be a positive integer.")
        
        words = []
        # Continuously rolls dice and appends words until the desired number of words is reached.
        while len(words) < num_words:
            roll = self._roll_dice()
            word = self.wordlist.get(roll)
            if word:
                words.append(word.capitalize() if capitalize else word)
            
        # Joins the selected words with the specified separator.
        return separator.join(words)