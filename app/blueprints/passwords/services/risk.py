def is_secure(password_analysis):
    """
    Evaluates if a password is secure enough based on its analysis.
    """
    pwned_check = password_analysis.get("pwned_password_check", {})
    zxcvbn_analysis = password_analysis.get("zxcvbn_analysis", {})
    strength_metrics = password_analysis.get("password_strength_metrics", {})
    password_length = len(password_analysis.get("password", ""))

    if pwned_check.get("pwned", False):
        return False

    # Relaxed requirements for shorter passwords
    if password_length < 12:
        if zxcvbn_analysis.get("score", 0) < 2:
            return False
        if strength_metrics.get("entropy", 0) < 30:
            return False
    else:
        if zxcvbn_analysis.get("score", 0) < 3:
            return False
        if strength_metrics.get("entropy", 0) < 60:
            return False
            
    return True