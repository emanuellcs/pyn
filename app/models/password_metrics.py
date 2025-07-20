from app.extensions import db

# Defines the data model for storing password-related metrics.
# This helps in tracking and analyzing the strength and characteristics of generated or evaluated passwords.
class PasswordMetrics(db.Model):
    # Uniquely identifies each password metric entry.
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    entropy = db.Column(db.Float, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Provides a string representation of the PasswordMetrics object.
    # This aids in debugging and logging by offering a clear identifier for each instance.
    def __repr__(self):
        return f'<PasswordMetrics {self.id}>'