# Enables testing mode for the application.
# This configures the application for a testing environment, allowing for specific test behaviors.
TESTING = True
# Provides a secret key for testing purposes.
# This key is used for session management and other security-related features during tests.
SECRET_KEY = "test-key"
# Disables CSRF protection for testing.
# This simplifies testing by removing the need for CSRF tokens in test requests.
WTF_CSRF_ENABLED = False