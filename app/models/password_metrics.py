# This is a placeholder for a more complex data model.
# In a real application, this might be a SQLAlchemy model.

class PasswordMetrics:
    def __init__(self, password, entropy, score):
        self.password = password
        self.entropy = entropy
        self.score = score