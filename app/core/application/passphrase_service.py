from typing import Dict, Any
from app.core.domain.passphrase import PassphraseDomain
from app.core.application.password_service import PasswordApplicationService


class PassphraseApplicationService:
    @staticmethod
    def generate(
        num_words: int, generator_type: str, separator: str, wordlist_path: str = None
    ) -> Dict[str, Any]:
        """
        Generates a passphrase and immediately analyzes its strength.
        """
        if generator_type == "pronounceable":
            passphrase = PassphraseDomain.generate_pronounceable(num_words, separator)
        else:
            passphrase = PassphraseDomain.generate_diceware(
                num_words, separator, wordlist_path
            )

        analysis = PasswordApplicationService.analyze(passphrase, check_pwned=False)
        return {"passphrase": passphrase, "analysis": analysis}
