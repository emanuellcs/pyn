import random
import string
from typing import Dict, Any
from password_analyzer import PasswordAnalysis

class PasswordGenerator:
    def __init__(self):
        """Initialize the password generator with character sets."""
        self.uppercase = string.ascii_uppercase  # Uppercase letters
        self.lowercase = string.ascii_lowercase  # Lowercase letters
        self.digits = string.digits  # Numeric digits
        self.special = "!@#$%^&*()_+-=[]{}|;:,.<>?"  # Special characters

    def generate(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a password based on provided options and analyze it, ensuring it's not pwned.

        Args:
            options (dict): Dictionary containing generation options.

        Returns:
            dict: Contains generated password and its analysis.
        """
        max_attempts = 5  # Limit the number of attempts to generate a password
        attempts = 0
        while attempts < max_attempts:
            try:
                # Validate options and set password length
                length = min(max(int(options.get('length', 12)), 12), 64)

                # Build character set based on user options
                chars = ''
                if options.get('use_upper', True):
                    chars += self.uppercase
                if options.get('use_lower', True):
                    chars += self.lowercase
                if options.get('use_digits', True):
                    chars += self.digits
                if options.get('use_special', True):
                    chars += self.special

                # Remove excluded characters from the character set
                exclude = options.get('exclude_chars', '')
                for char in exclude:
                    chars = chars.replace(char, '')

                if not chars:
                    raise ValueError("No valid characters available for password generation")

                # Generate password using random choices from the character set
                password = ''.join(random.SystemRandom().choice(chars) for _ in range(length))

                # Analyze the generated password and check if it's pwned
                analyzer = PasswordAnalysis(password)
                analyzer.analyze()
                pwned_count = analyzer.check_pwned()
                analysis = analyzer.report()

                # Return the result based on the Pwned status
                if pwned_count == 0:
                    return {
                        "password": password,
                        "analysis": analysis,
                        "message": "Not Pwned",  # Message indicating the password is safe
                        "message_style": "background-color: green; color: white;"  # Style for safe message
                    }
                else:
                    return {
                        "password": password,
                        "analysis": analysis,
                        "message": f"Pwned {pwned_count} times. Please generate another password.",  # Message indicating the password has been compromised
                        "message_style": "background-color: red; color: white;"  # Style for compromised message
                    }
                    
                attempts += 1  # Increment attempts
            except ValueError as e:
                raise ValueError(f"Password generation failed: {str(e)}")

        return {"error": "Could not generate a non-pwned password after several attempts."}
