from typing import Dict, Any

def analyze_passphrase(passphrase: str) -> Dict[str, Any]:
    """
    Analyzes a passphrase to determine its strength and provide detailed feedback.

    Calculates strength based on the number of words and estimates crack time.

    Args:
        passphrase: The passphrase to analyze.

    Returns:
        A dictionary containing the analysis details, including strength and crack time.
    """
    words = passphrase.split()
    num_words = len(words)
    
    # Assigns a strength category based on the number of words.
    # Provides a simplified assessment of passphrase robustness.
    if num_words < 4:
        strength = "Weak"
    elif num_words < 6:
        strength = "Good"
    elif num_words < 8:
        strength = "Strong"
    else:
        strength = "Very Strong"

    # Estimates the time required to crack the passphrase.
    # Offers a conceptual representation of computational effort.
    if num_words < 4:
        time_to_crack = "seconds"
    elif num_words < 5:
        time_to_crack = "a few hours"
    elif num_words < 6:
        time_to_crack = "several years"
    else:
        time_to_crack = "thousands of years"

    # Compiles detailed feedback for the user.
    # Explains the significance of passphrase length and estimated crack time.
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

    # Returns the comprehensive analysis of the passphrase.
    return {
        'strength': strength,
        'details': details
    }
