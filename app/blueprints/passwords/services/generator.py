import random
import string
from typing import Dict, Any
from .analyzer import PasswordAnalysis
from .risk import is_secure

class PasswordGenerator:
    """
    Generates random passwords based on specified criteria.

    Ensures generated passwords meet security requirements by integrating with
    password analysis and risk assessment services.
    """
    def __init__(self):
        # Initializes the generator with predefined character sets.
        # These sets are used to construct passwords based on user options.
        self.uppercase = string.ascii_uppercase
        self.lowercase = string.ascii_lowercase
        self.digits = string.digits
        self.special = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    def generate(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a secure password based on provided options, analyzes its strength,
        and regenerates if it does not meet security criteria.

        Args:
            options (dict): A dictionary containing password generation parameters,
                            such as length, character types to include, and characters to exclude.

        Returns:
            dict: A dictionary containing the generated secure password, its detailed analysis,
                  and a message indicating success.
        
        Raises:
            ValueError: If a secure password cannot be generated after a maximum number of attempts,
                        or if no valid character types are selected/available.
        """
        
        max_attempts = 5 # You can change the value if you wish.

        # Attempts to generate a secure password multiple times.
        # This loop ensures that the generated password meets the defined security standards.
        for _ in range(max_attempts):
            try:
                length = int(options.get('length', 16))
                
                exclude = options.get('exclude_chars', '')
                
                # Builds the character set for password generation based on user options.
                selected_char_sets = []
                if options.get('use_upper', True):
                    selected_char_sets.extend(self.uppercase)
                if options.get('use_lower', True):
                    selected_char_sets.extend(self.lowercase)
                if options.get('use_digits', True):
                    selected_char_sets.extend(self.digits)
                if options.get('use_special', True):
                    selected_char_sets.extend(self.special)

                if not selected_char_sets:
                    raise ValueError("No character types selected for password generation.")

                # Filters out excluded characters from the selected character set.
                all_chars = [c for c in selected_char_sets if c not in exclude]

                if not all_chars:
                    raise ValueError("All characters excluded or no valid characters available.")

                password_chars = []

                # Fills the password with random characters from the allowed set.
                for _ in range(length):
                    password_chars.append(random.SystemRandom().choice(all_chars))

                # Ensures the password reaches the desired length, if initial filling was insufficient.
                remaining_length = length - len(password_chars)
                for _ in range(remaining_length):
                    password_chars.append(random.SystemRandom().choice(all_chars))

                # Shuffles the characters to ensure randomness and joins them to form the password.
                random.SystemRandom().shuffle(password_chars)
                password = ''.join(password_chars)
                
                # Analyzes the generated password for strength and security.
                analyzer = PasswordAnalysis(password)
                analyzer.analyze()
                analysis = analyzer.report()

                analysis["password"] = password
                # Checks if the generated password is secure according to defined criteria.
                if is_secure(analysis):
                    return {
                        "password": password,
                        "analysis": analysis,
                        "message": "Secure password generated successfully.",
                        "message_style": "background-color: green; color: white;"
                    }
            except ValueError as e:
                # Propagates specific ValueError exceptions related to character set issues.
                raise ValueError(f"Password generation failed: {str(e)}")
        
        # Raises an error if a secure password cannot be generated after multiple attempts.
        raise ValueError("Could not generate a secure password after several attempts. Try including other types of characters.")
