from app.extensions import db
from app.infrastructure.crypto import CryptoService


class PasswordMetrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _password_encrypted = db.Column("password", db.LargeBinary, nullable=False)
    entropy = db.Column(db.Float, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    @property
    def password(self) -> str:
        if not self._password_encrypted:
            return ""
        return CryptoService.decrypt_data(self._password_encrypted)

    @password.setter
    def password(self, value: str):
        if value:
            self._password_encrypted = CryptoService.encrypt_data(value)
        else:
            self._password_encrypted = b""

    def __repr__(self):
        return f"<PasswordMetrics {self.id}>"
