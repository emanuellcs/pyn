import random
import string
from typing import Dict, Any
from .analyzer import PasswordAnalysis
from .risk import is_secure

class PasswordGenerator:
    def __init__(self):
        """Initialize the password generator with character sets."""
        self.uppercase = string.ascii_uppercase  # Uppercase letters
        self.lowercase = string.ascii_lowercase  # Lowercase letters
        self.digits = string.digits  # Numeric digits
        self.special = "!@#$%^&*()_+-=[]{}|;:,.<>?"  # Special characters

    def generate(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a secure password based on provided options.

        This function generates a password, analyzes it for security risks, and
        regenerates it until it meets the security criteria defined in `is_secure`.

        Args:
            options (dict): Dictionary containing generation options.

        Returns:
            dict: Contains the generated secure password and its analysis.
        
        Raises:
            ValueError: If a secure password cannot be generated after multiple attempts.
        """
        max_attempts = 5
        for _ in range(max_attempts):
            try:
                length = int(options.get('length', 16))
                
                exclude = options.get('exclude_chars', '')
                
                # Build initial character sets based on options
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

                # Apply exclusions
                all_chars = [c for c in selected_char_sets if c not in exclude]

                if not all_chars:
                    raise ValueError("All characters excluded or no valid characters available.")

                password_chars = []

                # Fill the password with random characters from the allowed set
                for _ in range(length):
                    password_chars.append(random.SystemRandom().choice(all_chars))

                remaining_length = length - len(password_chars)
                for _ in range(remaining_length):
                    password_chars.append(random.SystemRandom().choice(all_chars))

                random.SystemRandom().shuffle(password_chars)
                password = ''.join(password_chars)
                
                analyzer = PasswordAnalysis(password)
                analyzer.analyze()
                analysis = analyzer.report()

                analysis["password"] = password
                if is_secure(analysis):
                    return {
                        "password": password,
                        "analysis": analysis,
                        "message": "Secure password generated successfully.",
                        "message_style": "background-color: green; color: white;"
                    }
            except ValueError as e:
                # Propagate errors related to character set issues
                raise ValueError(f"Password generation failed: {str(e)}")
        
        raise ValueError("Could not generate a secure password after several attempts. Try including other types of characters.")
