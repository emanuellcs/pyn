def is_secure(passphrase):
    # Checks if the passphrase contains at least four words.
    # This is a simplified security metric.
    return len(passphrase.split('-')) >= 4