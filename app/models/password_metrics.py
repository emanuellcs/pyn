from app.extensions import db

# Defines the data model for storing password-related metrics.
# This helps in tracking and analyzing the strength and characteristics of generated or evaluated passwords.
class PasswordMetrics(db.Model):
    # Uniquely identifies each password metric entry.
    id = db.Column(db.Integer, primary_key=True)
    # Stores the actual password string.
    # This allows for direct reference to the password being analyzed.
    password = db.Column(db.String(255), nullable=False)
    # Records the calculated entropy of the password.
    # Provides a quantitative measure of the password's randomness and unpredictability.
    entropy = db.Column(db.Float, nullable=False)
    # Stores a qualitative score for the password's strength.
    # Offers a simplified assessment of how strong the password is.
    score = db.Column(db.Integer, nullable=False)
    # Records the timestamp when the password metrics were created.
    # Tracks when the password was analyzed or generated.
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Provides a string representation of the PasswordMetrics object.
    # This aids in debugging and logging by offering a clear identifier for each instance.
    def __repr__(self):
        return f'<PasswordMetrics {self.id}>'