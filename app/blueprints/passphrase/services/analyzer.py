import math
from typing import Dict, Any

def analyze_passphrase(passphrase: str) -> Dict[str, Any]:
    """
    Analyzes a passphrase to determine its strength and provide detailed feedback.

    Args:
        passphrase: The passphrase to analyze.

    Returns:
        A dictionary containing the analysis details.
    """
    words = passphrase.split()
    num_words = len(words)
    
    # Simplified strength categories based on the number of words
    if num_words < 4:
        strength = "Weak"
    elif num_words < 6:
        strength = "Good"
    elif num_words < 8:
        strength = "Strong"
    else:
        strength = "Very Strong"

    # Simplified crack time estimation
    # This is a conceptual representation. A real-world calculation would be more complex.
    if num_words < 4:
        time_to_crack = "seconds"
    elif num_words < 5:
        time_to_crack = "a few hours"
    elif num_words < 6:
        time_to_crack = "several years"
    else:
        time_to_crack = "thousands of years"

    details = [
        {
            'title': 'Length',
            'explanation': f'Your passphrase has {num_words} words. Longer passphrases are exponentially harder to guess. ✅'
        },
        {
            'title': 'Time to Crack',
            'explanation': f'It would take a standard desktop computer approximately {time_to_crack} to crack this passphrase. ⏳'
        }
    ]

    return {
        'strength': strength,
        'details': details
    }
