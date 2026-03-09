from app.core.domain.password import PasswordDomain
from app.infrastructure.hibp import HIBPService
from app.infrastructure.crypto import CryptoService


def test_password_entropy():
    result = PasswordDomain.calculate_entropy("password")
    assert result["entropy"] > 0
    assert result["expected_guesses"] > 0


def test_password_complexity():
    result = PasswordDomain.check_complexity_requirements("A1!a" * 4)
    assert result["min_length"] is True
    assert result["has_uppercase"] is True
    assert result["has_numbers"] is True
    assert result["has_special"] is True


def test_k_anonymity_hibp(monkeypatch):
    class MockResponse:
        status_code = 200
        text = "00000:1\n11111:5\n"

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    # "password" -> SHA1 is 5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8
    # Prefix: 5BAA6, Suffix: 1E4C9B93F3F0682250B6CF8331B7EE68FD8

    # We just test the parsing mechanism
    def mock_fetch_hibp_range(prefix):
        return "1E4C9B93F3F0682250B6CF8331B7EE68FD8:123\nOTHER:456"

    monkeypatch.setattr(HIBPService, "_fetch_hibp_range", mock_fetch_hibp_range)

    count = HIBPService.check_pwned("password")
    assert count == 123


def test_crypto_service(app):
    with app.app_context():
        # app context needed for current_app.config
        encrypted = CryptoService.encrypt_data("test_secret")
        assert encrypted != b""
        assert encrypted != "test_secret".encode("utf-8")

        decrypted = CryptoService.decrypt_data(encrypted)
        assert decrypted == "test_secret"
